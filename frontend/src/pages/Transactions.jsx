import { useState } from "react";

export default function Transactions() {
  const [filter, setFilter] = useState("All");

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">
        Transactions Explorer
      </h1>

      <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
        <p className="text-slate-400">
          Full transaction table with filtering will go here.
        </p>
      </div>
    </div>
  );
}
