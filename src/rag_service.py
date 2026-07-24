import os
import json
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_UTIL_DIR = os.path.join(BASE_DIR, 'api', 'util')
EMBEDDINGS_PATH = os.path.join(API_UTIL_DIR, 'embeddings_v3.json')
VALUE_DICT_PATH = os.path.join(API_UTIL_DIR, 'value_dict.json')

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
        Retrieves the top-1 document for a given clinical statement,
        and enriches the possible_values with their meanings.
        """
        if not self.vectorstore:
            raise RuntimeError("Vectorstore not initialized")
            
        # Top-1 retrieval
        results = self.vectorstore.similarity_search(clinical_statement, k=1)
        if not results:
            return {"clinical_statement": clinical_statement, "members": {}}
            
        best_doc = results[0]
        members = json.loads(best_doc.metadata.get("members", "{}"))
        
        # Enrich possible_values
        for ev_id, ev_data in members.items():
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
            "members": members
        }

# Singleton instance for the service
_rag_service_instance = None

def get_rag_service() -> RAGService:
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    return _rag_service_instance
