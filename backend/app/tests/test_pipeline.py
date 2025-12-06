from fastapi.testclient import TestClient

from app.main import app
from app.models.molecule import MoleculeInput
from app.services.pipeline_service import run_pipeline


def test_run_pipeline_basic():
    inp = MoleculeInput(identifier="CCO", identifier_type="SMILES", temperature_K=298.15, pressure_bar=1.0)
    result = run_pipeline(inp)
    assert result.thermo.cp_J_per_molK > 0
    assert result.thermo.boiling_point_K > 0
    assert len(result.reaction_pathways) >= 1
    assert result.separation_train.units
    assert 0 <= result.scaleup_risks.hot_spot_risk <= 1


def test_api_analyze():
    client = TestClient(app)
    payload = {"identifier": "CCO", "identifier_type": "SMILES"}
    response = client.post("/api/v1/molecule/analyze", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "thermo" in body
    assert "reactor_design" in body
