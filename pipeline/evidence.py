from pipeline.models import EvidenceFact

def evidence_id(case_id, section, code):
    return f"{case_id}.{section}.{code}"

def text_fact(case_id, section, code, label, text):
    return EvidenceFact(
        evidence_id=evidence_id(case_id, section, code),
        code=code,
        label=label,
        text=text,
    )

def value_fact(case_id, section, code, label, value, unit=None):
    return EvidenceFact(
        evidence_id=evidence_id(case_id, section, code),
        code=code,
        label=label,
        value=value,
        unit=unit,
    )
