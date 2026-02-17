import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

export default function RiskDistributionChart({ data }) {
  const COLORS = ["#16a34a", "#f59e0b", "#dc2626"];

  return (
    <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 h-full">
      <h2 className="text-xl font-semibold mb-6">
        Risk Distribution
      </h2>

      <div className="h-72">
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              outerRadius={100}
              label
            >
              {data.map((entry, index) => (
                <Cell key={index} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
