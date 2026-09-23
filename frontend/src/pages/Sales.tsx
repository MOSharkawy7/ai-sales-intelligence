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
} from "lucide-react";

import {
  getSalesSummary,
  getSalesTrends,
  getSalesCategories,
  getSalesRegions,
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

export default function Sales() {
  const [summary, setSummary] = useState<SalesSummary | null>(null);
  const [trends, setTrends] = useState<SalesTrend[]>([]);
  const [categories, setCategories] = useState<CategorySales[]>([]);
  const [regions, setRegions] = useState<RegionSales[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadSales = async () => {
      try {
        setLoading(true);
        setError("");

        const [
          summaryData,
          trendData,
          categoryData,
          regionData,
        ] = await Promise.all([
          getSalesSummary(),
          getSalesTrends(),
          getSalesCategories(),
          getSalesRegions(),
        ]);

        setSummary(summaryData);
        setTrends(trendData);
        setCategories(categoryData);
        setRegions(regionData);
      } catch (error) {
        console.error("Sales error:", error);
        setError("Failed to load sales data.");
      } finally {
        setLoading(false);
      }
    };

    loadSales();
  }, []);

  if (loading) {
    return (
      <div className="page">
        <div className="loading">Loading sales data...</div>
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
          <h1>Sales Analytics</h1>

          <p>
            Detailed analysis of sales performance across products and regions.
          </p>
        </div>
      </div>

      {/* KPI CARDS */}

      <div className="stats-grid">

        <div className="stat-card">
          <div className="stat-icon">
            <DollarSign size={22} />
          </div>

          <span>Total Revenue</span>

          <strong>
            ${summary?.total_sales.toLocaleString()}
          </strong>

          <small>
            Total sales generated
          </small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <ShoppingCart size={22} />
          </div>

          <span>Total Orders</span>

          <strong>
            {summary?.total_orders.toLocaleString()}
          </strong>

          <small>
            Completed transactions
          </small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Package size={22} />
          </div>

          <span>Units Sold</span>

          <strong>
            {summary?.total_quantity.toLocaleString()}
          </strong>

          <small>
            Products sold
          </small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <TrendingUp size={22} />
          </div>

          <span>Average Order Value</span>

          <strong>
            ${summary?.average_order_value.toLocaleString()}
          </strong>

          <small>
            Revenue per order
          </small>
        </div>

      </div>

      {/* SALES TREND */}

      <div className="chart-card full-width">

        <h2>Sales Over Time</h2>

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

      {/* CATEGORY + REGION */}

      <div className="charts-grid">

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