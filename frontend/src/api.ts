import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export const getSalesSummary = async () => {
  const response = await api.get("/sales/summary");
  return response.data;
};

export const getSalesTrends = async () => {
  const response = await api.get("/sales/trends");
  return response.data;
};

export const getSalesCategories = async () => {
  const response = await api.get("/sales/categories");
  return response.data;
};

export const getSalesRegions = async () => {
  const response = await api.get("/sales/regions");
  return response.data;
};

export const getCustomers = async () => {
  const response = await api.get("/customers/");
  return response.data;
};

export const getCustomerSegments = async () => {
  const response = await api.get("/customers/segments");
  return response.data;
};

export const getAnomalies = async () => {
  const response = await api.get("/anomalies/");
  return response.data;
};

export const getAnomalySummary = async () => {
  const response = await api.get("/anomalies/summary");
  return response.data;
};

export const getForecast = async (days: number = 7) => {
  const response = await api.get(`/sales/forecast?days=${days}`);
  return response.data;
};