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
  DollarSign,
  ShoppingCart,
  Package,
  TrendingUp,
  AlertTriangle,
} from "lucide-react";

import {
  getSalesSummary,
  getSalesTrends,
  getSalesCategories,
  getSalesRegions,
  getAnomalySummary,
} from "../api";

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

interface CategorySales {
  category: string;
  sales: number;
}

interface RegionSales {
  region: string;
  sales: number;
}

interface AnomalySummary {
  total_anomalies: number;
}

export default function Dashboard() {
  const [summary, setSummary] = useState<SalesSummary | null>(null);
  const [trends, setTrends] = useState<SalesTrend[]>([]);
  const [categories, setCategories] = useState<CategorySales[]>([]);
  const [regions, setRegions] = useState<RegionSales[]>([]);
  const [anomalies, setAnomalies] = useState<AnomalySummary | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        setLoading(true);
        setError("");

        const [
          summaryData,
          trendData,
          categoryData,
          regionData,
          anomalyData,
        ] = await Promise.all([
          getSalesSummary(),
          getSalesTrends(),
          getSalesCategories(),
          getSalesRegions(),
          getAnomalySummary(),
        ]);

        setSummary(summaryData);
        setTrends(trendData);
        setCategories(categoryData);
        setRegions(regionData);
        setAnomalies(anomalyData);
      } catch (error) {
        console.error("Dashboard error:", error);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="page">
        <div className="loading">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="page">

      {/* HEADER */}

      <div className="page-header">
        <div>
          <h1>Dashboard</h1>

          <p>
            Overview of your sales performance and AI-powered insights.
          </p>
        </div>
      </div>

      {/* KPI CARDS */}

      <div className="stats-grid">

        <div className="stat-card">
          <div className="stat-icon">
            <DollarSign size={22} />
          </div>

          <span>Total Sales</span>

          <strong>
            ${summary?.total_sales.toLocaleString()}
          </strong>

          <small>Revenue generated</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <ShoppingCart size={22} />
          </div>

          <span>Total Orders</span>

          <strong>
            {summary?.total_orders.toLocaleString()}
          </strong>

          <small>Orders processed</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Package size={22} />
          </div>

          <span>Total Quantity</span>

          <strong>
            {summary?.total_quantity.toLocaleString()}
          </strong>

          <small>Products sold</small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <TrendingUp size={22} />
          </div>

          <span>Average Order Value</span>

          <strong>
            ${summary?.average_order_value.toLocaleString()}
          </strong>

          <small>Average revenue per order</small>
        </div>

      </div>

      {/* ANOMALY ALERT */}

      <div className="insight-card">

        <div className="insight-icon">
          <AlertTriangle size={22} />
        </div>

        <div>
          <strong>
            AI Anomaly Detection
          </strong>

          <p>
            The ML model identified{" "}
            <b>{anomalies?.total_anomalies ?? 0}</b>{" "}
            potentially unusual transactions.
          </p>
        </div>

      </div>

      {/* CHARTS */}

      <div className="charts-grid">

        {/* SALES TREND */}

        <div className="chart-card full-width">

          <h2>Sales Trend</h2>

          <div className="chart-container chart-large">

            <ResponsiveContainer width="100%" height="100%">

              <LineChart
                data={trends}
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
                  formatter={(value) => [
                    `$${Number(value ?? 0).toLocaleString()}`,
                    "Sales",
                  ]}
                />

                <Line
                  type="monotone"
                  dataKey="sales"
                  stroke="#2563eb"
                  strokeWidth={3}
                  dot={false}
                  activeDot={{ r: 5 }}
                />

              </LineChart>

            </ResponsiveContainer>

          </div>

        </div>

        {/* CATEGORY */}

        <div className="chart-card">

          <h2>Sales by Category</h2>

          <div className="chart-container">

            <ResponsiveContainer width="100%" height="100%">

              <BarChart
                data={categories}
                margin={{
                  top: 10,
                  right: 10,
                  left: 0,
                  bottom: 10,
                }}
              >

                <CartesianGrid stroke="#e5e7eb" />

                <XAxis
                  dataKey="category"
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
                  formatter={(value) => [
                    `$${Number(value ?? 0).toLocaleString()}`,
                    "Sales",
                  ]}
                />

                <Bar
                  dataKey="sales"
                  fill="#2563eb"
                  radius={[4, 4, 0, 0]}
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

        {/* REGION */}

        <div className="chart-card">

          <h2>Sales by Region</h2>

          <div className="chart-container">

            <ResponsiveContainer width="100%" height="100%">

              <BarChart
                data={regions}
                margin={{
                  top: 10,
                  right: 10,
                  left: 0,
                  bottom: 10,
                }}
              >

                <CartesianGrid stroke="#e5e7eb" />

                <XAxis
                  dataKey="region"
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
                  formatter={(value) => [
                    `$${Number(value ?? 0).toLocaleString()}`,
                    "Sales",
                  ]}
                />

                <Bar
                  dataKey="sales"
                  fill="#111827"
                  radius={[4, 4, 0, 0]}
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

      </div>

    </div>
  );
}