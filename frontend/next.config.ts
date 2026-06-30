import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  outputFileTracingRoot: process.cwd(),
  async rewrites() {
    const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

    if (apiBaseUrl) {
      return [];
    }

    const proxyTarget =
      process.env.CODELENS_API_PROXY_TARGET ?? "http://localhost:8000";

    return [
      {
        source: "/analyze",
        destination: `${proxyTarget.replace(/\/$/, "")}/analyze`
      }
    ];
  }
};

export default nextConfig;
