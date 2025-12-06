from typing import List, Literal, Optional

from pydantic import BaseModel, Field, validator


class MoleculeInput(BaseModel):
    identifier: str = Field(..., description="SMILES or InChI")
    identifier_type: Literal["SMILES", "InChI"] = "SMILES"
    reaction_type: Optional[str] = Field(None, description="Reaction context e.g., substitution")
    temperature_K: Optional[float] = Field(None, ge=1.0)
    pressure_bar: Optional[float] = Field(None, ge=0.001)
    solvent: Optional[str] = None
    phase: Optional[Literal["liquid", "gas", "solid", "mixed"]] = "liquid"
    target_scale: Literal["lab", "pilot", "plant"] = "lab"

    @validator("identifier")
    def identifier_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("identifier must not be empty")
        return v.strip()


class ThermoProperties(BaseModel):
    cp_J_per_molK: float
    hf_formation_kJ_per_mol: float
    density_kg_per_m3: float
    boiling_point_K: float
    vapor_pressure_bar: float


class ReactionPathway(BaseModel):
    pathway_id: str
    description: str
    estimated_yield_percent: float
    hazard_score: float


class HeatMassTransfer(BaseModel):
    heat_transfer_coeff_W_per_m2K: float
    mass_transfer_coeff_m_per_s: float
    diffusion_coeff_m2_per_s: float


class PhaseEquilibria(BaseModel):
    k_value: float
    partition_coefficient_logP: float
    azeotrope_flag: bool


class EnvToxicityProfile(BaseModel):
    environmental_score: float
    toxicity_score: float
    notes: str


class ReactorDesign(BaseModel):
    reactor_type: Literal["CSTR", "PFR", "batch", "semi-batch"]
    volume_m3: float
    residence_time_s: float
    operating_temperature_K: float
    operating_pressure_bar: float


class SeparationUnit(BaseModel):
    unit_type: Literal["distillation", "extraction", "filtration", "absorption", "stripping"]
    description: str


class SeparationTrain(BaseModel):
    units: List[SeparationUnit]


class ScaleUpRisks(BaseModel):
    hot_spot_risk: float
    runaway_risk: float
    mixing_limitation_risk: float
    notes: str


class PipelineResult(BaseModel):
    thermo: ThermoProperties
    reaction_pathways: List[ReactionPathway]
    heat_mass_transfer: HeatMassTransfer
    phase_equilibria: PhaseEquilibria
    env_toxicity: EnvToxicityProfile
    reactor_design: ReactorDesign
    separation_train: SeparationTrain
    scaleup_risks: ScaleUpRisks
    raw_logs: Optional[List[str]] = None
