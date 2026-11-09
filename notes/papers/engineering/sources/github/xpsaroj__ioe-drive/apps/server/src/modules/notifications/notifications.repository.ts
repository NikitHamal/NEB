import { Inject, Injectable } from "@nestjs/common";
import { and, count, desc, eq, isNull } from "drizzle-orm";

import { DRIZZLE } from "../../database/database.constants";
import type { DrizzleDb } from "../../database/database.types";
import { notificationsTable, type NotificationType } from "../../database/schema";

interface CreateNotificationData {
  userId: number;
  type: NotificationType;
  message: string;
  link: string | null;
}

@Injectable()
export class NotificationsRepository {
  constructor(@Inject(DRIZZLE) private readonly db: DrizzleDb) {}

  async create(data: CreateNotificationData) {
    const [notification] = await this.db.insert(notificationsTable).values(data).returning();

    if (!notification) {
      throw new Error("Failed to create notification");
    }

    return notification;
  }

  async findForUser(userId: number, pagination: { limit: number; offset: number }) {
    const whereClause = eq(notificationsTable.userId, userId);

    const [items, totalResult] = await Promise.all([
      this.db.query.notificationsTable.findMany({
        where: whereClause,
        orderBy: [desc(notificationsTable.createdAt)],
        limit: pagination.limit,
        offset: pagination.offset,
      }),
      this.db.select({ total: count() }).from(notificationsTable).where(whereClause),
    ]);

    return { items, total: totalResult[0]?.total ?? 0 };
  }

  async countUnread(userId: number): Promise<number> {
    const [row] = await this.db
      .select({ total: count() })
      .from(notificationsTable)
      .where(and(eq(notificationsTable.userId, userId), isNull(notificationsTable.readAt)));

    return row?.total ?? 0;
  }

  async markRead(userId: number, notificationId: number): Promise<void> {
    await this.db
      .update(notificationsTable)
      .set({ readAt: new Date() })
      .where(
        and(
          eq(notificationsTable.id, notificationId),
          eq(notificationsTable.userId, userId),
          isNull(notificationsTable.readAt),
        ),
      );
  }

  async markAllRead(userId: number): Promise<void> {
    await this.db
      .update(notificationsTable)
      .set({ readAt: new Date() })
      .where(and(eq(notificationsTable.userId, userId), isNull(notificationsTable.readAt)));
  }
}
