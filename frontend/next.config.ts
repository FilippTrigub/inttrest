import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Ensure Turbopack uses this folder as the project root
  turbopack: {
    root: ".",
  },
  async rewrites() {
    return [
      {
        source: "/api/mcp-server/:path*",
        destination: "http://localhost:8000/:path*",
      },
    ];
  },
};

export default nextConfig;
