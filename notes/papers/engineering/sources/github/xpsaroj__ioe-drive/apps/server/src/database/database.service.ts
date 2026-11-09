import { Inject, Injectable, Logger, type OnModuleDestroy, type OnModuleInit } from "@nestjs/common";
import type { Pool } from "pg";

import { PG_POOL } from "./database.constants";

/** Verifies the DB connection at startup and closes the pool on shutdown. */
@Injectable()
export class DatabaseService implements OnModuleInit, OnModuleDestroy {
  private readonly logger = new Logger(DatabaseService.name);

  constructor(@Inject(PG_POOL) private readonly pool: Pool) {}

  async onModuleInit() {
    const client = await this.pool.connect();
    try {
      await client.query("SELECT 1");
      this.logger.log("Database connection successful.");
    } finally {
      client.release();
    }
  }

  async onModuleDestroy() {
    await this.pool.end();
  }
}
