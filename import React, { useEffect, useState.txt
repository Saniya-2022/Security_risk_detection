import React, { useEffect, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [alerts, setAlerts] = useState([]);
  const [filter, setFilter] = useState("ALL");

  // ==============================
  // Fetch Alerts
  // ==============================
  const fetchAlerts = () => {
    fetch("http://127.0.0.1:8000/alerts")
      .then((res) => res.json())
      .then((data) => setAlerts(data))
      .catch((err) => console.error("Error fetching alerts:", err));
  };

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  // ==============================
  // Filter Logic
  // ==============================
  const filteredAlerts =
    filter === "ALL"
      ? alerts
      : alerts.filter((a) => a.severity === filter);

  const dataSource = filteredAlerts;

  const severityLevels = [
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "ERROR",
    "WARNING",
    "INFO",
  ];

  const severityCount = {};
  severityLevels.forEach((level) => {
    severityCount[level] = dataSource.filter(
      (a) => a.severity === level
    ).length;
  });

  // ==============================
  // Chart Data
  // ==============================
  const chartData = {
    labels: severityLevels,
    datasets: [
      {
        label: "Threat Distribution",
        data: severityLevels.map((level) => severityCount[level]),
        backgroundColor: [
          "#ff1a1a",
          "#ff4d4d",
          "#4da6ff",
          "#ff944d",
          "#ffd11a",
          "#66cc66",
        ],
      },
    ],
  };

  // ==============================
  // Severity Color
  // ==============================
  const getSeverityColor = (severity) => {
    switch (severity) {
      case "CRITICAL":
        return "#ff1a1a";
      case "HIGH":
        return "#ff4d4d";
      case "ERROR":
        return "#ff944d";
      case "WARNING":
        return "#ffd11a";
      case "MEDIUM":
        return "#4da6ff";
      default:
        return "#66cc66";
    }
  };

  return (
    <div
      style={{
        padding: "20px",
        background: "#121212",
        minHeight: "100vh",
        color: "white",
      }}
    >
      <h1>🚨 Security Risk Dashboard</h1>

      {/* ==============================
          Summary Cards
      ============================== */}
      <div style={{ display: "flex", gap: "15px", marginBottom: "20px", flexWrap: "wrap" }}>
        {severityLevels.map((level) => (
          <div
            key={level}
            style={{
              background: "#1e1e1e",
              padding: "15px",
              borderRadius: "6px",
              borderLeft: `6px solid ${getSeverityColor(level)}`,
              minWidth: "120px",
            }}
          >
            <h3>{level}</h3>
            <p>{severityCount[level]}</p>
          </div>
        ))}
      </div>

      {/* ==============================
          Filter
      ============================== */}
      <div style={{ marginBottom: "20px" }}>
        <label>Filter by Severity: </label>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          style={{ padding: "5px" }}
        >
          <option value="ALL">ALL</option>
          {severityLevels.map((level) => (
            <option key={level} value={level}>
              {level}
            </option>
          ))}
        </select>
      </div>

      {/* ==============================
          Chart
      ============================== */}
      <div
        style={{
          background: "#1e1e1e",
          padding: "20px",
          borderRadius: "6px",
          marginBottom: "30px",
        }}
      >
        <Bar data={chartData} />
      </div>

      {/* ==============================
          Alerts List
      ============================== */}
      {filteredAlerts.length === 0 ? (
        <p>No alerts found.</p>
      ) : (
        filteredAlerts.map((alert) => (
          <div
            key={alert._id}
            style={{
              background: "#1e1e1e",
              padding: "15px",
              borderRadius: "6px",
              marginBottom: "15px",
              borderLeft: `6px solid ${getSeverityColor(alert.severity)}`,
            }}
          >
            <h3 style={{ color: getSeverityColor(alert.severity) }}>
              {alert.severity}
            </h3>

            {/* Risk Score */}
            <p><strong>Risk Score:</strong> {alert.risk_score}</p>

            {/* Static Code Alerts */}
            {alert.file && (
              <>
                <p><strong>File:</strong> {alert.file}</p>
                <p><strong>Line:</strong> {alert.line}</p>
                <p><strong>Rule:</strong> {alert.rule_id}</p>
              </>
            )}

            {/* Runtime Alerts */}
            {alert.type === "Runtime Threat" && (
              <>
                <p><strong>Threat:</strong> {alert.threat}</p>
                <p><strong>User:</strong> {alert.user}</p>
                <p><strong>IP:</strong> {alert.ip}</p>
              </>
            )}

            {/* Email / Phishing Data */}
            {alert.email_data && (
              <>
                <p><strong>Sender:</strong> {alert.email_data.sender}</p>
                <p><strong>Subject:</strong> {alert.email_data.subject}</p>
                <p><strong>Attachment:</strong> {alert.email_data.attachment}</p>
              </>
            )}

            {/* Description */}
            {alert.description && <p>{alert.description}</p>}

            {/* Phishing Explanation */}
            {alert.alert?.details?.map((item, index) => (
              <p key={index} style={{ color: "#ffcc00" }}>
                ⚠ {item}
              </p>
            ))}

            {/* Recommended Action */}
            {alert.alert?.recommended_action && (
              <p style={{ marginTop: "10px", color: "#66cc66" }}>
                🛡 <strong>Recommended Action:</strong>{" "}
                {alert.alert.recommended_action}
              </p>
            )}

            {/* Date */}
            <small>
              {alert.created_at || alert.timestamp
                ? new Date(alert.created_at || alert.timestamp).toLocaleString()
                : "No Date Available"}
            </small>
          </div>
        ))
      )}
    </div>
  );
}

export default App;
