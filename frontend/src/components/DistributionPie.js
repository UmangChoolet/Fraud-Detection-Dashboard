import React from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

const COLORS = ["#4caf50", "#ff4d4f", "#ffa726", "#2196f3"];

export default function DistributionPie({ data }) {
  // data: [{status: "SUCCESS", count: 40}, {status: "fraud", count: 10}]
  if (!data || data.length === 0) return <div>No distribution data</div>;

  return (
    <ResponsiveContainer width="100%" height={250}>
      <PieChart>
        <Pie data={data} dataKey="count" nameKey="status" outerRadius={80} fill="#8884d8" label>
          {data.map((entry, idx) => <Cell key={idx} fill={COLORS[idx % COLORS.length]} />)}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );
}