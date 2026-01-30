/**
 * GovernAble AI Governance Dashboard
 * 
 * Shows:
 * - Recent AI interactions (allowed, blocked, redacted)
 * - Policy violations by user/department
 * - Compliance audit trail
 * - Trends and risk analytics
 */

import React, { useEffect, useState } from "react";
import "./App.css";

type AIInteraction = {
  id: number;
  user_id: string;
  timestamp: string;
  action: "ALLOW" | "BLOCK" | "REDACT";
  ai_service: string;
  findings_count: number;
  risk_score: number;
  prompt_preview: string;
};

function App() {
  const [interactions, setInteractions] = useState<AIInteraction[]>([]);
  const [stats, setStats] = useState({
    total: 0,
    blocked: 0,
    redacted: 0,
    allowed: 0
  });

  useEffect(() => {
    // Fetch AI governance interactions
    fetch("http://localhost:8000/api/v1/governance/interactions")
      .then(r => r.json())
      .then(data => {
        setInteractions(data.interactions || []);
        setStats(data.stats || stats);
      })
      .catch(console.error);
  }, []);

  const getActionBadge = (action: string) => {
    const styles = {
      BLOCK: { bg: "#fee", color: "#c00", label: "🚫 BLOCKED" },
      REDACT: { bg: "#ffc", color: "#860", label: "🧹 REDACTED" },
      ALLOW: { bg: "#efe", color: "#060", label: "✅ ALLOWED" }
    };
    const style = styles[action as keyof typeof styles] || styles.ALLOW;
    return (
      <span style={{
        background: style.bg,
        color: style.color,
        padding: "4px 8px",
        borderRadius: "4px",
        fontWeight: "bold"
      }}>
        {style.label}
      </span>
    );
  };

  return (
    <div className="App">
      <header style={{ background: "#1a1a1a", color: "#fff", padding: "20px" }}>
        <h1>🛡️ GovernAble - AI Governance Dashboard</h1>
        <p>Monitoring AI usage and enforcing security policies</p>
      </header>

      {/* Statistics */}
      <div style={{ display: "flex", gap: "20px", padding: "20px" }}>
        <StatCard title="Total Requests" value={stats.total} color="#333" />
        <StatCard title="Blocked" value={stats.blocked} color="#c00" />
        <StatCard title="Redacted" value={stats.redacted} color="#f80" />
        <StatCard title="Allowed" value={stats.allowed} color="#0a0" />
      </div>

      {/* Recent AI Interactions */}
      <div style={{ padding: "20px" }}>
        <h2>Recent AI Interactions</h2>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#f5f5f5", textAlign: "left" }}>
              <th style={{ padding: "10px" }}>Time</th>
              <th style={{ padding: "10px" }}>User</th>
              <th style={{ padding: "10px" }}>AI Service</th>
              <th style={{ padding: "10px" }}>Action</th>
              <th style={{ padding: "10px" }}>Risk Score</th>
              <th style={{ padding: "10px" }}>Prompt Preview</th>
            </tr>
          </thead>
          <tbody>
            {interactions.length === 0 ? (
              <tr>
                <td colSpan={6} style={{ padding: "20px", textAlign: "center", color: "#999" }}>
                  No AI interactions yet. Try sending a request through the Governor Proxy.
                </td>
              </tr>
            ) : (
              interactions.map(interaction => (
                <tr key={interaction.id} style={{ borderBottom: "1px solid #eee" }}>
                  <td style={{ padding: "10px" }}>
                    {new Date(interaction.timestamp).toLocaleString()}
                  </td>
                  <td style={{ padding: "10px" }}>{interaction.user_id}</td>
                  <td style={{ padding: "10px" }}>{interaction.ai_service}</td>
                  <td style={{ padding: "10px" }}>{getActionBadge(interaction.action)}</td>
                  <td style={{ padding: "10px" }}>
                    <RiskScoreBadge score={interaction.risk_score} />
                  </td>
                  <td style={{ padding: "10px", maxWidth: "300px", overflow: "hidden", textOverflow: "ellipsis" }}>
                    {interaction.prompt_preview}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Compliance Export */}
      <div style={{ padding: "20px" }}>
        <button onClick={() => window.location.href = '/api/v1/governance/export?format=csv'}>
          📊 Export Compliance Report (CSV)
        </button>
      </div>
    </div>
  );
}

function StatCard({ title, value, color }: { title: string; value: number; color: string }) {
  return (
    <div style={{
      flex: 1,
      padding: "20px",
      background: "#fff",
      border: `2px solid ${color}`,
      borderRadius: "8px",
      textAlign: "center"
    }}>
      <h3 style={{ margin: 0, color: color }}>{value}</h3>
      <p style={{ margin: "5px 0 0", color: "#666" }}>{title}</p>
    </div>
  );
}

function RiskScoreBadge({ score }: { score: number }) {
  const color = score >= 80 ? "#c00" : score >= 40 ? "#f80" : "#0a0";
  return (
    <span style={{
      background: color,
      color: "#fff",
      padding: "4px 8px",
      borderRadius: "4px",
      fontWeight: "bold"
    }}>
      {score}
    </span>
  );
}

export default App;