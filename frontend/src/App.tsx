import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import {
  getSalesSummary,
  getSalesTrends,
  getCustomerSegments,
  getAnomalySummary,
  getForecast,
} from "./api";

import "./App.css";

interface SalesSummary {
  total_sales: number;
  total_orders: number;
  total_quantity: number;
  average_order_value: number;
}

interface SalesTrend {
  date: string;
  sales: number;
}

interface CustomerSegment {
  segment: string;
  customer_count: number;
  total_spend: number;
  average_order_value: number;
}

interface AnomalySummary {
  total_anomalies: number;
}

interface Forecast {
  date: string;
  predicted_sales: number;
}

function App() {
  const [summary, setSummary] = useState<SalesSummary | null>(null);
  const [trends, setTrends] = useState<SalesTrend[]>([]);
  const [segments, setSegments] = useState<CustomerSegment[]>([]);
  const [anomalies, setAnomalies] = useState<AnomalySummary | null>(null);
  const [forecast, setForecast] = useState<Forecast[]>([]);

  const [loading, setLoading] = useState(true);
  const [forecastLoading, setForecastLoading] = useState(true);
  const [forecastError, setForecastError] = useState(false);

  useEffect(() => {
    const loadDashboard = async () => {
      setLoading(true);

      try {
        /*
         * Load the main dashboard data first.
         *
         * We intentionally don't include the forecast request here.
         * If forecasting fails, the rest of the dashboard should still work.
         */
        const [
          summaryData,
          trendsData,
          segmentsData,
          anomalyData,
        ] = await Promise.all([
          getSalesSummary(),
          getSalesTrends(),
          getCustomerSegments(),
          getAnomalySummary(),
        ]);

        setSummary(summaryData);
        setTrends(trendsData);
        setSegments(segmentsData);
        setAnomalies(anomalyData);
      } catch (error) {
        console.error("Failed to load dashboard:", error);
      } finally {
        setLoading(false);
      }

      /*
       * Load forecast separately.
       *
       * If the backend forecast endpoint currently has an error,
       * the rest of the dashboard will still be displayed.
       */
      try {
        setForecastLoading(true);
        setForecastError(false);

        const forecastData = await getForecast(7);

        setForecast(forecastData);
      } catch (error) {
        console.error("Failed to load forecast:", error);

        setForecast([]);
        setForecastError(true);
      } finally {
        setForecastLoading(false);
      }
    };

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="app-loading">
        <h2>Loading dashboard...</h2>
        <p>Connecting to AI Sales Intelligence API</p>
      </div>
    );
  }

  return (
    <div className="app">
      {/* =========================
          SIDEBAR
      ========================== */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <div className="logo-icon">AI</div>

          <div>
            <h2>Sales AI</h2>
            <span>Intelligence Platform</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <div className="nav-item active">
            <span>📊</span>
            Dashboard
          </div>

          <div className="nav-item">
            <span>💰</span>
            Sales
          </div>

          <div className="nav-item">
            <span>👥</span>
            Customers
          </div>

          <div className="nav-item">
            <span>📈</span>
            Forecast
          </div>

          <div className="nav-item">
            <span>⚠️</span>
            Anomalies
          </div>
        </nav>

        <div className="sidebar-footer">
          <span>AI Sales Intelligence</span>
          <small>v1.0.0</small>
        </div>
      </aside>

      {/* =========================
          MAIN CONTENT
      ========================== */}
      <main className="main-content">
        {/* Header */}
        <header className="dashboard-header">
          <div>
            <h1>Sales Dashboard</h1>
            <p>
              AI-powered insights into your sales performance
            </p>
          </div>

          <div className="header-status">
            <span className="status-dot"></span>
            API Connected
          </div>
        </header>

        {/* =========================
            KPI CARDS
        ========================== */}
        <section className="kpi-grid">
          <div className="kpi-card">
            <div className="kpi-header">
              <span>Total Sales</span>
              <div className="kpi-icon">💰</div>
            </div>

            <h2>
              $
              {summary
                ? summary.total_sales.toLocaleString(undefined, {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })
                : "0.00"}
            </h2>

            <p className="kpi-description">
              Total revenue generated
            </p>
          </div>

          <div className="kpi-card">
            <div className="kpi-header">
              <span>Total Orders</span>
              <div className="kpi-icon">🛒</div>
            </div>

            <h2>
              {summary
                ? summary.total_orders.toLocaleString()
                : "0"}
            </h2>

            <p className="kpi-description">
              Number of orders
            </p>
          </div>

          <div className="kpi-card">
            <div className="kpi-header">
              <span>Total Quantity</span>
              <div className="kpi-icon">📦</div>
            </div>

            <h2>
              {summary
                ? summary.total_quantity.toLocaleString()
                : "0"}
            </h2>

            <p className="kpi-description">
              Products sold
            </p>
          </div>

          <div className="kpi-card">
            <div className="kpi-header">
              <span>Average Order Value</span>
              <div className="kpi-icon">📊</div>
            </div>

            <h2>
              $
              {summary
                ? summary.average_order_value.toLocaleString(undefined, {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })
                : "0.00"}
            </h2>

            <p className="kpi-description">
              Average revenue per order
            </p>
          </div>
        </section>

        {/* =========================
            CHARTS ROW
        ========================== */}
        <section className="charts-grid">
          {/* Sales Trend */}
          <div className="dashboard-card large-card">
            <div className="card-header">
              <div>
                <h3>Sales Trend</h3>
                <p>Daily sales performance</p>
              </div>
            </div>

            <div className="chart-container">
              {trends.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={trends}>
                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis
                      dataKey="date"
                      tickFormatter={(value) =>
                        new Date(value).toLocaleDateString()
                      }
                    />

                    <YAxis />

                    <Tooltip
                      formatter={(value: number | undefined) => [
                        `$${Number(value ?? 0).toLocaleString(undefined, {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2,
                        })}`,
                        "Sales",
                      ]}
                    />

                    <Line
                      type="monotone"
                      dataKey="sales"
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="empty-state">
                  No sales trend data available
                </div>
              )}
            </div>
          </div>

          {/* Customer Segments */}
          <div className="dashboard-card">
            <div className="card-header">
              <div>
                <h3>Customer Segments</h3>
                <p>Customer distribution</p>
              </div>
            </div>

            <div className="chart-container">
              {segments.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={segments}>
                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis dataKey="segment" />

                    <YAxis />

                    <Tooltip />

                    <Bar
                      dataKey="customer_count"
                      name="Customers"
                    />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="empty-state">
                  No customer segment data available
                </div>
              )}
            </div>
          </div>
        </section>

        {/* =========================
            AI INSIGHTS
        ========================== */}
        <section className="dashboard-card insights-card">
          <div className="card-header">
            <div>
              <h3>AI Insights</h3>
              <p>Automated intelligence from your sales data</p>
            </div>

            <div className="ai-badge">
              ✨ AI Powered
            </div>
          </div>

          <div className="insights-grid">
            {/* Anomalies */}
            <div className="insight-item">
              <div className="insight-icon warning">
                ⚠️
              </div>

              <div>
                <h4>Sales Anomalies</h4>

                <p>
                  {anomalies
                    ? `${anomalies.total_anomalies} potential anomalies detected`
                    : "No anomaly data available"}
                </p>
              </div>
            </div>

            {/* Forecast */}
            <div className="insight-item">
              <div className="insight-icon forecast">
                📈
              </div>

              <div>
                <h4>Sales Forecast</h4>

                {forecastLoading ? (
                  <p>Generating forecast...</p>
                ) : forecastError ? (
                  <p>
                    Forecast service is currently unavailable
                  </p>
                ) : forecast.length > 0 ? (
                  <p>
                    Forecast generated for the next{" "}
                    {forecast.length} days
                  </p>
                ) : (
                  <p>No forecast data available</p>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* =========================
            FORECAST CHART
        ========================== */}
        <section className="dashboard-card">
          <div className="card-header">
            <div>
              <h3>Sales Forecast</h3>
              <p>Predicted sales for the next 7 days</p>
            </div>
          </div>

          <div className="chart-container">
            {forecastLoading ? (
              <div className="empty-state">
                Generating AI forecast...
              </div>
            ) : forecastError ? (
              <div className="forecast-error">
                <div className="forecast-error-icon">
                  ⚠️
                </div>

                <h3>Forecast temporarily unavailable</h3>

                <p>
                  The forecasting API returned an error.
                  Your other dashboard data is still working.
                </p>

                <small>
                  Check the FastAPI terminal for the forecast
                  endpoint error.
                </small>
              </div>
            ) : forecast.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={forecast}>
                  <CartesianGrid strokeDasharray="3 3" />

                  <XAxis
                    dataKey="date"
                    tickFormatter={(value) =>
                      new Date(value).toLocaleDateString()
                    }
                  />

                  <YAxis />

                  <Tooltip
                    formatter={(value: number | undefined) => [
                      `$${Number(value ?? 0).toLocaleString(undefined, {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      })}`,
                      "Predicted Sales",
                    ]}
                  />

                  <Line
                    type="monotone"
                    dataKey="predicted_sales"
                    strokeWidth={3}
                    dot={{ r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="empty-state">
                No forecast data available
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;