import { Global, Module } from "@nestjs/common";
import { ConfigModule, ConfigService } from "@nestjs/config";
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";

import { DRIZZLE, PG_POOL } from "./database.constants";
import { DatabaseService } from "./database.service";
import * as schema from "./schema";

@Global()
@Module({
  imports: [ConfigModule],
  providers: [
    {
      provide: PG_POOL,
      inject: [ConfigService],
      useFactory: (configService: ConfigService) =>
        new Pool({
          connectionString: configService.getOrThrow<string>("DATABASE_URL"),
          max: 10,
          idleTimeoutMillis: 30_000,
          connectionTimeoutMillis: 5_000,
          ssl:
            configService.get<string>("NODE_ENV") === "production"
              ? { rejectUnauthorized: false }
              : false,
        }),
    },
    {
      provide: DRIZZLE,
      inject: [PG_POOL],
      useFactory: (pool: Pool) => drizzle(pool, { schema }),
    },
    DatabaseService,
  ],
  exports: [DRIZZLE],
})
export class DatabaseModule {}
