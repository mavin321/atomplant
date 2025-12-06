import { ScaleUpRisks } from "../api/client";

type Props = {
  risks: ScaleUpRisks;
};

const RiskBar = ({ label, value }: { label: string; value: number }) => {
  const pct = Math.min(100, Math.max(0, value * 100));
  return (
    <div className="risk-bar">
      <div className="risk-label">
        {label}: {pct.toFixed(0)}%
      </div>
      <div className="risk-meter">
        <div className="risk-meter-fill" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
};

function ScaleUpRiskView({ risks }: Props) {
  return (
    <div className="panel">
      <h3>Scale-Up Risks</h3>
      <RiskBar label="Hot spot" value={risks.hot_spot_risk} />
      <RiskBar label="Runaway" value={risks.runaway_risk} />
      <RiskBar label="Mixing" value={risks.mixing_limitation_risk} />
      <p className="notes">{risks.notes}</p>
    </div>
  );
}

export default ScaleUpRiskView;
