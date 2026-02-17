import { useState } from "react";
import { analyzeCSV } from "../../services/api";

export default function UploadCSV({ onData }) {
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      setLoading(true);
      const result = await analyzeCSV(file);
      onData(result);
    } catch (err) {
      console.error(err);
      alert("Error connecting to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
      <h2 className="text-xl font-semibold mb-4">Upload CSV</h2>

      <input
        type="file"
        accept=".csv"
        onChange={handleUpload}
        className="mb-3"
      />

      {loading && (
        <p className="text-slate-400 text-sm">Analyzing transactions...</p>
      )}
    </div>
  );
}
