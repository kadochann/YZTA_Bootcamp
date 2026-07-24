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

logger = logging.getLogger(__name__)

# Add root project dir to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.llm_service import extract_symptoms, map_evidences_and_urgency
from src.rag_service import get_rag_service

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
        predict_req = PredictRequest(
            age=req.age,
            sex=req.sex[0].upper() if req.sex else None, # M or F or E
            evidences=mapping["evidences"],
            initial_evidence=mapping["initial_evidence"],
            top_k=3
        )
        prediction_response = predict(predict_req)
        
        # 5. Build Response
        return TriageResponse(
            patient_name=req.full_name,
            age=req.age,
            sex=req.sex,
            urgency=mapping["urgency"],
            symptoms=symptoms,
            prediction=prediction_response
        )
    except Exception as e:
        logger.exception("Error during triage workflow")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if not _state:
        raise HTTPException(status_code=503, detail="Model not loaded")

    model = _state['model']
    classes = _state['classes']

    if req.sex is None:
        # Sex unknown/undisclosed: marginalize by averaging predictions for M and F
        # rather than injecting an undefined "0.5" value into a tree-based model.
        X_m, unrecognized = build_single_feature_vector(req, sex_override='M')
        X_f, _ = build_single_feature_vector(req, sex_override='F')
        proba = (model.predict(X_m)[0] + model.predict(X_f)[0]) / 2.0
    else:
        X, unrecognized = build_single_feature_vector(req)
        proba = model.predict(X)[0]

    order = np.argsort(proba)[::-1][:req.top_k]
    differential = [Diagnosis(pathology=classes[i], probability=float(proba[i])) for i in order]

    return PredictResponse(
        top_prediction=differential[0],
        differential=differential,
        unrecognized_evidences=unrecognized,
    )