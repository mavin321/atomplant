# C computation engine

Lightweight C layer providing deterministic surrogate thermo and transport calculations consumed by FastAPI via `ctypes`.

## Build

```bash
cd c_engine
make
```

Produces `libcengine.so` in this directory. Set `C_ENGINE_LIB_PATH` to point to that file for the backend.

On Windows without WSL, you can build a DLL with MinGW (if available):

```powershell
gcc -O2 -shared -I include src/properties.c src/reactor_models.c src/util.c -o libcengine.dll
```

Then set `C_ENGINE_LIB_PATH` to the Windows path, e.g. `C:\Users\admin\python\atomplant\c_engine\libcengine.dll`.

## Notes

- All computations are placeholders; replace with real correlations or calls into process simulators later.
- The interface is intentionally minimal to keep the Python FFI stable.
