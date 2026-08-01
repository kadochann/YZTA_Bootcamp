import os
import json
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_UTIL_DIR = os.path.join(BASE_DIR, 'api', 'util')
EMBEDDINGS_PATH = os.path.join(API_UTIL_DIR, 'embeddings_v3.json')
VALUE_DICT_PATH = os.path.join(API_UTIL_DIR, 'value_dict.json')

# Configurable RAG retrieval count — set RAG_K in .env to override (default: 4)
RAG_K = int(os.environ.get("RAG_K", "4"))

# ---------------------------------------------------------------------------
# LANDMINE FILTER
# These evidence codes are so disease-specific that they are near-exclusive
# indicators of a single pathology in the DDXPlus training set. Surfacing
# them via RAG for an unrelated complaint hijacks the LightGBM model with
# 95-100% single-code certainty, making all other evidence irrelevant.
#
# Only codes whose underlying question has NO plausible clinical meaning
# outside its designated disease are included ("surgical" approach).
# Medically overlapping codes (e.g. panic attack, anemia, PE) are intentionally
# kept accessible so real cases of those diseases are not blinded.
# ---------------------------------------------------------------------------
LANDMINE_CODES: frozenset = frozenset({
    # Myasthenia Gravis — jaw weakness, double vision, fatigability, dysphagia
    "E_38", "E_63", "E_52", "E_90", "E_28", "E_65",
    # Acute Dystonic Reactions — eye rolling, spasms, torticollis, grimacing
    "E_205", "E_192", "E_193", "E_147", "E_15", "E_128", "E_168", "E_180", "E_62",
    # Guillain-Barré Syndrome — bilateral ascending paralysis, absent reflexes
    "E_156", "E_157", "E_83", "E_93", "E_177", "E_84", "E_0", "E_176",
    # Whooping Cough — inspiratory whoop
    "E_112", "E_166",
    # Atrial Fibrillation — irregular/fluttering heartbeat
    "E_164", "E_19", "E_139", "E_76", "E_22",
    # PSVT — paroxysmal sudden-onset tachycardia
    "E_60", "E_213", "E_35", "E_16",
    # Scombroid Food Poisoning — fish-related flushing/rash
    "E_187", "E_92",
    # Boerhaave Syndrome — esophageal rupture
    "E_211",
    # GERD — heartburn / acid regurgitation
    "E_215", "E_173", "E_98",
    # Cluster Headache — unilateral eye tearing/redness
    "E_184", "E_127", "E_25",
    # Spontaneous Rib Fracture
    "E_216", "E_37", "E_153",
})

class RAGService:
    def __init__(self):
        self.vectorstore = None
        self.value_dict = {}
        self._load_value_dict()
        self._initialize_vectorstore()

    def _load_value_dict(self):
        if os.path.exists(VALUE_DICT_PATH):
            with open(VALUE_DICT_PATH, 'r', encoding='utf-8') as f:
                self.value_dict = json.load(f)

    def _initialize_vectorstore(self):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
        persist_dir = os.path.join(API_UTIL_DIR, "chroma_db_v3")
        
        if os.path.exists(persist_dir):
            print("Loading Chroma Vector Store from disk...")
            self.vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
            print("Vector Store loaded successfully.")
        else:
            print("WARNING: Chroma DB v3 not found on disk yet! Waiting for background builder script to finish...")
            # We initialize an empty one so it doesn't crash, but it won't return good results until the script finishes and we restart Uvicorn.
            self.vectorstore = Chroma(embedding_function=embeddings)

    def retrieve_and_enrich(self, clinical_statement: str) -> dict:
        """
        Retrieves the top-k documents for a given clinical statement,
        merges and deduplicates their member evidences into a unified
        candidate pool, tags each with retrieval_rank, and enriches
        possible_values with their meanings.
        """
        if not self.vectorstore:
            raise RuntimeError("Vectorstore not initialized")
            
        # Top-k retrieval (k configured via RAG_K env var)
        results = self.vectorstore.similarity_search(clinical_statement, k=RAG_K)
        if not results:
            return {"clinical_statement": clinical_statement, "candidates": {}}

        # Merge candidates across all k retrieved documents.
        # If the same evidence ID appears in multiple docs, keep the one
        # from the highest-ranked (lowest rank number) retrieval.
        candidates = {}
        for rank, doc in enumerate(results, start=1):
            members = json.loads(doc.metadata.get("members", "{}"))
            for ev_id, ev_data in members.items():
                if ev_id not in candidates:
                    ev_data["retrieval_rank"] = rank
                    candidates[ev_id] = ev_data
                # else: already seen from a better-ranked doc, skip
        
        # Remove landmine evidence codes — disease-specific codes that hijack
        # the ML model if spuriously matched by the LLM.
        candidates = {ev_id: ev_data for ev_id, ev_data in candidates.items()
                      if ev_id not in LANDMINE_CODES}

        # Enrich possible_values with human-readable meanings
        for ev_id, ev_data in candidates.items():
            if "possible_values" in ev_data:
                meanings = {}
                for val in ev_data["possible_values"]:
                    # Ensure val is a string representation for dictionary lookup
                    val_str = str(val)
                    if val_str in self.value_dict:
                        meanings[val_str] = self.value_dict[val_str]
                ev_data["possible_value_meanings"] = meanings
                
        return {
            "clinical_statement": clinical_statement,
            "candidates": candidates
        }

# Singleton instance for the service
_rag_service_instance = None

def get_rag_service() -> RAGService:
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    return _rag_service_instance
