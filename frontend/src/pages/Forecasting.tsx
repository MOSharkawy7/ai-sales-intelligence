import { useEffect, useMemo, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import { DollarSign, TrendingUp, CalendarDays } from "lucide-react";
import { getForecast, getSalesTrends } from "../api";

interface ForecastItem {
  date: string;
  predicted_sales: number;
}

interface HistoricalItem {
  date: string;
  sales: number;
}

interface ChartItem {
  date: string;
  historical?: number;
  forecast?: number;
}

export default function Forecasting() {
  const [days, setDays] = useState(7);
  const [forecast, setForecast] = useState<ForecastItem[]>([]);
  const [historical, setHistorical] = useState<HistoricalItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    const loadData = async () => {
      try {
        setLoading(true);
        setError("");

        const [forecastData, historicalData] = await Promise.all([
          getForecast(days),
          getSalesTrends(),
        ]);

        if (!cancelled) {
          setForecast(forecastData);
          setHistorical(historicalData);
        }
      } catch (error) {
        console.error("Forecasting page error:", error);

        if (!cancelled) {
          setError("Failed to load forecasting data.");
          setForecast([]);
          setHistorical([]);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    loadData();

    return () => {
      cancelled = true;
    };
  }, [days]);

  const totalForecast = useMemo(() => {
    return forecast.reduce(
      (total, item) => total + Number(item.predicted_sales || 0),
      0
    );
  }, [forecast]);

  const averageForecast = useMemo(() => {
    return forecast.length > 0 ? totalForecast / forecast.length : 0;
  }, [forecast, totalForecast]);

  const highestForecast = useMemo(() => {
    if (forecast.length === 0) {
      return null;
    }

    return forecast.reduce((highest, current) =>
      current.predicted_sales > highest.predicted_sales
        ? current
        : highest
    );
  }, [forecast]);

  const chartData = useMemo<ChartItem[]>(() => {
    const recentHistorical = historical.slice(-14).map((item) => ({
      date: item.date,
      historical: Number(item.sales),
    }));

    const forecastData = forecast.map((item) => ({
      date: item.date,
      forecast: Number(item.predicted_sales),
    }));

    return [...recentHistorical, ...forecastData];
  }, [historical, forecast]);

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Sales Forecasting</h1>
          <p>
            Predicted sales based on historical sales patterns.
          </p>
        </div>

        <select
          className="select-input"
          value={days}
          onChange={(e) => setDays(Number(e.target.value))}
        >
          <option value={7}>Next 7 days</option>
          <option value={14}>Next 14 days</option>
          <option value={30}>Next 30 days</option>
        </select>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading forecast...</div>
      ) : (
        <>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">
                <DollarSign size={20} />
              </div>

              <span>Total Predicted Sales</span>

              <strong>
                ${totalForecast.toLocaleString(undefined, {
                  maximumFractionDigits: 0,
                })}
              </strong>

              <small>
                Next {days} days
              </small>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <TrendingUp size={20} />
              </div>

              <span>Average Daily Sales</span>

              <strong>
                ${averageForecast.toLocaleString(undefined, {
                  maximumFractionDigits: 0,
                })}
              </strong>

              <small>
                Predicted daily average
              </small>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <CalendarDays size={20} />
              </div>

              <span>Highest Predicted Day</span>

              <strong>
                {highestForecast
                  ? `$${highestForecast.predicted_sales.toLocaleString(
                      undefined,
                      {
                        maximumFractionDigits: 0,
                      }
                    )}`
                  : "$0"}
              </strong>

              <small>
                {highestForecast
                  ? highestForecast.date
                  : "No forecast available"}
              </small>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <TrendingUp size={20} />
              </div>

              <span>Forecast Horizon</span>

              <strong>{days} Days</strong>

              <small>
                Machine learning prediction
              </small>
            </div>
          </div>

          <div className="chart-card full-width">
            <h2>Historical vs Predicted Sales</h2>

            <div className="chart-container chart-large">
              {chartData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={chartData}
                    margin={{
                      top: 10,
                      right: 20,
                      left: 10,
                      bottom: 10,
                    }}
                  >
                    <CartesianGrid stroke="#e5e7eb" />

                    <XAxis
                      dataKey="date"
                      tick={{
                        fill: "#6b7280",
                        fontSize: 11,
                      }}
                    />

                    <YAxis
                      tick={{
                        fill: "#6b7280",
                        fontSize: 11,
                      }}
                    />

                    <Tooltip
                      formatter={(value, name) => [
                        `$${Number(value ?? 0).toLocaleString()}`,
                        name === "historical"
                          ? "Historical Sales"
                          : "Predicted Sales",
                      ]}
                    />

                    <ReferenceLine
                      x={historical[historical.length - 1]?.date}
                      stroke="#9ca3af"
                      strokeDasharray="5 5"
                    />

                    <Line
                      type="monotone"
                      dataKey="historical"
                      name="Historical Sales"
                      stroke="#111827"
                      strokeWidth={2}
                      dot={false}
                      connectNulls
                    />

                    <Line
                      type="monotone"
                      dataKey="forecast"
                      name="Predicted Sales"
                      stroke="#2563eb"
                      strokeWidth={3}
                      dot={{ r: 4 }}
                      activeDot={{ r: 6 }}
                      connectNulls
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="loading">
                  No forecast data available.
                </div>
              )}
            </div>
          </div>

          <div className="table-card">
            <h2>Forecast Details</h2>

            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Predicted Sales</th>
                  </tr>
                </thead>

                <tbody>
                  {forecast.map((item) => (
                    <tr key={item.date}>
                      <td>{item.date}</td>
                      <td>
                        $
                        {Number(
                          item.predicted_sales
                        ).toLocaleString(undefined, {
                          maximumFractionDigits: 2,
                        })}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}