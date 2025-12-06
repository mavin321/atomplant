import os
from functools import lru_cache


class Settings:
    """Simple settings holder with sane defaults for local dev."""

    def __init__(self) -> None:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        self.app_port: int = int(os.getenv("APP_PORT", "8000"))
        self.log_level: str = os.getenv("LOG_LEVEL", "info")
        self.c_engine_lib_path: str = os.getenv("C_ENGINE_LIB_PATH", self._default_lib_path(project_root))
        self.allowed_origins: list[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

    @staticmethod
    def _default_lib_path(project_root: str) -> str:
        # Prefer platform-appropriate extension, but keep a deterministic fallback.
        candidates = ["libcengine.dll", "libcengine.so"] if os.name == "nt" else ["libcengine.so"]
        for name in candidates:
            candidate = os.path.join(project_root, "c_engine", name)
            if os.path.exists(candidate):
                return candidate
        return os.path.join(project_root, "c_engine", candidates[0])


@lru_cache()
def get_settings() -> Settings:
    return Settings()
