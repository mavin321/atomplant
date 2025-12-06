export type MoleculeInputForm = {
  identifier: string;
  identifier_type: "SMILES" | "InChI";
  reaction_type?: string;
  temperature_K?: number;
  pressure_bar?: number;
  solvent?: string;
  phase?: "liquid" | "gas" | "solid" | "mixed";
  target_scale: "lab" | "pilot" | "plant";
};

export type ThermoProperties = {
  cp_J_per_molK: number;
  hf_formation_kJ_per_mol: number;
  density_kg_per_m3: number;
  boiling_point_K: number;
  vapor_pressure_bar: number;
};

export type ReactionPathway = {
  pathway_id: string;
  description: string;
  estimated_yield_percent: number;
  hazard_score: number;
};

export type HeatMassTransfer = {
  heat_transfer_coeff_W_per_m2K: number;
  mass_transfer_coeff_m_per_s: number;
  diffusion_coeff_m2_per_s: number;
};

export type PhaseEquilibria = {
  k_value: number;
  partition_coefficient_logP: number;
  azeotrope_flag: boolean;
};

export type EnvToxicityProfile = {
  environmental_score: number;
  toxicity_score: number;
  notes: string;
};

export type ReactorDesign = {
  reactor_type: "CSTR" | "PFR" | "batch" | "semi-batch";
  volume_m3: number;
  residence_time_s: number;
  operating_temperature_K: number;
  operating_pressure_bar: number;
};

export type SeparationUnit = {
  unit_type: "distillation" | "extraction" | "filtration" | "absorption" | "stripping";
  description: string;
};

export type SeparationTrain = {
  units: SeparationUnit[];
};

export type ScaleUpRisks = {
  hot_spot_risk: number;
  runaway_risk: number;
  mixing_limitation_risk: number;
  notes: string;
};

export type PipelineResult = {
  thermo: ThermoProperties;
  reaction_pathways: ReactionPathway[];
  heat_mass_transfer: HeatMassTransfer;
  phase_equilibria: PhaseEquilibria;
  env_toxicity: EnvToxicityProfile;
  reactor_design: ReactorDesign;
  separation_train: SeparationTrain;
  scaleup_risks: ScaleUpRisks;
  raw_logs?: string[];
};

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function analyzeMolecule(input: MoleculeInputForm): Promise<PipelineResult> {
  const res = await fetch(`${API_BASE}/api/v1/molecule/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || "Failed to analyze molecule");
  }
  return res.json();
}
