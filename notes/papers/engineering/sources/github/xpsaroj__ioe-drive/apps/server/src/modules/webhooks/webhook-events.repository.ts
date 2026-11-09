import { Inject, Injectable } from "@nestjs/common";
import { eq } from "drizzle-orm";

import { DRIZZLE } from "../../database/database.constants";
import type { DrizzleDb } from "../../database/database.types";
import { webhookEventsTable } from "../../database/schema";

/** Clerk webhook idempotency tracking (svixId as primary key, dedupe on replay). */
@Injectable()
export class WebhookEventsRepository {
  constructor(@Inject(DRIZZLE) private readonly db: DrizzleDb) {}

  async alreadyProcessed(svixId: string): Promise<boolean> {
    const rows = await this.db.select().from(webhookEventsTable).where(eq(webhookEventsTable.svixId, svixId));
    return rows.length > 0;
  }

  async markProcessed(svixId: string, eventType: string): Promise<void> {
    await this.db.insert(webhookEventsTable).values({ svixId, eventType });
  }
}
