from pipeline.models import CanonicalCase

def collect_ids(case: CanonicalCase):
    ids = []
    ids += [x.evidence_id for x in case.patient.symptoms]
    ids += [x.evidence_id for x in case.patient.history]
    ids += [x.evidence_id for x in case.patient.allergies]
    ids += [x.evidence_id for x in case.laboratory.tests]
    ids += [x.evidence_id for x in case.radiology.studies]
    ids += [x.evidence_id for x in case.specialist.consultations]
    return ids

def validate_structural(case: CanonicalCase):
    errors = []
    ids = collect_ids(case)
    if len(ids) != len(set(ids)):
        errors.append("duplicate_evidence_id")
    for eid in ids:
        if eid not in case.reveal_policy:
            errors.append(f"missing_reveal_policy:{eid}")
    return errors
