import ctypes
import logging
import os
from dataclasses import dataclass
from typing import Optional

from app.core.config import get_settings
from app.models.molecule import ThermoProperties

logger = logging.getLogger(__name__)


@dataclass
class CThermoResult(ctypes.Structure):
    _fields_ = [
        ("cp", ctypes.c_double),
        ("hf", ctypes.c_double),
        ("density", ctypes.c_double),
        ("boiling_point", ctypes.c_double),
        ("vapor_pressure", ctypes.c_double),
        ("error_code", ctypes.c_int),
    ]


class CEngine:
    """Thin wrapper around the compiled C shared library."""

    def __init__(self, lib_path: Optional[str] = None) -> None:
        settings = get_settings()
        configured_path = lib_path or settings.c_engine_lib_path
        self.lib_path = self._resolve_path(configured_path)
        logger.info("Loading C engine library from %s", self.lib_path)
        self.lib = ctypes.CDLL(self.lib_path)
        # configure arg/return types
        self.lib.compute_thermo.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_double]
        self.lib.compute_thermo.restype = CThermoResult

    def compute_thermo(self, smiles: str, temperature: float, pressure: float) -> ThermoProperties:
        # Ensure null-terminated bytes
        encoded = smiles.encode("utf-8")
        result = self.lib.compute_thermo(encoded, ctypes.c_double(temperature), ctypes.c_double(pressure))
        if result.error_code != 0:
            raise ValueError(f"C engine failed to compute thermo properties (code={result.error_code})")
        return ThermoProperties(
            cp_J_per_molK=result.cp,
            hf_formation_kJ_per_mol=result.hf,
            density_kg_per_m3=result.density,
            boiling_point_K=result.boiling_point,
            vapor_pressure_bar=result.vapor_pressure,
        )

    def _resolve_path(self, configured_path: str) -> str:
        if os.path.exists(configured_path):
            return configured_path
        base_dir = os.path.dirname(configured_path)
        alt = "libcengine.dll" if configured_path.endswith(".so") else "libcengine.so"
        alt_path = os.path.join(base_dir, alt)
        if os.path.exists(alt_path):
            logger.warning("Configured C engine path not found; using alternate %s", alt_path)
            return alt_path
        raise FileNotFoundError(f"C engine shared library not found at {configured_path} or {alt_path}")


# Lazily instantiate to avoid issues on import when the library is missing
_engine: Optional[CEngine] = None


def get_engine() -> CEngine:
    global _engine
    if _engine is None:
        _engine = CEngine()
    return _engine
