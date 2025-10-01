// frontend/src/components/TransactionForm.js
import React, { useState } from "react";
import axios from "axios";

export default function TransactionForm({ onSubmitted }) {
  const [userId, setUserId] = useState("");
  const [amount, setAmount] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userId || !amount) {
      alert("Please enter User ID and Amount");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        user_id: Number(userId),
        amount: Number(amount),
      };

      // Relative URL → React proxy (package.json) forwards to Flask backend
      const res = await axios.post("/transactions/add", payload);

      alert(res.data.message || "Transaction submitted!");
      setUserId("");
      setAmount("");

      // Trigger parent refresh if passed
      if (typeof onSubmitted === "function") onSubmitted();

      // Dispatch event so Dashboard.js knows to refresh
      window.dispatchEvent(new Event("refreshDashboard"));
    } catch (err) {
      console.error("Error submitting transaction:", err);
      const msg =
        err?.response?.data?.error || err.message || "Failed to submit";
      alert("Error: " + msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{ display: "flex", gap: 8, alignItems: "center" }}
    >
      <input
        required
        placeholder="User ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        style={{ padding: 8, borderRadius: 6, border: "1px solid #ccc" }}
      />
      <input
        required
        placeholder="Amount"
        type="number"
        step="0.01"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        style={{ padding: 8, borderRadius: 6, border: "1px solid #ccc" }}
      />
      <button
        type="submit"
        disabled={loading}
        style={{
          padding: "8px 14px",
          borderRadius: 6,
          background: loading ? "#aaa" : "#1976d2",
          color: "#fff",
          border: "none",
          cursor: loading ? "not-allowed" : "pointer",
        }}
      >
        {loading ? "Submitting..." : "Submit"}
      </button>
    </form>
  );
}
