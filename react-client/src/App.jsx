import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [pingResult, setPingResult] = useState(null);
  const [message, setMessage] = useState("Hello from React!");
  const [echoResult, setEchoResult] = useState(null);
  const [error, setError] = useState(null);

  const preStyle = {
    background: "#111827",
    color: "#e5e7eb",
    padding: 12,
    borderRadius: 10,
    overflowX: "auto",
    border: "1px solid #374151",
  };

  const errorStyle = {
    background: "#3b0a0a",
    color: "#fecaca",
    padding: 12,
    borderRadius: 10,
    border: "1px solid #7f1d1d",
  };

  async function doPing() {
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/ping`);
      if (!res.ok) throw new Error(`Ping failed: ${res.status}`);
      setPingResult(await res.json());
    } catch (e) {
      setError(String(e));
    }
  }

  async function doEcho() {
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/echo`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      if (!res.ok) throw new Error(`Echo failed: ${res.status}`);
      setEchoResult(await res.json());
    } catch (e) {
      setError(String(e));
    }
  }

  return (
    <div style={{ fontFamily: "sans-serif", padding: 20, maxWidth: 700 }}>
      <h1>Local React ↔ FastAPI</h1>

      <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
        <button onClick={doPing}>Ping</button>
        <button onClick={doEcho}>Echo</button>
      </div>

      <div style={{ marginBottom: 10 }}>
        <label>
          Message:{" "}
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            style={{ width: 300 }}
          />
        </label>
      </div>

      {error && <pre style={errorStyle}>Error: {error}</pre>}

      <h3>/ping result</h3>
      <pre style={preStyle}>
        {pingResult ? JSON.stringify(pingResult, null, 2) : "—"}
      </pre>

      <h3>/echo result</h3>
      <pre style={preStyle}>
        {echoResult ? JSON.stringify(echoResult, null, 2) : "—"}
      </pre>
    </div>
  );
}
