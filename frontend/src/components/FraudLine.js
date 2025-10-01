import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

export default function FraudLine({ data }) {
  // data expected: [{date: "YYYY-MM-DD", alerts: 2}, ...]
  return (
    <ResponsiveContainer width="100%" height={250}>
      <LineChart data={data}>
        <CartesianGrid stroke="#eee" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line dataKey="alerts" stroke="#ff4d4f" />
      </LineChart>
    </ResponsiveContainer>
  );
}
