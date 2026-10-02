from pipeline.models import CanonicalCase
from pipeline.processor import process_records
from pipeline.inspector import case_summary, format_summary

def test_inspector_hides_protected_value(tmp_path):
    records = [{
        "source_dataset":"manual",
        "source_id":"inspect",
        "chief_complaint":"Dolor torácico",
        "diagnosis":"Diagnóstico secreto",
        "diagnosis_synonyms":["Sinónimo secreto"]
    }]
    process_records("manual", records, tmp_path/"p", tmp_path/"r", tmp_path/"m.csv")
    path = next((tmp_path/"p").glob("*.json"))
    case = CanonicalCase.model_validate_json(path.read_text(encoding="utf-8"))
    text = format_summary(case_summary(case))
    assert "Diagnóstico secreto" not in text
    assert "Sinónimo secreto" not in text
    assert "Diagnóstico protegido: Sí" in text
