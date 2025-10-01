import React from "react";

export default function RecentFrauds({ data }) {
  if (!data) return <div>Loading...</div>;
  if (data.length === 0) return <div>No alerts</div>;

  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <th style={th}>User</th>
          <th style={th}>Amount</th>
          <th style={th}>Alert</th>
          <th style={th}>Time</th>
        </tr>
      </thead>
      <tbody>
        {data.map((r, idx) => (
          <tr key={idx}>
            <td style={td}>{r.user_id}</td>
            <td style={td}>${r.amount}</td>
            <td style={td}>{r.alert}</td>
            <td style={td}>{new Date(r.created_at).toLocaleString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

const th = { textAlign: "left", padding: 8, borderBottom: "1px solid #ddd" };
const td = { padding: 8, borderBottom: "1px solid #f0f0f0" };
