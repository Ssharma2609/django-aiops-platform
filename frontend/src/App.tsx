import axios from "axios";
import { useEffect, useState } from "react";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function App() {
  const [incidents, setIncidents] = useState<any[]>([]);
  const [metrics, setMetrics] = useState<any[]>([]);
  const [anomalies, setAnomalies] = useState<any[]>([]);

  // INCIDENT FETCH

  const fetchIncidents = async () => {
    try {
      const response = await axios.get(
        "http://localhost:8000/api/incidents/"
      );

      setIncidents(response.data);
    } catch (error) {
      console.error(
        "Incident Fetch Error:",
        error
      );
    }
  };

  // METRIC FETCH

  const fetchMetrics = async () => {
    try {
      console.log("FETCHING METRICS...");

      const response = await axios.get(
        "http://localhost:8000/api/metrics/"
      );

      const latestMetrics = Array.isArray(response.data)
        ? response.data
        : [];

      console.log(
        "LATEST METRIC ID:",
        latestMetrics[0]?.id
      );

      setMetrics(latestMetrics);

      // DETECT ANOMALIES

      const detectedAnomalies =
        latestMetrics.filter((metric: any) => {

          if (
            metric.metric_type === "CPU" &&
            metric.metric_value > 85
          ) {
            return true;
          }

          if (
            metric.metric_type === "MEMORY" &&
            metric.metric_value > 90
          ) {
            return true;
          }

          if (
            metric.metric_type === "DISK" &&
            metric.metric_value > 80
          ) {
            return true;
          }

          if (
            metric.metric_type === "NETWORK" &&
            metric.metric_value > 95
          ) {
            return true;
          }

          return false;
        });

      setAnomalies(detectedAnomalies);

    } catch (error) {

      console.error(
        "Metric Fetch Error:",
        error
      );

    }
  };

  // INITIAL LOAD + POLLING

  useEffect(() => {

    fetchIncidents();
    fetchMetrics();

    const interval = setInterval(() => {

      fetchIncidents();
      fetchMetrics();

    }, 5000);

    return () => clearInterval(interval);

  }, []);

  // WEBSOCKET

  useEffect(() => {

    const socket = new WebSocket(
      "ws://localhost:8000/ws/metrics/"
    );

    socket.onopen = () => {

      console.log(
        "WEBSOCKET CONNECTED"
      );

    };

    socket.onmessage = (event) => {

      const data = JSON.parse(event.data);

      console.log(
        "LIVE METRIC:",
        data
      );

    };

    socket.onerror = (error) => {

      console.log(
        "WEBSOCKET ERROR:",
        error
      );

    };

    socket.onclose = () => {

      console.log(
        "WEBSOCKET CLOSED"
      );

    };

    return () => {

      socket.close();

    };

  }, []);

  // INCIDENT PIE DATA

  const severityData = [
    {
      name: "Critical",
      value: incidents.filter(
        (i: any) => i.severity === "CRITICAL"
      ).length,
    },

    {
      name: "High",
      value: incidents.filter(
        (i: any) => i.severity === "HIGH"
      ).length,
    },

    {
      name: "Medium",
      value: incidents.filter(
        (i: any) => i.severity === "MEDIUM"
      ).length,
    },

    {
      name: "Low",
      value: incidents.filter(
        (i: any) => i.severity === "LOW"
      ).length,
    },
  ];

  // PIE COLORS

  const chartColors = [
    "#ef4444",
    "#f97316",
    "#eab308",
    "#22c55e",
  ];

  // CPU METRICS

  const cpuMetrics = metrics
    .filter(
      (metric: any) =>
        metric.metric_type === "CPU"
    )
    .slice(0, 10)
    .map((metric: any, index: number) => ({
      name: `${index + 1}`,
      value: Number(metric.metric_value),
    }));

  // MEMORY METRICS

  const memoryMetrics = metrics
    .filter(
      (metric: any) =>
        metric.metric_type === "MEMORY"
    )
    .slice(0, 10)
    .map((metric: any, index: number) => ({
      name: `${index + 1}`,
      value: Number(metric.metric_value),
    }));

  return (

    <div
      style={{
        backgroundColor: "#0f172a",
        minHeight: "100vh",
        color: "white",
        padding: "30px",
        fontFamily: "Arial",
      }}
    >

      {/* HEADER */}

      <div
        style={{
          textAlign: "center",
          marginBottom: "40px",
        }}
      >

        <h1
          style={{
            fontSize: "55px",
            marginBottom: "5px",
          }}
        >
          AIOps Incident Dashboard
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: "20px",
          }}
        >
          Real-Time Infrastructure Monitoring
        </p>

      </div>

      {/* TOP CHARTS */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "30px",
          marginBottom: "40px",
        }}
      >

        {/* INCIDENT PIE */}

        <ChartCard title="Incident Severity Distribution">

          <ResponsiveContainer
            width="100%"
            height={300}
          >

            <PieChart>

              <Pie
                data={severityData}
                dataKey="value"
                nameKey="name"
                outerRadius={100}
                label
              >

                {severityData.map((_, index) => (

                  <Cell
                    key={index}
                    fill={
                      chartColors[
                        index %
                          chartColors.length
                      ]
                    }
                  />

                ))}

              </Pie>

              <Tooltip />

            </PieChart>

          </ResponsiveContainer>

        </ChartCard>

        {/* CPU CHART */}

        <ChartCard title="CPU Usage Trends">

          <ResponsiveContainer
            width="100%"
            height={300}
          >

            <LineChart data={cpuMetrics}>

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                dataKey="name"
                stroke="#ffffff"
              />

              <YAxis
                stroke="#ffffff"
              />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="value"
                stroke="#ef4444"
                strokeWidth={3}
              />

            </LineChart>

          </ResponsiveContainer>

        </ChartCard>

      </div>

      {/* SECOND ROW */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "30px",
          marginBottom: "50px",
        }}
      >

        {/* MEMORY CHART */}

        <ChartCard title="Memory Usage Trends">

          <ResponsiveContainer
            width="100%"
            height={300}
          >

            <BarChart data={memoryMetrics}>

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                dataKey="name"
                stroke="#ffffff"
              />

              <YAxis
                stroke="#ffffff"
              />

              <Tooltip />

              <Bar
                dataKey="value"
                fill="#3b82f6"
              />

            </BarChart>

          </ResponsiveContainer>

        </ChartCard>

        {/* METRIC PANEL */}

        <ChartCard title="Infrastructure Metrics">

          <div
            style={{
              padding: "20px",
            }}
          >

            <MetricRow
              label="Latest Metric ID"
              value={
                metrics.length > 0
                  ? metrics[0].id
                  : "Loading..."
              }
            />

            <MetricRow
              label="CPU Metrics"
              value={
                metrics.filter(
                  (m) =>
                    m.metric_type === "CPU"
                ).length
              }
            />

            <MetricRow
              label="Memory Metrics"
              value={
                metrics.filter(
                  (m) =>
                    m.metric_type ===
                    "MEMORY"
                ).length
              }
            />

            <MetricRow
              label="Network Metrics"
              value={
                metrics.filter(
                  (m) =>
                    m.metric_type ===
                    "NETWORK"
                ).length
              }
            />

          </div>

        </ChartCard>

      </div>

      {/* ANOMALIES */}

      <ChartCard title="Live Anomaly Alerts">

        <div
          style={{
            maxHeight: "400px",
            overflowY: "auto",
          }}
        >

          {anomalies.length === 0 && (

            <p
              style={{
                color: "#94a3b8",
                textAlign: "center",
              }}
            >
              No anomalies detected
            </p>

          )}

          {anomalies.map(
            (anomaly: any, index: number) => (

              <div
                key={index}
                style={{
                  backgroundColor:
                    "#7f1d1d",
                  border:
                    "2px solid #ef4444",
                  padding: "15px",
                  borderRadius: "12px",
                  marginBottom: "15px",
                }}
              >

                <h3
                  style={{
                    color: "#fecaca",
                  }}
                >
                  ANOMALY DETECTED
                </h3>

                <p>
                  <strong>Host:</strong>{" "}
                  {anomaly.hostname}
                </p>

                <p>
                  <strong>Service:</strong>{" "}
                  {anomaly.service_name}
                </p>

                <p>
                  <strong>Metric:</strong>{" "}
                  {anomaly.metric_type}
                </p>

                <p>
                  <strong>Value:</strong>{" "}
                  {anomaly.metric_value}
                </p>

              </div>

            )
          )}

        </div>

      </ChartCard>

    </div>

  );
}

// CHART CARD

function ChartCard({
  title,
  children,
}: any) {

  return (

    <div
      style={{
        backgroundColor: "#1e293b",
        padding: "20px",
        borderRadius: "15px",
        marginBottom: "30px",
      }}
    >

      <h2
        style={{
          textAlign: "center",
          marginBottom: "20px",
        }}
      >
        {title}
      </h2>

      {children}

    </div>

  );
}

// METRIC ROW

function MetricRow({
  label,
  value,
}: any) {

  return (

    <div
      style={{
        display: "flex",
        justifyContent:
          "space-between",
        padding: "15px 0",
        borderBottom:
          "1px solid #334155",
        fontSize: "20px",
      }}
    >

      <span>{label}</span>

      <strong>{value}</strong>

    </div>

  );
}

export default App;