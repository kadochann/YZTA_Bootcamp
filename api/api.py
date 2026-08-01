"""
FastAPI service wrapping the trained DDXPlus LightGBM model.

Expected files alongside this script (or set via env vars):
  - ddx_lightgbm_model.txt   (from model.save_model(...))
  - label_classes.json       (from json.dump(label_encoder.classes_.tolist(), ...))
  - release_evidences.json   (the DDXPlus schema file)

Run locally:
  uvicorn api:app --reload --port 8000
"""
import os
import json
import numpy as np
import lightgbm as lgb
import sys
from scipy.sparse import csr_matrix, hstack
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging

# Temperature scaling for probability calibration.
# Higher values spread out the distribution (reduce over-confidence).
# Set PREDICT_TEMPERATURE in .env to override.
# NOTE: The primary misdiagnosis fix is the RAG landmine filter in rag_service.py.
# Scaling above 1.0 flattens ALL predictions (not just wrong ones) so default is 1.0 (off).
PREDICT_TEMPERATURE = float(os.environ.get("PREDICT_TEMPERATURE", "1.0"))


logger = logging.getLogger(__name__)

# Add root project dir to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.llm_service import extract_symptoms, map_evidences_and_urgency
from src.rag_service import get_rag_service
from src.db.database import SessionLocal
from src.db.models import Patient

MODEL_PATH = os.environ.get('DDX_MODEL_PATH', '../model/ddx_lightgbm_model.txt')
CLASSES_PATH = os.environ.get('DDX_CLASSES_PATH', './util/label_classes.json')
EVIDENCES_PATH = os.environ.get('DDX_EVIDENCES_PATH', './util/release_evidences.json')
SCHEMA_PATH = os.environ.get('DDX_SCHEMA_PATH', './util/feature_schema.json')

app = FastAPI(title="DDX Triage Model API", version="1.0")

# ---------- Load model + schema once at startup ----------
_state = {}

@app.on_event("startup")
def load_artifacts():
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model file not found at {MODEL_PATH}")
    if not os.path.exists(CLASSES_PATH):
        raise RuntimeError(f"Label classes file not found at {CLASSES_PATH}")
    if not os.path.exists(EVIDENCES_PATH):
        raise RuntimeError(f"Evidences schema not found at {EVIDENCES_PATH}")
    if not os.path.exists(SCHEMA_PATH):
        raise RuntimeError(
            f"Feature schema not found at {SCHEMA_PATH}. This must be the "
            f"vocab/initial_evidence ordering saved at training time (section7_pipeline.py) "
            f"-- do not regenerate it, or column indices may silently drift out of sync with the model."
        )

    model = lgb.Booster(model_file=MODEL_PATH)

    with open(CLASSES_PATH) as f:
        classes = json.load(f)

    with open(EVIDENCES_PATH) as f:
        evidences = json.load(f)  # used only for the /evidences reference endpoint

    with open(SCHEMA_PATH) as f:
        schema = json.load(f)
    vocab = schema['vocab']
    col_index = {tok: i for i, tok in enumerate(vocab)}
    ie_index = {code: i for i, code in enumerate(schema['initial_evidence_codes'])}

    _state.update(
        model=model,
        classes=classes,
        evidences=evidences,
        col_index=col_index,
        ie_index=ie_index,
        vocab_size=len(vocab),
    )


# ---------- Request / response schemas ----------
class PredictRequest(BaseModel):
    age: int = Field(..., ge=0, le=120)
    sex: Optional[str] = Field(None, pattern="^[MFE]$", description="Omit if unknown/undisclosed")
    evidences: list[str] = Field(
        ..., description="List of evidence tokens, e.g. ['E_53', 'E_54_@_V_112']"
    )
    initial_evidence: Optional[str] = Field(
        None, description="The evidence code treated as the chief complaint, e.g. 'E_53'"
    )
    top_k: int = Field(3, ge=1, le=10)


class Diagnosis(BaseModel):
    pathology: str
    probability: float


class PredictResponse(BaseModel):
    top_prediction: Diagnosis
    differential: list[Diagnosis]
    unrecognized_evidences: list[str]

class TriageRequest(BaseModel):
    full_name: str
    national_id: Optional[str] = None
    age: int
    sex: str
    complaint: str

class TriageResponse(BaseModel):
    patient_name: str
    age: int
    sex: str
    urgency: int
    symptoms: list[str]
    prediction: PredictResponse


# ---------- Debug request / response schemas ----------

class DebugExtractRequest(BaseModel):
    complaint: str = Field(..., description="Free-text patient complaint (any language).")

class DebugExtractResponse(BaseModel):
    symptoms: list[str] = Field(description="Extracted atomic clinical statements.")
    prompt_path: str = Field(description="Prompt file used for this call.")

class DebugRagRequest(BaseModel):
    clinical_statement: str = Field(
        ..., description="A single clinical statement to retrieve RAG candidates for."
    )

class DebugRagResponse(BaseModel):
    clinical_statement: str
    candidates: dict = Field(description="Enriched RAG candidate pool for this statement.")

class DebugMapRequest(BaseModel):
    enriched_rag_results: list[dict] = Field(
        ...,
        description=(
            "Pre-built RAG output list — the same structure returned by /debug/rag. "
            "Each element must have 'clinical_statement' and 'candidates' keys."
        ),
        examples=[[
            {
                "clinical_statement": "Fever is present.",
                "candidates": {
                    "E_91": {"question": "Do you have a fever?", "retrieval_rank": 1}
                }
            }
        ]]
    )

class DebugMapResponse(BaseModel):
    evidences: list[str]
    initial_evidence: str
    urgency: int
    reasoning: Optional[str] = Field(None, description="LLM reasoning field if returned.")
    prompt_path: str

# ---------- Feature building for a single request ----------
def build_single_feature_vector(req: PredictRequest, sex_override: Optional[str] = None):
    col_index = _state['col_index']
    ie_index = _state['ie_index']
    vocab_size = _state['vocab_size']

    unrecognized = [e for e in req.evidences if e not in col_index]

    ev_indices = [col_index[e] for e in req.evidences if e in col_index]
    ev_data = np.ones(len(ev_indices), dtype=np.int8)
    X_ev = csr_matrix(
        (ev_data, (np.zeros(len(ev_indices), dtype=int), ev_indices)),
        shape=(1, vocab_size), dtype=np.int8,
    )

    from scipy.sparse import lil_matrix
    X_ie = lil_matrix((1, len(ie_index)), dtype=np.int8)
    if req.initial_evidence and req.initial_evidence in ie_index:
        X_ie[0, ie_index[req.initial_evidence]] = 1
    elif req.initial_evidence:
        unrecognized.append(req.initial_evidence)
    X_ie = X_ie.tocsr()

    sex_value = sex_override if sex_override is not None else req.sex
    age = np.array([[req.age]], dtype=np.float32)
    sex = np.array([[1.0 if sex_value == 'M' else 0.0]], dtype=np.float32)
    dense = csr_matrix(np.hstack([age, sex]))

    X = hstack([X_ev, X_ie, dense], format='csr')
    return X, unrecognized


# ---------- Endpoints ----------
@app.get("/evidences")
def get_evidences():
    """Schema reference for the LLM extraction layer: which evidence codes exist,
    their question text, data type, and (for non-binary) valid values."""
    return _state['evidences']


@app.get("/health")
def health():
    return {"status": "ok", "vocab_size": _state.get('vocab_size'), "num_classes": len(_state.get('classes', []))}


@app.post("/triage", response_model=TriageResponse)
def triage(req: TriageRequest):
    db = SessionLocal()
    try:
        # 1. Extraction: 1 LLM call
        symptoms = extract_symptoms(req.complaint)
        
        # 2. Retrieval & Enrichment (RAG)
        rag_service = get_rag_service()
        enriched_results = []
        for sym in symptoms:
            result = rag_service.retrieve_and_enrich(sym)
            enriched_results.append(result)
            
        # 3. Evidence Mapping: 1 LLM call
        mapping = map_evidences_and_urgency(enriched_results)
        
        # 4. Local ML Prediction
        # Normalize sex: UI may send Turkish strings ("Erkek"/"Kadın") or single chars.
        _SEX_MAP = {
            "erkek": "M", "e": "M", "m": "M",
            "kadın": "F", "kadin": "F", "k": "F", "f": "F",
        }
        sex_code = _SEX_MAP.get((req.sex or "").lower().strip()) if req.sex else None
        predict_req = PredictRequest(
            age=req.age,
            sex=sex_code,
            evidences=mapping["evidences"],
            initial_evidence=mapping["initial_evidence"],
            top_k=3
        )
        prediction_response = predict(predict_req)
        
        # 5. Save to database
        db_patient = Patient(
            full_name=req.full_name,
            national_id=req.national_id,
            age=req.age,
            sex=req.sex,
            complaints=symptoms,
            urgency_score=mapping["urgency"],
            top_prediction={"pathology": prediction_response.top_prediction.pathology, "probability": prediction_response.top_prediction.probability},
            differentials=[{"pathology": d.pathology, "probability": d.probability} for d in prediction_response.differential],
            evidences=mapping.get("evidences", []),
            initial_evidence=mapping.get("initial_evidence")
        )
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        
        # 6. Build Response
        return TriageResponse(
            patient_name=req.full_name,
            age=req.age,
            sex=req.sex,
            urgency=mapping["urgency"],
            symptoms=symptoms,
            prediction=prediction_response
        )
    except Exception as e:
        db.rollback()
        logger.exception("Error during triage workflow")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if not _state:
        raise HTTPException(status_code=503, detail="Model not loaded")

    model = _state['model']
    classes = _state['classes']

    if req.sex is None:
        X_m, unrecognized = build_single_feature_vector(req, sex_override='M')
        X_f, _ = build_single_feature_vector(req, sex_override='F')
        raw_proba = (model.predict(X_m)[0] + model.predict(X_f)[0]) / 2.0
    else:
        X, unrecognized = build_single_feature_vector(req)
        raw_proba = model.predict(X)[0]

    # Temperature scaling: softmax over log-probabilities scaled by 1/T.
    # Prevents a single landmine feature from yielding 99.9% certainty.
    if PREDICT_TEMPERATURE != 1.0:
        log_p = np.log(np.clip(raw_proba, 1e-12, None))
        scaled = log_p / PREDICT_TEMPERATURE
        scaled -= scaled.max()  # numerical stability
        proba = np.exp(scaled) / np.exp(scaled).sum()
    else:
        proba = raw_proba

    order = np.argsort(proba)[::-1][:req.top_k]
    differential = [Diagnosis(pathology=classes[i], probability=float(proba[i])) for i in order]

    return PredictResponse(
        top_prediction=differential[0],
        differential=differential,
        unrecognized_evidences=unrecognized,
    )


# ==========================================================
# DEBUG / TESTING ENDPOINTS
# These endpoints isolate each pipeline step so individual
# LLM calls and the RAG layer can be tested independently.
# ==========================================================

@app.post(
    "/debug/extract",
    response_model=DebugExtractResponse,
    summary="[Debug] LLM-1: Extract clinical statements from free text",
    tags=["Debug"],
)
def debug_extract(req: DebugExtractRequest):
    """
    Runs ONLY the first LLM call (information extraction).
    Accepts any free-text complaint (including non-English) and returns
    the list of atomic clinical statements produced by the extraction prompt.
    """
    import src.llm_service as svc
    try:
        symptoms = svc.extract_symptoms(req.complaint)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return DebugExtractResponse(
        symptoms=symptoms,
        prompt_path=svc.EXTRACTION_PROMPT_PATH,
    )


@app.post(
    "/debug/rag",
    response_model=DebugRagResponse,
    summary="[Debug] RAG: Retrieve & enrich candidates for one clinical statement",
    tags=["Debug"],
)
def debug_rag(req: DebugRagRequest):
    """
    Runs ONLY the RAG retrieval step for a single clinical statement.
    Returns the enriched candidate pool exactly as it would be fed to LLM-2.
    No LLM call is made.
    """
    try:
        rag_service = get_rag_service()
        result = rag_service.retrieve_and_enrich(req.clinical_statement)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return DebugRagResponse(
        clinical_statement=result["clinical_statement"],
        candidates=result["candidates"],
    )


@app.post(
    "/debug/map",
    response_model=DebugMapResponse,
    summary="[Debug] LLM-2: Map pre-built RAG results to evidence expressions",
    tags=["Debug"],
)
def debug_map(req: DebugMapRequest):
    """
    Runs ONLY the second LLM call (evidence mapping).
    Accepts a pre-built enriched RAG results list (e.g. from /debug/rag or
    crafted manually) and returns evidence codes, initial evidence,
    urgency score, and the LLM's step-by-step reasoning.

    Tip: Chain /debug/extract → /debug/rag (per statement) → /debug/map
    to replay the full pipeline with full visibility at each step.
    """
    import src.llm_service as svc
    from google import genai
    from google.genai import types
    import json as _json

    # Re-use the internal helper but also capture the raw `reasoning` field
    with open(svc.MAPPING_PROMPT_PATH, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    input_data = _json.dumps(req.enriched_rag_results, indent=2)
    prompt = f"{prompt_template}\n\n--------------------------------------------------\nINPUT:\n{input_data}"

    client = svc._get_gemini_client()
    try:
        response = svc._generate_with_retry(
            client,
            model='gemini-3.5-flash',
            prompt=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.0,
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        result = _json.loads(response.text)
    except _json.JSONDecodeError as e:
        raise HTTPException(status_code=502, detail=f"LLM returned invalid JSON: {e}\nRaw: {response.text}")

    return DebugMapResponse(
        evidences=result.get("evidences", []),
        initial_evidence=result.get("initial_evidence", ""),
        urgency=result.get("urgency", 5),
        reasoning=result.get("reasoning"),
        prompt_path=svc.MAPPING_PROMPT_PATH,
    )