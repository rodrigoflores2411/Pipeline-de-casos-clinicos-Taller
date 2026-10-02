from pipeline.models import CanonicalCase

def case_summary(case: CanonicalCase) -> dict:
    return {
        "case_id": case.case_id,
        "public": {
            "age": case.initial_presentation.demographics.get("age"),
            "sex": case.initial_presentation.demographics.get("sex"),
            "chief_complaint": case.initial_presentation.chief_complaint,
        },
        "on_request": {
            "symptoms": len(case.patient.symptoms),
            "history": len(case.patient.history),
            "allergies": len(case.patient.allergies),
            "laboratory_tests": len(case.laboratory.tests),
            "radiology_studies": len(case.radiology.studies),
            "specialist_consultations": len(case.specialist.consultations),
        },
        "protected": {
            "diagnosis_present": bool(case.protected_evaluation.diagnosis),
            "diagnosis_synonyms": len(case.protected_evaluation.diagnosis_synonyms),
            "reference_treatment_present": bool(case.protected_evaluation.reference_treatment),
        },
        "reveal_rules": len(case.reveal_policy),
    }

def format_summary(summary: dict) -> str:
    p, o, pr = summary["public"], summary["on_request"], summary["protected"]
    return "\n".join([
        "",
        "=== RESUMEN DEL CASO ===",
        f"Caso: {summary['case_id']}",
        "",
        "PUBLIC / INITIAL",
        f"- Edad: {p['age'] if p['age'] is not None else 'No registrada'}",
        f"- Sexo: {p['sex'] if p['sex'] is not None else 'No registrado'}",
        f"- Motivo de consulta: {p['chief_complaint'] or 'No registrado'}",
        "",
        "ON_REQUEST",
        f"- Síntomas: {o['symptoms']}",
        f"- Antecedentes: {o['history']}",
        f"- Alergias: {o['allergies']}",
        f"- Laboratorio: {o['laboratory_tests']}",
        f"- Radiología: {o['radiology_studies']}",
        f"- Especialistas: {o['specialist_consultations']}",
        f"- Políticas de revelación: {summary['reveal_rules']}",
        "",
        "PROTECTED",
        f"- Diagnóstico protegido: {'Sí' if pr['diagnosis_present'] else 'No'}",
        f"- Sinónimos protegidos: {pr['diagnosis_synonyms']}",
        f"- Tratamiento protegido: {'Sí' if pr['reference_treatment_present'] else 'No'}",
        "",
        "Estado de aislamiento: SEGURO",
    ])
