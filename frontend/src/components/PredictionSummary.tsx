import { ReactionPathway, ThermoProperties } from "../api/client";

type Props = {
  thermo: ThermoProperties;
  pathways: ReactionPathway[];
};

function PredictionSummary({ thermo, pathways }: Props) {
  return (
    <div className="panel">
      <h3>Thermo Properties</h3>
      <table>
        <tbody>
          <tr>
            <td>Cp</td>
            <td>{thermo.cp_J_per_molK.toFixed(2)} J/mol-K</td>
          </tr>
          <tr>
            <td>ΔHf</td>
            <td>{thermo.hf_formation_kJ_per_mol.toFixed(2)} kJ/mol</td>
          </tr>
          <tr>
            <td>Density</td>
            <td>{thermo.density_kg_per_m3.toFixed(1)} kg/m³</td>
          </tr>
          <tr>
            <td>Boiling Point</td>
            <td>{thermo.boiling_point_K.toFixed(1)} K</td>
          </tr>
          <tr>
            <td>Vapor Pressure</td>
            <td>{thermo.vapor_pressure_bar.toFixed(2)} bar</td>
          </tr>
        </tbody>
      </table>
      <h3>Reaction Pathways</h3>
      <ul className="pathways">
        {pathways.map((p) => (
          <li key={p.pathway_id}>
            <div className="pathway-header">
              <span>{p.description}</span>
              <span className="badge">Hazard {p.hazard_score.toFixed(1)}</span>
            </div>
            <div>Yield: {p.estimated_yield_percent.toFixed(1)}%</div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PredictionSummary;
