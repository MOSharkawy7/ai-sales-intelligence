import { useEffect, useMemo, useState } from "react";
import { AlertTriangle, DollarSign, Activity } from "lucide-react";
import { getAnomalies, getAnomalySummary } from "../api";

interface Anomaly {
  order_id: string;
  order_date: string;
  customer_id: string;
  product: string;
  quantity: number;
  unit_price: number;
  discount: number;
  sales: number;
  anomaly_score: number;
}

interface AnomalySummary {
  total_anomalies: number;
}

export default function Anomalies() {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [summary, setSummary] = useState<AnomalySummary | null>(null);

  const [search, setSearch] = useState("");
  const [severity, setSeverity] = useState("All");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadAnomalies = async () => {
      try {
        setLoading(true);
        setError("");

        const [anomalyData, summaryData] = await Promise.all([
          getAnomalies(),
          getAnomalySummary(),
        ]);

        setAnomalies(anomalyData);
        setSummary(summaryData);
      } catch (error) {
        console.error("Anomalies error:", error);
        setError("Failed to load anomaly data.");
      } finally {
        setLoading(false);
      }
    };

    loadAnomalies();
  }, []);

  /*
   * Isolation Forest produces lower scores for more unusual
   * transactions in this implementation.
   */
  const getSeverity = (score: number) => {
    if (score < -0.15) {
      return "High";
    }

    if (score < -0.05) {
      return "Medium";
    }

    return "Low";
  };

  const filteredAnomalies = useMemo(() => {
    const normalizedSearch = search.trim().toLowerCase();

    return anomalies.filter((item) => {
      const matchesSearch =
        normalizedSearch === "" ||
        item.order_id.toLowerCase().includes(normalizedSearch) ||
        item.customer_id.toLowerCase().includes(normalizedSearch) ||
        item.product.toLowerCase().includes(normalizedSearch);

      const matchesSeverity =
        severity === "All" ||
        getSeverity(item.anomaly_score) === severity;

      return matchesSearch && matchesSeverity;
    });
  }, [anomalies, search, severity]);

  const highSeverityCount = anomalies.filter(
    (item) => getSeverity(item.anomaly_score) === "High"
  ).length;

  const mediumSeverityCount = anomalies.filter(
    (item) => getSeverity(item.anomaly_score) === "Medium"
  ).length;

  const anomalyRevenue = anomalies.reduce(
    (sum, item) => sum + item.sales,
    0
  );

  if (loading) {
    return (
      <div className="page">
        <div className="loading">
          Loading anomaly data...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <div className="error-message">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="page">

      {/* HEADER */}

      <div className="page-header">
        <div>
          <h1>Anomaly Detection</h1>

          <p>
            Transactions identified as unusual by the
            machine learning model.
          </p>
        </div>
      </div>

      {/* KPI CARDS */}

      <div className="stats-grid">

        <div className="stat-card danger">
          <div className="stat-icon anomaly-high">
            <AlertTriangle size={22} />
          </div>

          <span>Detected Anomalies</span>

          <strong>
            {summary?.total_anomalies.toLocaleString() ?? "0"}
          </strong>

          <small>
            Unusual transactions
          </small>
        </div>

        <div className="stat-card">
          <div className="stat-icon anomaly-high">
            <Activity size={22} />
          </div>

          <span>High Severity</span>

          <strong>
            {highSeverityCount.toLocaleString()}
          </strong>

          <small>
            Strongest anomaly signals
          </small>
        </div>

        <div className="stat-card">
          <div className="stat-icon anomaly-medium">
            <AlertTriangle size={22} />
          </div>

          <span>Medium Severity</span>

          <strong>
            {mediumSeverityCount.toLocaleString()}
          </strong>

          <small>
            Moderate anomaly signals
          </small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <DollarSign size={22} />
          </div>

          <span>Anomalous Sales</span>

          <strong>
            ${anomalyRevenue.toLocaleString()}
          </strong>

          <small>
            Revenue from detected transactions
          </small>
        </div>

      </div>

      {/* ML EXPLANATION */}

      <div className="insight-card anomaly-insight">

        <div className="insight-icon">
          <Activity size={22} />
        </div>

        <div>
          <strong>
            Isolation Forest Detection
          </strong>

          <p>
            The model analyzes transaction features such as
            quantity, unit price, discount, and sales value to
            identify transactions that differ from normal
            patterns.
          </p>
        </div>

      </div>

      {/* FILTERS */}

      <div className="table-card">

        <div className="anomaly-table-header">

          <div>
            <h2>
              Detected Transactions
            </h2>

            <p>
              Showing{" "}
              {filteredAnomalies.length.toLocaleString()}{" "}
              of{" "}
              {anomalies.length.toLocaleString()}{" "}
              anomalies
            </p>
          </div>

          <div className="customer-filters">

            <input
              className="search-input"
              type="text"
              placeholder="Search order, customer, product..."
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
            />

            <select
              className="select-input"
              value={severity}
              onChange={(event) =>
                setSeverity(event.target.value)
              }
            >
              <option value="All">
                All Severity
              </option>

              <option value="High">
                High
              </option>

              <option value="Medium">
                Medium
              </option>

              <option value="Low">
                Low
              </option>
            </select>

          </div>

        </div>

        <div className="table-container">

          <table>

            <thead>
              <tr>
                <th>Order</th>
                <th>Date</th>
                <th>Customer</th>
                <th>Product</th>
                <th>Quantity</th>
                <th>Sales</th>
                <th>Score</th>
                <th>Severity</th>
              </tr>
            </thead>

            <tbody>

              {filteredAnomalies.map((item) => {
                const itemSeverity = getSeverity(
                  item.anomaly_score
                );

                return (
                  <tr key={item.order_id}>

                    <td>
                      <strong>
                        {item.order_id}
                      </strong>
                    </td>

                    <td>
                      {item.order_date}
                    </td>

                    <td>
                      {item.customer_id}
                    </td>

                    <td>
                      {item.product}
                    </td>

                    <td>
                      {item.quantity}
                    </td>

                    <td>
                      ${item.sales.toLocaleString()}
                    </td>

                    <td>
                      <span className="danger-score">
                        {item.anomaly_score.toFixed(4)}
                      </span>
                    </td>

                    <td>
                      <span
                        className={`severity-badge severity-${itemSeverity.toLowerCase()}`}
                      >
                        {itemSeverity}
                      </span>
                    </td>

                  </tr>
                );
              })}

              {filteredAnomalies.length === 0 && (
                <tr>
                  <td colSpan={8}>
                    No anomalies match your filters.
                  </td>
                </tr>
              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}