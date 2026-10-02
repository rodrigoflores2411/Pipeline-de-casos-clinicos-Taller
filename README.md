# Pipeline real de conversión de casos clínicos

Metodología: ETL + Quality Gates.

## Flujo
1. Extract: adaptador de fuente.
2. Transform: normalización y segmentación PUBLIC / ON_REQUEST / PROTECTED.
3. Quality Gates: validación estructural y semántica.
4. Load: casos válidos a `data/processed`, inválidos a `data/rejected`.
5. Measure: métricas CSV por corrida.

## Instalación
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Verificación
```powershell
python -m compileall pipeline
python -m pytest -q
```

## Ejecutar pipeline
```powershell
python -m pipeline.cli convert --adapter manual --input data/raw/manual_cases.json
python -m pipeline.cli validate --input data/processed
```

## Casos de prueba adicionales
```powershell
python -m pipeline.cli convert --adapter manual --input data/raw/invalid_cases.json
python -m pipeline.cli convert --adapter manual --input data/raw/leaky_cases.json
```

Los casos inválidos se almacenan en `data/rejected/` con las causas.


## V2 - modo interactivo

```powershell
python -m pipeline.cli interactive
```

## V2 - inspección segura

```powershell
python -m pipeline.cli inspect --case data/processed/MANUAL-CARD-001.json
```

`inspect` muestra PUBLIC / ON_REQUEST / PROTECTED sin imprimir el valor del diagnóstico.
