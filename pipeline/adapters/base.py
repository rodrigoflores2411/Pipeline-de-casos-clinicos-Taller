from abc import ABC, abstractmethod
from typing import Any
from pipeline.models import RawClinicalCase

class BaseAdapter(ABC):
    @abstractmethod
    def parse_record(self, record: dict[str, Any]) -> RawClinicalCase:
        raise NotImplementedError
