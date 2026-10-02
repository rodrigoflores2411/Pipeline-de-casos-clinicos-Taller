from dataclasses import dataclass, asdict
from pathlib import Path
import csv

@dataclass
class RunMetrics:
    input_records: int = 0
    accepted: int = 0
    rejected: int = 0
    schema_valid: int = 0
    protected_leak_count: int = 0
    duplicate_evidence_ids: int = 0
    missing_reveal_policy_count: int = 0

    def row(self):
        total = max(self.input_records,1)
        d = asdict(self)
        d["conversion_success_rate_pct"] = round(100*self.accepted/total,2)
        d["schema_valid_rate_pct"] = round(100*self.schema_valid/total,2)
        return d

def write_metrics(path: Path, metrics: RunMetrics):
    path.parent.mkdir(parents=True, exist_ok=True)
    row = metrics.row()
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=row.keys())
        w.writeheader()
        w.writerow(row)
