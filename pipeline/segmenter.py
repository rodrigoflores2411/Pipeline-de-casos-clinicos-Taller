from pipeline.models import *
from pipeline.evidence import text_fact, value_fact

def slug(text: str, fallback: str):
    s = "".join(ch if ch.isalnum() else "_" for ch in text.lower()).strip("_")
    while "__" in s:
        s = s.replace("__", "_")
    return s[:40] or fallback

def segment_case(raw: RawClinicalCase) -> CanonicalCase:
    case_id = f"{raw.source_dataset.upper()}-{raw.source_id}"

    initial = InitialPresentation(
        demographics={k:v for k,v in {"age":raw.age, "sex":raw.sex}.items() if v is not None},
        chief_complaint=raw.chief_complaint,
    )

    patient = PatientSection(
        symptoms=[text_fact(case_id,"patient.symptoms",f"symptom_{i:02d}","Síntoma",t)
                  for i,t in enumerate(raw.symptoms,1)],
        history=[text_fact(case_id,"patient.history",f"history_{i:02d}","Antecedente",t)
                 for i,t in enumerate(raw.history,1)],
        allergies=[text_fact(case_id,"patient.allergies",f"allergy_{i:02d}","Alergia",t)
                   for i,t in enumerate(raw.allergies,1)],
    )

    lab = []
    for item in raw.laboratory:
        name = str(item.get("label") or item.get("name") or "test")
        code = str(item.get("code") or slug(name,"test"))
        lab.append(value_fact(case_id,"laboratory",code,name,item.get("value"),item.get("unit")))

    rad = []
    for i,item in enumerate(raw.radiology,1):
        name = str(item.get("name") or item.get("label") or f"study_{i}")
        code = str(item.get("code") or slug(name,f"study_{i}"))
        rad.append(text_fact(case_id,"radiology",code,name,str(item.get("finding") or item.get("text") or "")))

    spec = []
    for i,item in enumerate(raw.specialist,1):
        name = str(item.get("name") or item.get("label") or f"consult_{i}")
        code = str(item.get("code") or slug(name,f"consult_{i}"))
        spec.append(text_fact(case_id,"specialist",code,name,str(item.get("text") or item.get("finding") or "")))

    return CanonicalCase(
        case_id=case_id,
        source=SourceInfo(dataset=raw.source_dataset, source_id=raw.source_id),
        metadata=Metadata(specialty=raw.specialty, difficulty=raw.difficulty),
        initial_presentation=initial,
        patient=patient,
        laboratory=LaboratorySection(tests=lab),
        radiology=RadiologySection(studies=rad),
        specialist=SpecialistSection(consultations=spec),
        protected_evaluation=ProtectedEvaluation(
            diagnosis=raw.diagnosis,
            diagnosis_synonyms=raw.diagnosis_synonyms,
            reference_treatment=raw.reference_treatment,
            original_answer=raw.original_answer,
        )
    )
