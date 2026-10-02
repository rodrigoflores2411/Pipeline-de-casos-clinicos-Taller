import json
from pipeline.processor import process_records

def valid():
    return [{
        "source_dataset":"manual",
        "source_id":"001",
        "age":58,
        "sex":"Masculino",
        "chief_complaint":"Dolor torácico",
        "symptoms":["Dolor 8/10"],
        "laboratory":[{"name":"Troponina T","value":1.8,"unit":"ng/ml"}],
        "diagnosis":"Infarto inferior",
        "diagnosis_synonyms":["IAM inferior"]
    }]

def test_valid_case(tmp_path):
    m = process_records("manual", valid(), tmp_path/"p", tmp_path/"r", tmp_path/"m.csv")
    assert m.accepted == 1
    assert m.rejected == 0

def test_diagnosis_is_protected(tmp_path):
    process_records("manual", valid(), tmp_path/"p", tmp_path/"r", tmp_path/"m.csv")
    f = next((tmp_path/"p").glob("*.json"))
    data = json.loads(f.read_text(encoding="utf-8"))
    public = json.dumps({
        "initial":data["initial_presentation"],
        "patient":data["patient"],
        "laboratory":data["laboratory"],
        "radiology":data["radiology"],
        "specialist":data["specialist"],
    }, ensure_ascii=False)
    assert "Infarto inferior" not in public
    assert data["protected_evaluation"]["diagnosis"] == "Infarto inferior"

def test_policy_exists(tmp_path):
    process_records("manual", valid(), tmp_path/"p", tmp_path/"r", tmp_path/"m.csv")
    f = next((tmp_path/"p").glob("*.json"))
    data = json.loads(f.read_text(encoding="utf-8"))
    eid = data["laboratory"]["tests"][0]["evidence_id"]
    assert eid in data["reveal_policy"]
