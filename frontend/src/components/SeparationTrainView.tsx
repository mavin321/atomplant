import { SeparationTrain } from "../api/client";

type Props = {
  train: SeparationTrain;
};

function SeparationTrainView({ train }: Props) {
  return (
    <div className="panel">
      <h3>Separation Train</h3>
      <ol className="train">
        {train.units.map((u, idx) => (
          <li key={`${u.unit_type}-${idx}`}>
            <span className="badge">{u.unit_type}</span> {u.description}
          </li>
        ))}
      </ol>
    </div>
  );
}

export default SeparationTrainView;
