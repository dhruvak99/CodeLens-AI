import type { NextConfig } from "next";

const proxiedBackendEndpoints = [
  "/analyze",
  "/apply-fix",
  "/explain",
  "/runtime",
  "/metrics"
];

const nextConfig: NextConfig = {
  outputFileTracingRoot: process.cwd(),
  async rewrites() {
    const apiBaseUrl =
      process.env.NEXT_PUBLIC_CODELENS_API ?? process.env.NEXT_PUBLIC_API_BASE_URL;

    if (apiBaseUrl) {
      return [];
    }

    const proxyTarget =
      process.env.CODELENS_API_PROXY_TARGET ?? "http://localhost:8000";
    const normalizedProxyTarget = proxyTarget.replace(/\/$/, "");

    return proxiedBackendEndpoints.map((endpoint) => ({
      source: endpoint,
      destination: `${normalizedProxyTarget}${endpoint}`
    }));
  }
};

export default nextConfig;
