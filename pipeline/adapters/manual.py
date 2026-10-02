from typing import Any
from .base import BaseAdapter
from pipeline.models import RawClinicalCase

class ManualAdapter(BaseAdapter):
    def parse_record(self, record: dict[str, Any]) -> RawClinicalCase:
        return RawClinicalCase(**record)
