import path from "node:path";
import { fileURLToPath } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url));
// Fully static: Cloudflare Pages free tier serves static assets with no request or
// bandwidth cap. Anything dynamic would count against the 100k/day Functions quota.
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
  // A stray package-lock.json in $HOME made Next infer the wrong workspace root,
  // which broke the "@/…" path alias. Pin it.
  outputFileTracingRoot: here,
};
export default nextConfig;
