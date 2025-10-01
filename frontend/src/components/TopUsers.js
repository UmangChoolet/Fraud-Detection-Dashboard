import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

export default function TopUsers({ data }) {
  // data: [{ user_id: 1029, total_spent: 9984.05 }, ...]
  return (
    <ResponsiveContainer width="100%" height={250}>
      <BarChart data={data}>
        <CartesianGrid stroke="#eee" />
        <XAxis dataKey="user_id" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="total_spent" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );
}