from pipeline.models import CanonicalCase, RevealRule

def build_reveal_policy(case: CanonicalCase):
    p = {}
    for fact in case.patient.symptoms + case.patient.history + case.patient.allergies:
        p[fact.evidence_id] = RevealRule(owner="patient", mode="on_request", intents=["ask_patient"])
    for fact in case.laboratory.tests:
        p[fact.evidence_id] = RevealRule(owner="laboratory", mode="after_order",
                                         intents=["request_lab"], requires={"test":fact.code})
    for fact in case.radiology.studies:
        p[fact.evidence_id] = RevealRule(owner="radiologist", mode="after_order",
                                         intents=["request_radiology"], requires={"study":fact.code})
    for fact in case.specialist.consultations:
        p[fact.evidence_id] = RevealRule(owner="specialist", mode="after_consult",
                                         intents=["request_specialist"], requires={"consultation":fact.code})
    return p
