import { useState } from "react";
import UploadCSV from "../components/dashboard/UploadCSV";
import RiskDistributionChart from "../components/dashboard/RiskDistributionChart";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const [transactions, setTransactions] = useState([]);
  const navigate = useNavigate();

  const total = transactions.length;

  /* ================= RISK COUNTS ================= */

  const riskCounts = { High: 0, Medium: 0, Low: 0 };

  transactions.forEach((txn) => {
    if (riskCounts[txn.risk_level] !== undefined) {
      riskCounts[txn.risk_level]++;
    }
  });

  const highRiskTransactions = transactions
    .filter((txn) => txn.risk_level === "High")
    .sort((a, b) => b.final_risk - a.final_risk)
    .slice(0, 10);

  const chartData = [
    { name: "Low Risk", value: riskCounts.Low },
    { name: "Medium Risk", value: riskCounts.Medium },
    { name: "High Risk", value: riskCounts.High },
  ];

  /* ================= METRICS ================= */

  const avgConfidence =
    total > 0
      ? (
          transactions.reduce(
            (sum, txn) => sum + txn.confidence_score,
            0
          ) / total
        ).toFixed(1)
      : 0;

  const avgContextImpact =
    total > 0
      ? (
          transactions.reduce(
            (sum, txn) => sum + txn.context_adjustment,
            0
          ) / total
        ).toFixed(2)
      : 0;

  return (
    <div>

      <UploadCSV onData={setTransactions} />

      {total > 0 && (
        <>
          {/* ================= EXECUTIVE METRICS ================= */}
          <div className="grid grid-cols-4 gap-6 mt-12">

            <MetricCard
              title="Total Transactions"
              value={total}
            />

            <MetricCard
              title="High Risk Alerts"
              value={riskCounts.High}
              color="bg-red-600"
            />

            <MetricCard
              title="Avg Confidence"
              value={`${avgConfidence}%`}
              color="bg-purple-600"
            />

            <MetricCard
              title="Avg Context Impact"
              value={avgContextImpact}
              color="bg-blue-600"
            />

          </div>

          {/* ================= ANALYTICS GRID ================= */}
          <div className="grid grid-cols-3 gap-6 mt-12">

            <RiskDistributionChart data={chartData} />

            <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
              <h3 className="text-lg font-semibold mb-4">
                Hybrid Risk Model
              </h3>

              <div className="space-y-2 text-slate-300 text-sm">
                <p>• AI Anomaly Score (60%)</p>
                <p>• Rule-Based Score (40%)</p>
                <p>• Context Adjustment Applied</p>
                <p>• Confidence Calibration Layer</p>
              </div>
            </div>

            <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
              <h3 className="text-lg font-semibold mb-4">
                System Insight
              </h3>

              <p className="text-slate-400 text-sm leading-relaxed">
                Risk levels are determined using absolute calibrated
                thresholds. Context layer reduces false positives by
                adjusting risk based on peer similarity and exporter stability.
              </p>
            </div>
          </div>

          {/* ================= HIGH RISK INTELLIGENCE TABLE ================= */}
          <div className="bg-slate-900 p-8 rounded-2xl border border-slate-800 mt-14">
            <h3 className="text-2xl font-semibold mb-8">
              High Risk Transactions – Intelligence View
            </h3>

            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="text-slate-400 border-b border-slate-700">
                  <tr>
                    <th className="text-left pb-4">Txn ID</th>
                    <th className="text-center">Final Risk</th>
                    <th className="text-center">AI Score</th>
                    <th className="text-center">Context Δ</th>
                    <th className="text-center">Primary Trigger</th>
                    <th className="text-center">Confidence</th>
                    <th className="text-center">Action</th>
                  </tr>
                </thead>

                <tbody>
                  {highRiskTransactions.map((txn) => {

                    const getTrigger = () => {
                      if (txn.price_rule_triggered) return "Price Deviation";
                      if (txn.volume_rule_triggered) return "Volume Spike";
                      if (txn.route_rule_triggered) return "Rare Route";
                      if (txn.exporter_rule_triggered) return "New Exporter";
                      return "AI Anomaly";
                    };

                    return (
                      <tr
                        key={txn.transaction_id}
                        className="border-b border-slate-800 hover:bg-slate-800 transition"
                      >
                        <td className="py-4 font-medium">
                          {txn.transaction_id}
                        </td>

                        <td className="text-center">
                          <span className="text-red-400 font-semibold">
                            {txn.final_risk.toFixed(1)}
                          </span>
                        </td>

                        <td className="text-center">
                          {txn.ai_score.toFixed(1)}
                        </td>

                        <td
                          className={`text-center ${
                            txn.context_adjustment < 0
                              ? "text-blue-400"
                              : "text-yellow-400"
                          }`}
                        >
                          {txn.context_adjustment.toFixed(1)}
                        </td>

                        <td className="text-center text-slate-300">
                          {getTrigger()}
                        </td>

                        <td className="text-center">
                          {txn.confidence_score.toFixed(1)}%
                        </td>

                        <td className="text-center">
                          <button
                            onClick={() =>
                              navigate("/transactions")
                            }
                            className="bg-blue-600 px-4 py-1 rounded-lg hover:bg-blue-500 transition"
                          >
                            View
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>

              {highRiskTransactions.length === 0 && (
                <p className="text-slate-400 mt-6">
                  No high-risk transactions detected.
                </p>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

/* ================= METRIC CARD ================= */

function MetricCard({ title, value, color = "bg-slate-800" }) {
  return (
    <div
      className={`${color} p-6 rounded-xl border border-slate-700`}
    >
      <p className="text-sm text-slate-300">{title}</p>
      <p className="text-2xl font-bold mt-2">{value}</p>
    </div>
  );
}
