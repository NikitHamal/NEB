// Server-only (never imported client-side) - API_INTERNAL_URL overrides the public URL inside Docker Compose, where "localhost" wouldn't reach the server container.
export const SERVER_API_BASE_URL =
    process.env.API_INTERNAL_URL || process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:4000/api";
