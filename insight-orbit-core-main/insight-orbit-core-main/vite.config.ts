import { defineConfig } from "@lovable.dev/vite-tanstack-config";

export default defineConfig({
  vite: {
    base: "/jupyter-hack-team-2671-260612052841-847ec4b2/proxy/3000/",
    server: {
      allowedHosts: "all",
    },
  },
  tanstackStart: {
    server: { entry: "server" },
    routers: {
      client: {
        base: "/jupyter-hack-team-2671-260612052841-847ec4b2/proxy/3000/",
      },
      ssr: {
        base: "/jupyter-hack-team-2671-260612052841-847ec4b2/proxy/3000/",
      },
    },
  },
});
