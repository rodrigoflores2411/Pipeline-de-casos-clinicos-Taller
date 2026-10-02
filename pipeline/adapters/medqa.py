from typing import Any
from .base import BaseAdapter
from pipeline.models import RawClinicalCase

class MedQAAdapter(BaseAdapter):
    def parse_record(self, record: dict[str, Any]) -> RawClinicalCase:
        answer = record.get("answer") or record.get("correct_answer")
        if not answer:
            raise ValueError("El registro no contiene respuesta/diagnóstico.")
        return RawClinicalCase(
            source_dataset="medqa",
            source_id=str(record.get("id", record.get("source_id", "unknown"))),
            specialty=record.get("specialty"),
            difficulty=record.get("difficulty"),
            chief_complaint=record.get("question"),
            diagnosis=str(answer),
            diagnosis_synonyms=list(record.get("diagnosis_synonyms", [])),
            original_answer=str(answer),
        )
