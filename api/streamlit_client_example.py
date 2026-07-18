"""
Minimal example of how your Streamlit app calls the DDX API.
Assumes your LLM layer has already turned the conversation into a
structured evidence list matching the DDXPlus evidence codes
(GET /evidences on the API gives the LLM the valid codes/questions/values
to extract into).
"""
import requests
import streamlit as st

API_URL = "http://localhost:8000"  # swap for your deployed API URL

def get_prediction(age: int, sex: str, evidences: list[str], initial_evidence: str | None = None):
    resp = requests.post(
        f"{API_URL}/predict",
        json={
            "age": age,
            "sex": sex,
            "evidences": evidences,
            "initial_evidence": initial_evidence,
            "top_k": 3,
        },
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()

# --- Example usage inside your Streamlit page ---
# result = get_prediction(age=45, sex="F", evidences=extracted_evidence_list, initial_evidence=chief_complaint_code)
# st.write(f"Top prediction: {result['top_prediction']['pathology']} ({result['top_prediction']['probability']:.1%})")
# for d in result['differential']:
#     st.write(f"- {d['pathology']}: {d['probability']:.1%}")
# if result['unrecognized_evidences']:
#     st.warning(f"LLM produced unrecognized evidence codes: {result['unrecognized_evidences']}")
