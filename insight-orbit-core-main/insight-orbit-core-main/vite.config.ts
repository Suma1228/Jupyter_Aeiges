import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

const JUPYTER_BASE = process.env.JUPYTER_BASE_PATH || "/";

export default defineConfig({
  plugins: [react()],
  base: JUPYTER_BASE,
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
    allowedHosts: "all",
  },
});
