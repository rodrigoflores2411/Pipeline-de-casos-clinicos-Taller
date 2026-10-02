import json
from pipeline.models import CanonicalCase

def norm(s: str):
    return " ".join(s.lower().split())

def validate_semantic(case: CanonicalCase):
    errors = []
    public = {
        "initial_presentation": case.initial_presentation.model_dump(),
        "patient": case.patient.model_dump(),
        "laboratory": case.laboratory.model_dump(),
        "radiology": case.radiology.model_dump(),
        "specialist": case.specialist.model_dump(),
    }
    public_text = norm(json.dumps(public, ensure_ascii=False))
    terms = [case.protected_evaluation.diagnosis, *case.protected_evaluation.diagnosis_synonyms]
    for term in terms:
        if term and norm(term) in public_text:
            errors.append(f"protected_term_exposed:{term}")
    return errors
