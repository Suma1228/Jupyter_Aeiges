// src/lib/api/complaints.api.ts
import apiClient from "./client";

export interface Complaint {
  id: number;
  title: string;
  description: string;
  status: string;
  category?: string;
  created_at: string;
}

export interface RaiseComplaintPayload {
  title: string;
  description: string;
}

// Customer APIs
export const raiseComplaint = async (payload) => {
  console.log("RAISE COMPLAINT CALLED");
  const { data } = await apiClient.post("/api/complaints", payload);
  return data;
};

export const getMyComplaints = async (): Promise<Complaint[]> => {
  const { data } = await apiClient.get("/api/complaints/my");
  return data;
};

export const trackComplaint = async (id: number): Promise<Complaint> => {
  const { data } = await apiClient.get(`/api/complaints/${id}`);
  return data;
};

// Ops APIs
export const getAllComplaints = async (): Promise<Complaint[]> => {
  const { data } = await apiClient.get("/api/ops/complaints");
  return data;
};

export const getInsights = async () => {
  const { data } = await apiClient.get("/api/ops/dashboard");
  return data;
};
