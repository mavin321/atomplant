# Atom-to-Plant AI Pipeline

End-to-end demo showing a molecular-to-reactor heuristic pipeline. React frontend drives a FastAPI backend that calls a lightweight C shared library for thermo surrogates.

## Stack

- Frontend: React + TypeScript (Vite), fetch-based client.
- Backend: FastAPI, Pydantic, pytest.
- C engine: GCC-built shared library loaded via `ctypes`.

## Quick start

1) Build the C engine

```bash
cd c_engine
make
cd ..
```

2) Run backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\activate ./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
# Linux/macOS
export C_ENGINE_LIB_PATH="$(pwd)/../c_engine/libcengine.so"
# Windows PowerShell (no WSL)
# $env:C_ENGINE_LIB_PATH="C:\\Users\\admin\\python\\atomplant\\c_engine\\libcengine.dll"
uvicorn app.main:app --reload --port 8000
```

3) Run frontend (new terminal)

```bash
cd frontend
npm install
npm run dev -- --host --port 3000
```

4) Open `http://localhost:3000`, enter a SMILES (e.g., `CCO` for ethanol), and run the pipeline.

## Configuration

- Backend env vars: `APP_PORT`, `LOG_LEVEL`, `C_ENGINE_LIB_PATH`, `ALLOWED_ORIGINS`.
- Frontend env: `VITE_API_BASE_URL` (defaults to `http://localhost:8000`).

## Where to plug real models

- `c_engine/src/properties.c`: replace deterministic surrogates with real thermo estimators or simulator bindings.
- `backend/app/services/pipeline_service.py`: swap heuristics for ML models, kinetic solvers, and equipment sizing routines.
- `frontend/src/components/*`: add charts/visuals for richer results.

## Testing

- Backend: `cd backend && pytest`
- C engine: `cd c_engine && make clean && make`
- Frontend: `cd frontend && npm run build`

## Notes

All calculations are deterministic placeholders to keep the interface stable for future integration with proper physical/ML models.
