import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Ensure Turbopack uses this folder as the project root
  turbopack: {
    root: ".",
  },
};

export default nextConfig;
