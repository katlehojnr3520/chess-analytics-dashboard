import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  LineChart,
  Line,
} from "recharts";

export default function App() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${process.env.PUBLIC_URL}/stats.json`)
      .then((res) => res.json())
      .then((data) => {
        setStats(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching stats:", error);
        setLoading(false);
      });
  }, []);

  if (loading)
    return (
      <div
        style={{
          textAlign: "center",
          color: "#fff",
          background: "#0f172a",
          minHeight: "100vh",
          paddingTop: "20%",
        }}
      >
        <h2>Compiling Executive Metrics...</h2>
      </div>
    );
  if (!stats)
    return (
      <div
        style={{
          textAlign: "center",
          color: "#fff",
          background: "#0f172a",
          minHeight: "100vh",
          paddingTop: "20%",
        }}
      >
        <h2>Data Stream Missing. Run your Python pipeline script</h2>
      </div>
    );

  const summaryData = [
    { name: "Wins", value: stats.metadata.wins, fill: "#10b981" },
    { name: "Losses", value: stats.metadata.losses, fill: "#ef4444" },
    { name: "Draws", value: stats.metadata.draws, fill: "#64748b" },
  ];

 
  const styles = {
    container: {
      minHeight: "100vh",
      backgroundColor: "#0f172a",
      color: "#f8fafc",
      padding: "2rem",
      fontFamily:
        '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    },
    header: {
      marginBottom: "2.5rem",
      borderBottom: "1px solid #334155",
      paddingBottom: "1rem",
    },
    title: {
      fontSize: "2.25rem",
      fontWeight: "800",
      margin: "0 0 0.5rem 0",
      color: "#38bdf8",
    },
    subtitle: { fontSize: "1rem", margin: 0, color: "#94a3b8" },
    grid: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
      gap: "1.5rem",
      marginBottom: "2.5rem",
    },
    card: {
      backgroundColor: "#1e293b",
      border: "1px solid #334155",
      padding: "1.5rem",
      borderRadius: "0.75rem",
      boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
    },
    cardLabel: {
      fontSize: "0.875rem",
      fontWeight: "600",
      textTransform: "uppercase",
      color: "#94a3b8",
      margin: "0 0 0.5rem 0",
      tracking: "0.05em",
    },
    cardVal: { fontSize: "2.5rem", fontWeight: "800", margin: 0 },
    chartSection: {
      backgroundColor: "#1e293b",
      border: "1px solid #334155",
      padding: "2rem",
      borderRadius: "0.75rem",
      height: "400px",
    },
    chartTitle: {
      fontSize: "1.25rem",
      fontWeight: "700",
      margin: "0 0 1.5rem 0",
      color: "#f1f5f9",
    },
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>Chess.com Stats Dashboard</h1>
        <p style={styles.subtitle}>
          This is how good is{" "}
          <strong>{stats.metadata.username}</strong>
           {" "} at chess.
        </p>
      </header>

      <div style={styles.grid}>
        <div style={styles.card}>
          <p style={styles.cardLabel}>Total Scale</p>
          <p style={{ ...styles.cardVal, color: "#818cf8" }}>
            {stats.metadata.total_games}
          </p>
          <span style={{ fontSize: "0.85rem", color: "#64748b" }}>
            Games Evaluated
          </span>
        </div>
        <div style={styles.card}>
          <p style={styles.cardLabel}>Win Strategy Ratio</p>
          <p style={{ ...styles.cardVal, color: "#34d399" }}>
            {stats.metadata.win_rate_percentage}%
          </p>
          <span style={{ fontSize: "0.85rem", color: "#64748b" }}>
            Overall Efficiency
          </span>
        </div>
        <div style={styles.card}>
          <p style={styles.cardLabel}>Average Blitz ELO</p>
          <p style={{ ...styles.cardVal, color: "#fbbf24" }}>
            {stats.ratings.blitz_avg || "N/A"}
          </p>
          <span style={{ fontSize: "0.85rem", color: "#64748b" }}>
            Current Tier Strength
          </span>
        </div>
        <div style={styles.card}>
          <p style={styles.cardLabel}>Average Rapid ELO</p>
          <p style={{ ...styles.cardVal, color: "#60a5fa" }}>
            {stats.ratings.rapid_avg || "N/A"}
          </p>
          <span style={{ fontSize: "0.85rem", color: "#64748b" }}>
            Strategic Format
          </span>
        </div>
      </div>

      {/* Recharts Graphical Distribution Matrix */}
      <div style={styles.chartSection}>
        <h3 style={styles.chartTitle}>
          Match Outcome Distributions (Recent Timeline)
        </h3>
        <ResponsiveContainer width="100%" height="85%">
          <BarChart
            data={summaryData}
            margin={{ top: 10, right: 10, left: -20, bottom: 5 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#334155"
              vertical={false}
            />
            <XAxis dataKey="name" stroke="#94a3b8" tickLine={false} />
            <YAxis stroke="#94a3b8" tickLine={false} />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                border: "1px solid #334155",
                borderRadius: "0.5rem",
                color: "#fff",
              }}
              cursor={{ fill: "rgba(255, 255, 255, 0.03)" }}
            />
            <Bar dataKey="value" radius={[6, 6, 0, 0]} barSize={60} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
