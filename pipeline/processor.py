import json
from pathlib import Path
from pydantic import ValidationError
from pipeline.adapters import ADAPTERS
from pipeline.normalizer import normalize_raw_case
from pipeline.segmenter import segment_case
from pipeline.reveal_policy import build_reveal_policy
from pipeline.validators.structural import validate_structural
from pipeline.validators.semantic import validate_semantic
from pipeline.metrics import RunMetrics, write_metrics

def process_records(adapter_name, records, processed_dir, rejected_dir, report_path):
    adapter = ADAPTERS[adapter_name]()
    processed_dir = Path(processed_dir)
    rejected_dir = Path(rejected_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)
    rejected_dir.mkdir(parents=True, exist_ok=True)

    metrics = RunMetrics(input_records=len(records))

    for idx, record in enumerate(records,1):
        source_id = str(record.get("source_id", record.get("id", idx)))
        try:
            raw = adapter.parse_record(record)
            raw = normalize_raw_case(raw)
            case = segment_case(raw)
            case.reveal_policy = build_reveal_policy(case)
            metrics.schema_valid += 1

            errors = validate_structural(case) + validate_semantic(case)
            for e in errors:
                if e == "duplicate_evidence_id":
                    metrics.duplicate_evidence_ids += 1
                elif e.startswith("missing_reveal_policy:"):
                    metrics.missing_reveal_policy_count += 1
                elif e.startswith("protected_term_exposed:"):
                    metrics.protected_leak_count += 1

            if errors:
                (rejected_dir/f"{source_id}.json").write_text(
                    json.dumps({"source_id":source_id,"errors":errors}, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
                metrics.rejected += 1
                continue

            (processed_dir/f"{case.case_id}.json").write_text(
                case.model_dump_json(indent=2), encoding="utf-8"
            )
            metrics.accepted += 1

        except (ValidationError, ValueError, TypeError, KeyError) as exc:
            (rejected_dir/f"{source_id}.json").write_text(
                json.dumps({"source_id":source_id,"errors":[f"{type(exc).__name__}: {exc}"]},
                           ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            metrics.rejected += 1

    write_metrics(Path(report_path), metrics)
    return metrics
