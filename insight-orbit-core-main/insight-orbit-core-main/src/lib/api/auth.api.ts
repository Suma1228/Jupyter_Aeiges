// src/lib/api/auth.api.ts
import apiClient from "./client";

export const login = async (username: string, password: string) => {
  // FastAPI OAuth2 expects form data, not JSON
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const { data } = await apiClient.post("/auth/token", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  localStorage.setItem("access_token", data.access_token);
  return data;
};

export const logout = () => {
  localStorage.removeItem("access_token");
};