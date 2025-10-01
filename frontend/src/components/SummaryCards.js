import React from "react";

export default function SummaryCards({ summary }) {
  if (!summary) return <div>Loading summary...</div>;

  return (
    <div style={{ display: "flex", gap: 12 }}>
      <div style={cardStyle}>
        <h4>Total Transactions</h4>
        <div style={big}>{summary.total_transactions}</div>
      </div>
      <div style={cardStyle}>
        <h4>Average Amount</h4>
        <div style={big}>${summary.avg_amount}</div>
      </div>
      <div style={cardStyle}>
        <h4>Fraud Rate</h4>
        <div style={big}>{(summary.fraud_rate * 100).toFixed(2)}%</div>
      </div>
    </div>
  );
}

const cardStyle = {
  background: "#f5f7fb",
  padding: 12,
  borderRadius: 8,
  flex: 1,
};

const big = { fontSize: 22, marginTop: 6, fontWeight: 700 };
