from __future__ import annotations
import argparse, json
from pathlib import Path

from pipeline.processor import process_records
from pipeline.models import CanonicalCase
from pipeline.validators.structural import validate_structural
from pipeline.validators.semantic import validate_semantic
from pipeline.inspector import case_summary, format_summary

def load_records(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "records" in data:
        return data["records"]
    raise ValueError("El archivo debe ser una lista JSON o contener 'records'.")

def cmd_convert(args):
    m = process_records(args.adapter, load_records(args.input),
                        args.processed, args.rejected, args.report)
    print(json.dumps(m.row(), ensure_ascii=False, indent=2))

def cmd_validate(args):
    files = sorted(Path(args.input).glob("*.json"))
    invalid = 0
    for p in files:
        try:
            case = CanonicalCase.model_validate_json(p.read_text(encoding="utf-8"))
            errs = validate_structural(case) + validate_semantic(case)
            if errs:
                invalid += 1
                print(f"[INVALID] {p.name}: {errs}")
            else:
                print(f"[OK] {p.name}")
        except Exception as exc:
            invalid += 1
            print(f"[INVALID] {p.name}: {exc}")
    print(f"Total: {len(files)} | válidos: {len(files)-invalid} | inválidos: {invalid}")
    raise SystemExit(1 if invalid else 0)

def ask_many(title):
    print(f"\n{title} (vacío para terminar)")
    out, i = [], 1
    while True:
        v = input(f"{title} {i}: ").strip()
        if not v:
            return out
        out.append(v)
        i += 1

def yesno(prompt):
    while True:
        v = input(f"{prompt} [s/n]: ").strip().lower()
        if v in {"s","si","sí"}: return True
        if v in {"n","no"}: return False
        print("Responde s o n.")

def cmd_interactive(args):
    print("\n=== NUEVO CASO CLÍNICO ===")
    print("Pipeline ETL + Quality Gates\n")

    sid = input("ID del caso: ").strip() or "INTERACTIVE-001"
    age_s = input("Edad: ").strip()
    age = int(age_s) if age_s else None
    sex = input("Sexo: ").strip() or None
    specialty = input("Especialidad: ").strip() or None
    difficulty = input("Dificultad: ").strip() or None
    chief = input("Motivo de consulta: ").strip() or None

    symptoms = ask_many("Síntoma")
    history = ask_many("Antecedente")
    allergies = ask_many("Alergia")

    laboratory = []
    while yesno("\n¿Agregar laboratorio?"):
        laboratory.append({
            "name": input("  Prueba: ").strip(),
            "value": input("  Valor: ").strip(),
            "unit": input("  Unidad: ").strip() or None,
        })

    radiology = []
    while yesno("\n¿Agregar radiología?"):
        radiology.append({
            "name": input("  Estudio: ").strip(),
            "finding": input("  Hallazgo: ").strip(),
        })

    specialist = []
    while yesno("\n¿Agregar especialista?"):
        specialist.append({
            "name": input("  Especialidad: ").strip(),
            "text": input("  Nota: ").strip(),
        })

    print("\n=== DATOS PROTEGIDOS ===")
    diagnosis = input("Diagnóstico correcto: ").strip()
    synonyms = ask_many("Sinónimo")
    treatment = input("Tratamiento/solución de referencia (opcional): ").strip() or None

    record = {
        "source_dataset": "manual",
        "source_id": sid,
        "specialty": specialty,
        "difficulty": difficulty,
        "age": age,
        "sex": sex,
        "chief_complaint": chief,
        "symptoms": symptoms,
        "history": history,
        "allergies": allergies,
        "laboratory": laboratory,
        "radiology": radiology,
        "specialist": specialist,
        "diagnosis": diagnosis,
        "diagnosis_synonyms": synonyms,
        "reference_treatment": treatment,
        "original_answer": diagnosis,
    }

    Path(args.temp_input).parent.mkdir(parents=True, exist_ok=True)
    Path(args.temp_input).write_text(json.dumps([record], ensure_ascii=False, indent=2), encoding="utf-8")

    print("\nProcesando caso...")
    m = process_records("manual", [record], args.processed, args.rejected, args.report)
    print(json.dumps(m.row(), ensure_ascii=False, indent=2))

    processed = Path(args.processed) / f"MANUAL-{sid}.json"
    if processed.exists():
        case = CanonicalCase.model_validate_json(processed.read_text(encoding="utf-8"))
        print("\n[OK] Estructura válida")
        print("[OK] Diagnóstico aislado")
        print("[OK] Evidence IDs generados")
        print("[OK] Reveal policies generadas")
        print(f"\nCaso guardado: {processed}")
        print(format_summary(case_summary(case)))
        if yesno("\n¿Mostrar JSON generado?"):
            print(processed.read_text(encoding="utf-8"))
        if yesno("\n¿Mostrar métricas?"):
            print(Path(args.report).read_text(encoding="utf-8-sig"))
        return

    rejected = Path(args.rejected) / f"{sid}.json"
    print("\n[REJECTED] El caso no superó los Quality Gates.")
    if rejected.exists():
        print(rejected.read_text(encoding="utf-8"))
    raise SystemExit(1)

def cmd_inspect(args):
    path = Path(args.case)
    case = CanonicalCase.model_validate_json(path.read_text(encoding="utf-8"))
    errs = validate_structural(case) + validate_semantic(case)
    print(format_summary(case_summary(case)))
    print("\nQUALITY GATES")
    if errs:
        print("Estado: INVALID")
        for e in errs:
            print("-", e)
        raise SystemExit(1)
    print("Estado: VALID")
    print("- Esquema canónico: OK")
    print("- Diagnóstico protegido: OK")
    print("- Evidence IDs: OK")
    print("- Reveal policies: OK")

def main():
    p = argparse.ArgumentParser(description="Pipeline ETL + Quality Gates")
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("convert")
    c.add_argument("--adapter", choices=["manual","medqa"], default="manual")
    c.add_argument("--input", required=True)
    c.add_argument("--processed", default="data/processed")
    c.add_argument("--rejected", default="data/rejected")
    c.add_argument("--report", default="reports/conversion_metrics.csv")
    c.set_defaults(func=cmd_convert)

    v = sub.add_parser("validate")
    v.add_argument("--input", default="data/processed")
    v.set_defaults(func=cmd_validate)

    i = sub.add_parser("interactive")
    i.add_argument("--processed", default="data/processed")
    i.add_argument("--rejected", default="data/rejected")
    i.add_argument("--report", default="reports/interactive_metrics.csv")
    i.add_argument("--temp-input", default="data/raw/interactive_last_case.json")
    i.set_defaults(func=cmd_interactive)

    ins = sub.add_parser("inspect")
    ins.add_argument("--case", required=True)
    ins.set_defaults(func=cmd_inspect)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
