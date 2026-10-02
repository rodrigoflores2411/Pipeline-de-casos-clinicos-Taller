from pipeline.models import RawClinicalCase

UNIT_MAP = {
    "mg / dl": "mg/dL",
    "mg/dl": "mg/dL",
    "ng / ml": "ng/mL",
    "ng/ml": "ng/mL",
}
TEST_MAP = {
    "troponina t": ("troponin_t", "Troponina T"),
    "troponin t": ("troponin_t", "Troponina T"),
    "ctnt": ("troponin_t", "Troponina T"),
    "glucosa": ("glucose", "Glucosa"),
    "glucose": ("glucose", "Glucosa"),
}

def normalize_unit(unit):
    if unit is None:
        return None
    u = unit.strip()
    return UNIT_MAP.get(u.lower(), u)

def normalize_test(name: str):
    key = name.strip().lower()
    if key in TEST_MAP:
        return TEST_MAP[key]
    code = "".join(ch if ch.isalnum() else "_" for ch in key).strip("_")
    while "__" in code:
        code = code.replace("__", "_")
    return code, name.strip()

def normalize_raw_case(raw: RawClinicalCase) -> RawClinicalCase:
    lab = []
    for item in raw.laboratory:
        item = dict(item)
        name = str(item.get("name") or item.get("label") or item.get("code") or "test")
        code, label = normalize_test(name)
        item["code"] = code
        item["label"] = label
        item["unit"] = normalize_unit(item.get("unit"))
        lab.append(item)
    return raw.model_copy(update={
        "laboratory": lab,
        "sex": raw.sex.strip().lower() if isinstance(raw.sex, str) else raw.sex,
        "diagnosis": raw.diagnosis.strip(),
        "diagnosis_synonyms": [x.strip() for x in raw.diagnosis_synonyms if x.strip()],
    })
