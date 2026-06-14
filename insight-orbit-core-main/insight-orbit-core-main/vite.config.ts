import { defineConfig } from "@lovable.dev/vite-tanstack-config";

const JUPYTER_BASE = process.env.JUPYTER_BASE_PATH || "/";

export default defineConfig({
  vite: {
    base: JUPYTER_BASE,
    server: { allowedHosts: "all" },
  },
  tanstackStart: {
    server: { entry: "server" },
    routers: {
      client: { base: JUPYTER_BASE },
      ssr:    { base: JUPYTER_BASE },
    },
  },
});
