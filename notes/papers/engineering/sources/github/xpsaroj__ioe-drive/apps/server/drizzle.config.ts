import { defineConfig } from "drizzle-kit";
import dotenv from "dotenv";

const nodeEnv = process.env.NODE_ENV;

// Load env files for local dev / test only (no need in production)
if (nodeEnv === "test") {
    dotenv.config({ path: ".env.test" });
} else if (nodeEnv === "development" || !nodeEnv) {
    dotenv.config({ path: ".env.local" });
}

// Ensure DATABASE_URL is present
const DATABASE_URL = process.env.DATABASE_URL;
if (!DATABASE_URL) {
    throw new Error("DATABASE_URL is required for migrations");
}

export default defineConfig({
    schema: "./src/database/schema.ts",
    out: "./src/database/migrations",
    dialect: "postgresql",
    dbCredentials: {
        url: DATABASE_URL,
    },
    verbose: true,
    strict: true,
});
