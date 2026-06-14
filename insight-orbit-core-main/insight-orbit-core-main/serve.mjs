import http from "http";
import fs from "fs";
import path from "path";

const BASE = process.env.JUPYTER_BASE_PATH?.replace(/\/$/, "") || "";
const DIST = "./dist/client";

const mime = {
  ".js": "application/javascript",
  ".css": "text/css",
  ".html": "text/html",
  ".json": "application/json",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".ico": "image/x-icon",
};

http.createServer((req, res) => {
  let url = req.url.replace(BASE, "") || "/";
  if (url === "/" || !url.includes(".")) url = "/index.html";
  
  const filePath = path.join(DIST, url);
  
  if (!fs.existsSync(filePath)) {
    // SPA fallback
    const index = fs.readFileSync(path.join(DIST, "index.html"));
    res.writeHead(200, { "Content-Type": "text/html" });
    return res.end(index);
  }

  const ext = path.extname(filePath);
  res.writeHead(200, { "Content-Type": mime[ext] || "text/plain" });
  res.end(fs.readFileSync(filePath));
}).listen(3000, "0.0.0.0", () => console.log("Serving on :3000"));
