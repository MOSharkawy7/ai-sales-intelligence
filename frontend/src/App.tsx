import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import type { ReactNode } from "react";

import {
  LayoutDashboard,
  ShoppingCart,
  Users,
  TrendingUp,
  AlertTriangle,
  Brain,
} from "lucide-react";

import Dashboard from "./pages/Dashboard";
import Sales from "./pages/Sales";
import Customers from "./pages/Customers";
import Forecasting from "./pages/Forecasting";
import Anomalies from "./pages/Anomalies";

import "./App.css";

interface LayoutProps {
  children: ReactNode;
}

function Layout({ children }: LayoutProps) {
  const navigation = [
    {
      name: "Dashboard",
      path: "/",
      icon: LayoutDashboard,
    },
    {
      name: "Sales",
      path: "/sales",
      icon: ShoppingCart,
    },
    {
      name: "Customers",
      path: "/customers",
      icon: Users,
    },
    {
      name: "Forecasting",
      path: "/forecasting",
      icon: TrendingUp,
    },
    {
      name: "Anomalies",
      path: "/anomalies",
      icon: AlertTriangle,
    },
  ];

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <Brain size={28} />
          <span>SalesAI</span>
        </div>

        <nav>
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === "/"}
                className={({ isActive }) =>
                  isActive ? "nav-link active" : "nav-link"
                }
              >
                <Icon size={20} />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <span>AI Sales Intelligence</span>
          <small>v1.0.0</small>
        </div>
      </aside>

      <main className="main-content">
        {children}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/sales" element={<Sales />} />
          <Route path="/customers" element={<Customers />} />
          <Route path="/forecasting" element={<Forecasting />} />
          <Route path="/anomalies" element={<Anomalies />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}