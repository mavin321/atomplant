import { useState } from "react";
import { MoleculeInputForm } from "../api/client";

type Props = {
  onSubmit: (payload: MoleculeInputForm) => void | Promise<void>;
  loading?: boolean;
};

const defaults: MoleculeInputForm = {
  identifier: "",
  identifier_type: "SMILES",
  reaction_type: "",
  temperature_K: 298.15,
  pressure_bar: 1,
  solvent: "",
  phase: "liquid",
  target_scale: "lab",
};

function MoleculeForm({ onSubmit, loading }: Props) {
  const [form, setForm] = useState<MoleculeInputForm>(defaults);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (key: keyof MoleculeInputForm, value: any) => {
    setForm({ ...form, [key]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.identifier.trim()) {
        setError("Identifier is required");
        return;
    }
    setError(null);
    await onSubmit(form);
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <div className="field">
        <label>Identifier</label>
        <input
          type="text"
          value={form.identifier}
          onChange={(e) => handleChange("identifier", e.target.value)}
          placeholder="SMILES or InChI"
          required
        />
      </div>
      <div className="field">
        <label>Identifier Type</label>
        <select value={form.identifier_type} onChange={(e) => handleChange("identifier_type", e.target.value as any)}>
          <option value="SMILES">SMILES</option>
          <option value="InChI">InChI</option>
        </select>
      </div>
      <div className="field">
        <label>Reaction Type</label>
        <select value={form.reaction_type} onChange={(e) => handleChange("reaction_type", e.target.value)}>
          <option value="">General</option>
          <option value="Substitution">Substitution</option>
          <option value="Oxidation">Oxidation</option>
          <option value="Polymerization">Polymerization</option>
          <option value="Hydrogenation">Hydrogenation</option>
          <option value="Other">Other</option>
        </select>
      </div>
      <div className="field inline">
        <label>Temperature (K)</label>
        <input
          type="number"
          min={1}
          value={form.temperature_K}
          onChange={(e) => handleChange("temperature_K", parseFloat(e.target.value))}
        />
      </div>
      <div className="field inline">
        <label>Pressure (bar)</label>
        <input
          type="number"
          min={0.001}
          value={form.pressure_bar}
          onChange={(e) => handleChange("pressure_bar", parseFloat(e.target.value))}
        />
      </div>
      <div className="field">
        <label>Solvent</label>
        <input type="text" value={form.solvent} onChange={(e) => handleChange("solvent", e.target.value)} />
      </div>
      <div className="field inline">
        <label>Phase</label>
        <select value={form.phase} onChange={(e) => handleChange("phase", e.target.value as any)}>
          <option value="liquid">Liquid</option>
          <option value="gas">Gas</option>
          <option value="solid">Solid</option>
          <option value="mixed">Mixed</option>
        </select>
      </div>
      <div className="field inline">
        <label>Target Scale</label>
        <select value={form.target_scale} onChange={(e) => handleChange("target_scale", e.target.value as any)}>
          <option value="lab">Lab</option>
          <option value="pilot">Pilot</option>
          <option value="plant">Plant</option>
        </select>
      </div>
      {error && <div className="error">{error}</div>}
      <button type="submit" disabled={loading}>
        {loading ? "Analyzing..." : "Run Pipeline"}
      </button>
    </form>
  );
}

export type { MoleculeInputForm };
export default MoleculeForm;
