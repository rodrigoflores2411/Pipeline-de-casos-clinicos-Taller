from pipeline.processor import process_records

def test_missing_diagnosis_rejected(tmp_path):
    records = [{
        "source_dataset":"manual",
        "source_id":"bad",
        "chief_complaint":"Caso incompleto"
    }]
    m = process_records("manual", records, tmp_path/"p", tmp_path/"r", tmp_path/"m.csv")
    assert m.accepted == 0
    assert m.rejected == 1

def test_public_diagnosis_rejected(tmp_path):
    records = [{
        "source_dataset":"manual",
        "source_id":"leak",
        "chief_complaint":"Paciente con Neumonía adquirida en la comunidad",
        "diagnosis":"Neumonía adquirida en la comunidad"
    }]
    m = process_records("manual", records, tmp_path/"p", tmp_path/"r", tmp_path/"m.csv")
    assert m.accepted == 0
    assert m.rejected == 1
    assert m.protected_leak_count >= 1
