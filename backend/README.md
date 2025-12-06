# Backend (FastAPI)

This service exposes the Atom-to-Plant pipeline API.

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows
pip install -r requirements.txt
# Linux/macOS
export C_ENGINE_LIB_PATH="$(pwd)/../c_engine/libcengine.so"
# Windows PowerShell (no WSL)
# $env:C_ENGINE_LIB_PATH="C:\\Users\\admin\\python\\atomplant\\c_engine\\libcengine.dll"
uvicorn app.main:app --reload --port 8000
```

## Env vars

- `APP_PORT` (default `8000`)
- `LOG_LEVEL` (default `info`)
- `C_ENGINE_LIB_PATH` path to `libcengine.so`
- `ALLOWED_ORIGINS` comma-separated origins for CORS

## Tests

```bash
pytest
```
