import { ReactorDesign } from "../api/client";

type Props = {
  design: ReactorDesign;
};

function ReactorDesignView({ design }: Props) {
  return (
    <div className="panel">
      <h3>Reactor Design</h3>
      <div className="reactor-type">{design.reactor_type}</div>
      <ul>
        <li>Volume: {design.volume_m3} m³</li>
        <li>Residence time: {design.residence_time_s} s</li>
        <li>Temperature: {design.operating_temperature_K} K</li>
        <li>Pressure: {design.operating_pressure_bar} bar</li>
      </ul>
    </div>
  );
}

export default ReactorDesignView;
