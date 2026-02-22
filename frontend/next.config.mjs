/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",

    // Proxy all /api/v1/* → backend (works both locally and on Vercel)
    async rewrites() {
        const backendUrl =
            process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        return [
            {
                source: "/api/v1/:path*",
                destination: `${backendUrl}/api/v1/:path*`,
            },
        ];
    },

    // Security & performance headers
    async headers() {
        return [
            {
                source: "/(.*)",
                headers: [
                    { key: "X-Content-Type-Options", value: "nosniff" },
                    { key: "X-Frame-Options", value: "DENY" },
                    { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
                ],
            },
        ];
    },
};

export default nextConfig;
