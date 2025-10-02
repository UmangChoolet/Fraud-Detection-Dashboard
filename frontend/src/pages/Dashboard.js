import React, { useEffect, useState } from "react";
import axios from "axios";
import SummaryCards from "../components/SummaryCards";
import FraudLine from "../components/FraudLine";
import TopUsers from "../components/TopUsers";
import DistributionPie from "../components/DistributionPie";
import RecentFrauds from "../components/RecentFrauds";
import TransactionForm from "../components/TransactionForm";
import API_BASE_URL from "../config";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [alertsOverTime, setAlertsOverTime] = useState([]);
  const [topUsers, setTopUsers] = useState([]);
  const [distribution, setDistribution] = useState([]);
  const [recentFrauds, setRecentFrauds] = useState([]);

  const fetchAll = async () => {
    try {
      const [s, a, t, d, r] = await Promise.all([
        axios.get(`${API_BASE_URL}/transactions/summary`),
        axios.get(`${API_BASE_URL}/frauds/alerts`),
        axios.get(`${API_BASE_URL}/users/top`),
        axios.get(`${API_BASE_URL}/transactions/distribution`),
        axios.get(`${API_BASE_URL}/frauds/recent`),
      ]);
      setSummary(s.data);
      setAlertsOverTime(a.data);
      setTopUsers(t.data);
      setDistribution(d.data);
      setRecentFrauds(r.data);
    } catch (err) {
      console.error("Error fetching dashboard data", err);
    }
  };

  useEffect(() => {
    fetchAll();

    // Poll every 6 seconds for near-real-time updates
    const id = setInterval(fetchAll, 6000);

    // Listen for refresh event from TransactionForm
    const refreshHandler = () => {
      fetchAll();
    };
    window.addEventListener("refreshDashboard", refreshHandler);

    return () => {
      clearInterval(id);
      window.removeEventListener("refreshDashboard", refreshHandler);
    };
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h1>📊 Fraud Detection Dashboard</h1>

      <div style={{ marginTop: 12 }}>
        <SummaryCards summary={summary} />
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 20,
          marginTop: 20,
        }}
      >
        <div style={{ background: "#fff", padding: 12, borderRadius: 8 }}>
          <h3>Fraud Alerts Over Time</h3>
          <FraudLine data={alertsOverTime} />
        </div>

        <div style={{ background: "#fff", padding: 12, borderRadius: 8 }}>
          <h3>Top Users by Spending</h3>
          <TopUsers data={topUsers} />
        </div>

        <div
          style={{
            gridColumn: "1 / span 1",
            background: "#fff",
            padding: 12,
            borderRadius: 8,
          }}
        >
          <h3>Transaction Distribution</h3>
          <DistributionPie data={distribution} />
        </div>

        <div
          style={{
            gridColumn: "2 / span 1",
            background: "#fff",
            padding: 12,
            borderRadius: 8,
          }}
        >
          <h3>Latest Fraud Alerts</h3>
          <RecentFrauds data={recentFrauds} />
        </div>
      </div>

      <div
        style={{
          marginTop: 20,
          background: "#fff",
          padding: 12,
          borderRadius: 8,
        }}
      >
        <h3>Simulate a Transaction</h3>
        <TransactionForm onSubmitted={fetchAll} />
      </div>
    </div>
  );
}
