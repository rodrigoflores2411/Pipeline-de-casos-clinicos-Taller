from .manual import ManualAdapter
from .medqa import MedQAAdapter

ADAPTERS = {
    "manual": ManualAdapter,
    "medqa": MedQAAdapter,
}
