import dotenv from "dotenv";
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";

import * as schema from "./schema";

// Standalone DB connection for the seeder scripts, run via `tsx` outside Nest's DI lifecycle.
const nodeEnv = process.env.NODE_ENV;

if (nodeEnv === "test") {
  dotenv.config({ path: ".env.test" });
} else if (nodeEnv === "development" || !nodeEnv) {
  dotenv.config({ path: ".env.local" });
}

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) {
  throw new Error("DATABASE_URL is required to run seeders");
}

const pool = new Pool({
  connectionString: databaseUrl,
  max: 10,
  idleTimeoutMillis: 30_000,
  connectionTimeoutMillis: 5_000,
  ssl: nodeEnv === "production" ? { rejectUnauthorized: false } : false,
});

export const db = drizzle(pool, { schema });
