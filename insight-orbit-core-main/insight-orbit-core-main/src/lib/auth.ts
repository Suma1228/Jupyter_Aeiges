import { jwtDecode } from "jwt-decode";

type TokenPayload = {
  sub: string;
  role: "CUSTOMER" | "OPS";
  name: string;
  exp: number;
};

export function getToken() {
  return localStorage.getItem("access_token");
}

export function getRole() {
  const token = getToken();
  if (!token) return null;

  try {
    const decoded = jwtDecode(token);
    return decoded.role;
  } catch {
    return null;
  }
}

export function isOps() {
  return getRole() === "OPS";
}

export function isCustomer() {
  return getRole() === "CUSTOMER";
}