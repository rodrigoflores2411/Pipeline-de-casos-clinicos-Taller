from pipeline.normalizer import normalize_unit, normalize_test

def test_units():
    assert normalize_unit("mg/dl") == "mg/dL"
    assert normalize_unit("ng/ml") == "ng/mL"

def test_test_name():
    code, label = normalize_test("Troponina T")
    assert code == "troponin_t"
    assert label == "Troponina T"
