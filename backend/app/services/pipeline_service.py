import hashlib
import logging
from typing import List

from app.models.molecule import (
    EnvToxicityProfile,
    HeatMassTransfer,
    MoleculeInput,
    PhaseEquilibria,
    PipelineResult,
    ReactionPathway,
    ReactorDesign,
    ScaleUpRisks,
    SeparationTrain,
    SeparationUnit,
)
from app.services.c_interface import get_engine

logger = logging.getLogger(__name__)


def _deterministic_score(seed: str) -> float:
    digest = hashlib.sha256(seed.encode()).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


def _reaction_pathways(molecule: MoleculeInput) -> List[ReactionPathway]:
    base = molecule.reaction_type or "general"
    hazard_mod = _deterministic_score(molecule.identifier + base)
    return [
        ReactionPathway(
            pathway_id="pathway-1",
            description=f"{base} primary route",
            estimated_yield_percent=60 + 20 * hazard_mod,
            hazard_score=hazard_mod * 5,
        ),
        ReactionPathway(
            pathway_id="pathway-2",
            description=f"{base} side route",
            estimated_yield_percent=25 + 10 * (1 - hazard_mod),
            hazard_score=hazard_mod * 3,
        ),
    ]


def _heat_mass_transfer(molecule: MoleculeInput) -> HeatMassTransfer:
    phase_factor = {"liquid": 1.0, "gas": 0.8, "solid": 0.5, "mixed": 1.1}.get(molecule.phase or "liquid", 1.0)
    base = 200.0 * phase_factor
    diffusion = 1e-9 * (1.2 if molecule.phase == "gas" else 1.0)
    return HeatMassTransfer(
        heat_transfer_coeff_W_per_m2K=base,
        mass_transfer_coeff_m_per_s=0.01 * phase_factor,
        diffusion_coeff_m2_per_s=diffusion,
    )


def _phase_equilibria(thermo_cp: float) -> PhaseEquilibria:
    k_value = 0.5 + (thermo_cp % 50) / 200.0
    return PhaseEquilibria(
        k_value=k_value,
        partition_coefficient_logP=1.0 + (thermo_cp / 1000.0),
        azeotrope_flag=k_value < 0.6,
    )


def _env_toxicity_profile(molecule: MoleculeInput) -> EnvToxicityProfile:
    base = _deterministic_score(molecule.identifier)
    env = 0.3 + 0.5 * base
    tox = 0.2 + 0.6 * (1 - base)
    return EnvToxicityProfile(environmental_score=env, toxicity_score=tox, notes="Heuristic placeholder scores")


def _reactor_design(molecule: MoleculeInput, hazard: float, thermo_bp: float) -> ReactorDesign:
    scale_map = {"lab": 0.1, "pilot": 2.0, "plant": 20.0}
    base_vol = scale_map.get(molecule.target_scale, 0.5)
    reactor_type = "CSTR" if molecule.phase == "liquid" else "PFR"
    if hazard > 3.0 or thermo_bp < 350:
        reactor_type = "batch"
    return ReactorDesign(
        reactor_type=reactor_type,
        volume_m3=round(base_vol, 3),
        residence_time_s=3600 * (1.5 if reactor_type == "batch" else 1.0),
        operating_temperature_K=molecule.temperature_K or thermo_bp * 0.8,
        operating_pressure_bar=molecule.pressure_bar or (1.0 if thermo_bp > 350 else 2.0),
    )


def _separation_train(logp: float, boiling_point: float) -> SeparationTrain:
    units = [
        SeparationUnit(unit_type="distillation", description="Primary cut based on boiling point"),
    ]
    if logp > 2.0:
        units.append(SeparationUnit(unit_type="extraction", description="Solvent extraction for heavy organics"))
    if boiling_point < 320:
        units.append(SeparationUnit(unit_type="absorption", description="Off-gas polishing"))
    units.append(SeparationUnit(unit_type="filtration", description="Final solids removal"))
    return SeparationTrain(units=units)


def _scaleup_risks(hazard: float, phase: str, target_scale: str) -> ScaleUpRisks:
    phase_factor = {"gas": 0.7, "liquid": 1.0, "solid": 1.2, "mixed": 1.3}.get(phase, 1.0)
    hot_spot = min(1.0, hazard / 5 * phase_factor)
    runaway = min(1.0, (hazard / 4) * (1.2 if target_scale == "plant" else 0.9))
    mixing = min(1.0, 0.4 * phase_factor + (0.2 if target_scale != "lab" else 0.0))
    return ScaleUpRisks(
        hot_spot_risk=hot_spot,
        runaway_risk=runaway,
        mixing_limitation_risk=mixing,
        notes="Deterministic heuristic based on hazard and phase; replace with dynamic model later.",
    )


def run_pipeline(molecule: MoleculeInput) -> PipelineResult:
    logs: List[str] = []
    logger.info("Running pipeline for %s", molecule.identifier)
    engine = get_engine()
    temperature = molecule.temperature_K or 298.15
    pressure = molecule.pressure_bar or 1.0
    thermo = engine.compute_thermo(molecule.identifier, temperature, pressure)
    logs.append(f"Computed thermo via C engine at T={temperature}K, P={pressure}bar")

    pathways = _reaction_pathways(molecule)
    logs.append(f"Generated {len(pathways)} reaction pathways for context={molecule.reaction_type or 'general'}")

    hmt = _heat_mass_transfer(molecule)
    logs.append("Estimated heat/mass transfer coefficients")

    phase_eq = _phase_equilibria(thermo.cp_J_per_molK)
    logs.append("Calculated phase equilibria surrogate values")

    env_tox = _env_toxicity_profile(molecule)
    logs.append("Estimated environment/toxicity profile")

    hazard = max(p.hazard_score for p in pathways)
    reactor = _reactor_design(molecule, hazard, thermo.boiling_point_K)
    logs.append(f"Selected reactor type {reactor.reactor_type}")

    sep = _separation_train(phase_eq.partition_coefficient_logP, thermo.boiling_point_K)
    logs.append(f"Built separation train with {len(sep.units)} units")

    risks = _scaleup_risks(hazard, molecule.phase or "liquid", molecule.target_scale)
    logs.append("Assessed scale-up risks")

    return PipelineResult(
        thermo=thermo,
        reaction_pathways=pathways,
        heat_mass_transfer=hmt,
        phase_equilibria=phase_eq,
        env_toxicity=env_tox,
        reactor_design=reactor,
        separation_train=sep,
        scaleup_risks=risks,
        raw_logs=logs,
    )
