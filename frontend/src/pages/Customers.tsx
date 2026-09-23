import { useEffect, useMemo, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Users, DollarSign, ShoppingCart } from "lucide-react";
import { getCustomers, getCustomerSegments } from "../api";

interface Customer {
  customer_id: string;
  total_spend: number;
  total_orders: number;
  total_quantity: number;
  average_order_value: number;
  average_discount: number;
  unique_products: number;
  unique_categories: number;
  segment: string;
}

interface CustomerSegment {
  segment: string;
  customer_count: number;
  total_spend: number;
  average_order_value: number;
}

export default function Customers() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [segments, setSegments] = useState<CustomerSegment[]>([]);

  const [search, setSearch] = useState("");
  const [selectedSegment, setSelectedSegment] = useState("All");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadCustomers = async () => {
      try {
        setLoading(true);
        setError("");

        const [customerData, segmentData] = await Promise.all([
          getCustomers(),
          getCustomerSegments(),
        ]);

        setCustomers(customerData);
        setSegments(segmentData);
      } catch (error) {
        console.error("Customers error:", error);
        setError("Failed to load customer data.");
      } finally {
        setLoading(false);
      }
    };

    loadCustomers();
  }, []);

  /*
   * Normalize segment names so filtering still works
   * even if there are differences in spaces/capitalization.
   */
  const normalizeSegment = (value: unknown) => {
    return String(value ?? "")
      .trim()
      .toLowerCase()
      .replace(/[\s_-]+/g, "");
  };

  const filteredCustomers = useMemo(() => {
    const normalizedSearch = search.trim().toLowerCase();
    const normalizedSelectedSegment =
      normalizeSegment(selectedSegment);

    return customers.filter((customer) => {
      const matchesSearch =
        normalizedSearch === "" ||
        customer.customer_id
          .toLowerCase()
          .includes(normalizedSearch);

      const matchesSegment =
        normalizedSelectedSegment === "all" ||
        normalizeSegment(customer.segment) ===
          normalizedSelectedSegment;

      return matchesSearch && matchesSegment;
    });
  }, [customers, search, selectedSegment]);

  const totalCustomers = customers.length;

  const totalCustomerSpend = customers.reduce(
    (sum, customer) => sum + customer.total_spend,
    0
  );

  const averageCustomerSpend =
    totalCustomers > 0
      ? totalCustomerSpend / totalCustomers
      : 0;

  if (loading) {
    return (
      <div className="page">
        <div className="loading">
          Loading customers...
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
          <h1>Customers</h1>

          <p>
            Customer behavior, value analysis, and AI-powered
            segmentation.
          </p>
        </div>
      </div>

      {/* KPI CARDS */}

      <div className="stats-grid">

        <div className="stat-card">
          <div className="stat-icon">
            <Users size={22} />
          </div>

          <span>Total Customers</span>

          <strong>
            {totalCustomers.toLocaleString()}
          </strong>

          <small>
            Unique customers
          </small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <DollarSign size={22} />
          </div>

          <span>Total Customer Spend</span>

          <strong>
            ${totalCustomerSpend.toLocaleString()}
          </strong>

          <small>
            Combined customer revenue
          </small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <ShoppingCart size={22} />
          </div>

          <span>Average Customer Spend</span>

          <strong>
            ${averageCustomerSpend.toLocaleString()}
          </strong>

          <small>
            Average spend per customer
          </small>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Users size={22} />
          </div>

          <span>Customer Segments</span>

          <strong>
            {segments.length}
          </strong>

          <small>
            ML-generated groups
          </small>
        </div>

      </div>

      {/* SEGMENTATION CHART */}

      <div className="chart-card full-width">

        <h2>Customer Segmentation</h2>

        <div className="chart-container">

          <ResponsiveContainer
            width="100%"
            height="100%"
          >

            <BarChart
              data={segments}
              margin={{
                top: 10,
                right: 20,
                left: 10,
                bottom: 10,
              }}
            >

              <CartesianGrid stroke="#e5e7eb" />

              <XAxis
                dataKey="segment"
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
                  Number(value ?? 0).toLocaleString(),
                  name === "customer_count"
                    ? "Customers"
                    : "Spend",
                ]}
              />

              <Bar
                dataKey="customer_count"
                fill="#2563eb"
                radius={[4, 4, 0, 0]}
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>

      {/* SEGMENT CARDS */}

      <div className="segment-grid">

        {segments.map((segment) => (
          <div
            className="stat-card"
            key={segment.segment}
          >

            <span>
              {segment.segment}
            </span>

            <strong>
              {segment.customer_count.toLocaleString()}
            </strong>

            <small>
              ${segment.total_spend.toLocaleString()} total spend
            </small>

            <small>
              ${segment.average_order_value.toLocaleString()} avg order
            </small>

          </div>
        ))}

      </div>

      {/* CUSTOMER TABLE */}

      <div className="table-card">

        <div className="customer-table-header">

          <div>
            <h2>
              Customer Overview
            </h2>

            <p>
              Showing{" "}
              {filteredCustomers.length.toLocaleString()}{" "}
              of{" "}
              {customers.length.toLocaleString()}{" "}
              customers
            </p>
          </div>

          <div className="customer-filters">

            <input
              className="search-input"
              type="text"
              placeholder="Search customer..."
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
            />

            <select
              className="select-input"
              value={selectedSegment}
              onChange={(event) =>
                setSelectedSegment(event.target.value)
              }
            >

              <option value="All">
                All Segments
              </option>

              {segments.map((segment) => {
                const segmentName =
                  String(segment.segment).trim();

                return (
                  <option
                    key={segmentName}
                    value={segmentName}
                  >
                    {segmentName}
                  </option>
                );
              })}

            </select>

          </div>

        </div>

        <div className="table-container">

          <table>

            <thead>
              <tr>
                <th>Customer</th>
                <th>Segment</th>
                <th>Total Spend</th>
                <th>Orders</th>
                <th>Quantity</th>
                <th>Avg Order</th>
                <th>Products</th>
              </tr>
            </thead>

            <tbody>

              {filteredCustomers.map((customer) => (
                <tr key={customer.customer_id}>

                  <td>
                    <strong>
                      {customer.customer_id}
                    </strong>
                  </td>

                  <td>
                    <span className="badge">
                      {customer.segment}
                    </span>
                  </td>

                  <td>
                    ${customer.total_spend.toLocaleString()}
                  </td>

                  <td>
                    {customer.total_orders.toLocaleString()}
                  </td>

                  <td>
                    {customer.total_quantity.toLocaleString()}
                  </td>

                  <td>
                    ${customer.average_order_value.toLocaleString()}
                  </td>

                  <td>
                    {customer.unique_products}
                  </td>

                </tr>
              ))}

              {filteredCustomers.length === 0 && (
                <tr>
                  <td colSpan={7}>
                    No customers match your filters.
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