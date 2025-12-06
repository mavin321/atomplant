import { useState } from "react";
import MoleculeForm, { MoleculeInputForm } from "./components/MoleculeForm";
import PredictionSummary from "./components/PredictionSummary";
import ReactorDesignView from "./components/ReactorDesignView";
import SeparationTrainView from "./components/SeparationTrainView";
import ScaleUpRiskView from "./components/ScaleUpRiskView";
import { analyzeMolecule, PipelineResult } from "./api/client";

function App() {
  const [result, setResult] = useState<PipelineResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (payload: MoleculeInputForm) => {
    setLoading(true);
    setError(null);
    try {
      const res = await analyzeMolecule(payload);
      setResult(res);
    } catch (err: any) {
      setError(err?.message || "Failed to analyze molecule");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header>
        <h1>Atom-to-Plant AI</h1>
        <p>Stubbed molecular-to-reactor pipeline ready for future ML models.</p>
      </header>
      <main>
        <section className="card">
          <MoleculeForm onSubmit={onSubmit} loading={loading} />
          {error && <div className="error">{error}</div>}
        </section>
        {result && (
          <>
            <section className="card grid">
              <PredictionSummary thermo={result.thermo} pathways={result.reaction_pathways} />
              <ReactorDesignView design={result.reactor_design} />
              <SeparationTrainView train={result.separation_train} />
              <ScaleUpRiskView risks={result.scaleup_risks} />
            </section>
            <section className="card">
              <details>
                <summary>Raw JSON & Logs</summary>
                <pre>{JSON.stringify(result, null, 2)}</pre>
                {result.raw_logs && (
                  <ul>
                    {result.raw_logs.map((l) => (
                      <li key={l}>{l}</li>
                    ))}
                  </ul>
                )}
              </details>
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
