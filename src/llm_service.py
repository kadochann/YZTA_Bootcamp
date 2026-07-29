import os
import json
import time
from google import genai
from google.genai import types

# Setup paths relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS_DIR = os.path.join(BASE_DIR, 'prompts')

EXTRACTION_PROMPT_PATH = os.path.join(PROMPTS_DIR, 'information_extraction.txt')
MAPPING_PROMPT_PATH = os.path.join(PROMPTS_DIR, 'evidence_mapping_v2.txt')

def _get_gemini_client():
    """Initializes the Gemini client using the API key."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    return genai.Client(api_key=api_key)

import logging
logger = logging.getLogger(__name__)

def _generate_with_retry(client, model: str, prompt: str, config, max_retries: int = 3):
    """Calls generate_content with automatic retry on 429 rate limit errors."""
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=prompt,
                config=config
            )
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                # Parse retry delay from error if available, default to 15s
                wait = 15
                import re
                match = re.search(r'retryDelay.*?(\d+)s', err_str)
                if match:
                    wait = int(match.group(1)) + 2  # add small buffer
                if attempt < max_retries - 1:
                    logger.warning(f"Rate limited (429). Waiting {wait}s before retry {attempt + 1}/{max_retries - 1}...")
                    time.sleep(wait)
                    continue
            raise
    raise RuntimeError("Max retries exceeded for Gemini API call.")

def extract_symptoms(complaint: str) -> list[str]:
    """
    Translates (if necessary) and extracts atomic medical symptom statements
    from a free-text chief complaint using exactly one LLM call.
    """
    with open(EXTRACTION_PROMPT_PATH, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    prompt = prompt_template.replace("{{PATIENT_TEXT}}", complaint)
    
    client = _get_gemini_client()
    try:
        response = _generate_with_retry(
            client,
            model='gemini-flash-latest',
            prompt=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.0
            )
        )
    except Exception as e:
        logger.error(f"Error calling Gemini in extract_symptoms: {e}")
        raise RuntimeError(f"LLM extraction failed: {e}")
    
    try:
        statements = json.loads(response.text)
        if isinstance(statements, list):
            return statements
        return []
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in extract_symptoms: {e}")
        return []

def map_evidences_and_urgency(enriched_rag_results: list[dict]) -> dict:
    """
    Maps clinical statements and enriched RAG candidates to DDXPlus evidence expressions.
    Returns evidences list, initial_evidence string, and urgency int.
    Uses exactly one LLM call.
    """
    with open(MAPPING_PROMPT_PATH, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
        
    input_data = json.dumps(enriched_rag_results, indent=2)
    prompt = f"{prompt_template}\n\n--------------------------------------------------\nINPUT:\n{input_data}"
    
    client = _get_gemini_client()
    try:
        response = _generate_with_retry(
            client,
            model='gemini-3.5-flash',
            prompt=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.0
            )
        )
    except Exception as e:
        logger.error(f"Error calling Gemini in map_evidences_and_urgency: {e}")
        raise RuntimeError(f"LLM mapping failed: {e}")
    
    try:
        result = json.loads(response.text)
        return {
            "evidences": result.get("evidences", []),
            "initial_evidence": result.get("initial_evidence", ""),
            "urgency": result.get("urgency", 5)
        }
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in map_evidences_and_urgency: {e}")
        return {"evidences": [], "initial_evidence": "", "urgency": 5}

