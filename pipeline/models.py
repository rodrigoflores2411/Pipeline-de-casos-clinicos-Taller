from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, Field

class SourceInfo(BaseModel):
    dataset: str
    source_id: str

class Metadata(BaseModel):
    specialty: str | None = None
    difficulty: str | None = None

class EvidenceFact(BaseModel):
    evidence_id: str
    code: str
    label: str
    value: Any | None = None
    unit: str | None = None
    text: str | None = None

class InitialPresentation(BaseModel):
    demographics: dict[str, Any] = Field(default_factory=dict)
    chief_complaint: str | None = None
    facts: list[EvidenceFact] = Field(default_factory=list)

class PatientSection(BaseModel):
    symptoms: list[EvidenceFact] = Field(default_factory=list)
    history: list[EvidenceFact] = Field(default_factory=list)
    allergies: list[EvidenceFact] = Field(default_factory=list)

class LaboratorySection(BaseModel):
    tests: list[EvidenceFact] = Field(default_factory=list)

class RadiologySection(BaseModel):
    studies: list[EvidenceFact] = Field(default_factory=list)

class SpecialistSection(BaseModel):
    consultations: list[EvidenceFact] = Field(default_factory=list)

class RevealRule(BaseModel):
    owner: Literal["patient", "assistant", "laboratory", "radiologist", "specialist"]
    mode: Literal["initial", "on_request", "after_order", "after_consult"]
    intents: list[str] = Field(default_factory=list)
    requires: dict[str, Any] = Field(default_factory=dict)

class ProtectedEvaluation(BaseModel):
    diagnosis: str
    diagnosis_synonyms: list[str] = Field(default_factory=list)
    reference_treatment: str | None = None
    original_answer: str | None = None

class ConversionMetadata(BaseModel):
    pipeline_version: str = "1.0"
    status: Literal["accepted", "rejected"] = "accepted"
    warnings: list[str] = Field(default_factory=list)

class CanonicalCase(BaseModel):
    schema_version: str = "1.0"
    case_id: str
    source: SourceInfo
    metadata: Metadata = Field(default_factory=Metadata)
    initial_presentation: InitialPresentation
    patient: PatientSection = Field(default_factory=PatientSection)
    laboratory: LaboratorySection = Field(default_factory=LaboratorySection)
    radiology: RadiologySection = Field(default_factory=RadiologySection)
    specialist: SpecialistSection = Field(default_factory=SpecialistSection)
    reveal_policy: dict[str, RevealRule] = Field(default_factory=dict)
    protected_evaluation: ProtectedEvaluation
    conversion_metadata: ConversionMetadata = Field(default_factory=ConversionMetadata)

class RawClinicalCase(BaseModel):
    source_dataset: str
    source_id: str
    specialty: str | None = None
    difficulty: str | None = None
    age: int | None = None
    sex: str | None = None
    chief_complaint: str | None = None
    symptoms: list[str] = Field(default_factory=list)
    history: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    laboratory: list[dict[str, Any]] = Field(default_factory=list)
    radiology: list[dict[str, Any]] = Field(default_factory=list)
    specialist: list[dict[str, Any]] = Field(default_factory=list)
    diagnosis: str
    diagnosis_synonyms: list[str] = Field(default_factory=list)
    reference_treatment: str | None = None
    original_answer: str | None = None
