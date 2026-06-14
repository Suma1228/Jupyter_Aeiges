// src/lib/api/auth.api.ts
import apiClient from "./client";

export const login = async (email: string, password: string) => {
  const { data } = await apiClient.post("/api/auth/login", { email, password });
  localStorage.setItem("access_token", data.access_token);
  return data;
};

export const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user_role");
};

export const logout = () => {
  localStorage.removeItem("access_token");
};
