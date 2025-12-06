from fastapi import APIRouter, HTTPException

from app.models.molecule import MoleculeInput, PipelineResult
from app.services.pipeline_service import run_pipeline

router = APIRouter()


@router.post("/molecule/analyze", response_model=PipelineResult)
def analyze_molecule(payload: MoleculeInput) -> PipelineResult:
    try:
        return run_pipeline(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/molecule/example", response_model=PipelineResult)
def example_pipeline() -> PipelineResult:
    sample = MoleculeInput(identifier="CCO", identifier_type="SMILES", reaction_type="oxidation", target_scale="pilot")
    return run_pipeline(sample)
