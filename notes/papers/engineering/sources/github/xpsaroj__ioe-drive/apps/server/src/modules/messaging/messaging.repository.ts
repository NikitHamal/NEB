import { Inject, Injectable } from "@nestjs/common";
import { and, asc, count, desc, eq, inArray, isNull, ne, or } from "drizzle-orm";

import { DRIZZLE } from "../../database/database.constants";
import type { DrizzleDb } from "../../database/database.types";
import { marketplaceConversationsTable, marketplaceListingPhotosTable, marketplaceMessagesTable } from "../../database/schema";

/** Shared `with` shape for a conversation's joined detail (listing + cover photo, both participants + profile pictures). */
const CONVERSATION_DETAIL_RELATIONS = {
  listing: {
    columns: { id: true, title: true, status: true },
    with: {
      photos: {
        orderBy: asc(marketplaceListingPhotosTable.sortOrder),
        limit: 1,
      },
    },
  },
  poster: {
    columns: { id: true, fullName: true },
    with: { profile: { columns: { id: true, userId: true, profilePictureUrl: true } } },
  },
  initiator: {
    columns: { id: true, fullName: true },
    with: { profile: { columns: { id: true, userId: true, profilePictureUrl: true } } },
  },
} as const;

@Injectable()
export class MessagingRepository {
  constructor(@Inject(DRIZZLE) private readonly db: DrizzleDb) {}

  async findConversationsForUser(userId: number, pagination: { limit: number; offset: number }) {
    const whereClause = or(
      eq(marketplaceConversationsTable.posterId, userId),
      eq(marketplaceConversationsTable.initiatorId, userId),
    );

    const [conversations, totalResult] = await Promise.all([
      this.db.query.marketplaceConversationsTable.findMany({
        where: whereClause,
        orderBy: [desc(marketplaceConversationsTable.updatedAt)],
        limit: pagination.limit,
        offset: pagination.offset,
        with: {
          ...CONVERSATION_DETAIL_RELATIONS,
          messages: { orderBy: [desc(marketplaceMessagesTable.createdAt)], limit: 1 },
        },
      }),
      this.db.select({ total: count() }).from(marketplaceConversationsTable).where(whereClause),
    ]);

    const unreadCounts = await this.countUnreadPerConversation(
      userId,
      conversations.map((conversation) => conversation.id),
    );

    const items = conversations.map(({ messages, ...conversation }) => ({
      ...conversation,
      lastMessage: messages[0] ?? null,
      unreadCount: unreadCounts.get(conversation.id) ?? 0,
    }));

    return { items, total: totalResult[0]?.total ?? 0 };
  }

  private async countUnreadPerConversation(userId: number, conversationIds: number[]): Promise<Map<number, number>> {
    if (conversationIds.length === 0) return new Map();

    const rows = await this.db
      .select({ conversationId: marketplaceMessagesTable.conversationId, total: count() })
      .from(marketplaceMessagesTable)
      .where(
        and(
          inArray(marketplaceMessagesTable.conversationId, conversationIds),
          ne(marketplaceMessagesTable.senderId, userId),
          isNull(marketplaceMessagesTable.readAt),
        ),
      )
      .groupBy(marketplaceMessagesTable.conversationId);

    return new Map(rows.map((row) => [row.conversationId, row.total]));
  }

  /** Minimal data needed to authorize + drive an action against a conversation. */
  findConversationById(conversationId: number) {
    return this.db.query.marketplaceConversationsTable.findFirst({
      where: eq(marketplaceConversationsTable.id, conversationId),
      columns: { id: true, listingId: true, posterId: true, initiatorId: true },
    });
  }

  /** Same joined shape as the inbox list, for a single conversation's thread header. */
  findConversationDetail(conversationId: number) {
    return this.db.query.marketplaceConversationsTable.findFirst({
      where: eq(marketplaceConversationsTable.id, conversationId),
      with: CONVERSATION_DETAIL_RELATIONS,
    });
  }

  findExistingConversation(listingId: number, initiatorId: number) {
    return this.db.query.marketplaceConversationsTable.findFirst({
      where: and(
        eq(marketplaceConversationsTable.listingId, listingId),
        eq(marketplaceConversationsTable.initiatorId, initiatorId),
      ),
      columns: { id: true },
    });
  }

  async createConversation(listingId: number, posterId: number, initiatorId: number) {
    const [conversation] = await this.db
      .insert(marketplaceConversationsTable)
      .values({ listingId, posterId, initiatorId })
      .returning();

    if (!conversation) {
      throw new Error("Failed to create conversation");
    }

    return conversation;
  }

  // Bumps the conversation's updatedAt in the same transaction, so inbox sort order always reflects the latest message.
  async createMessage(conversationId: number, senderId: number, body: string) {
    return this.db.transaction(async (tx) => {
      const [message] = await tx
        .insert(marketplaceMessagesTable)
        .values({ conversationId, senderId, body })
        .returning();

      if (!message) {
        throw new Error("Failed to create message");
      }

      await tx
        .update(marketplaceConversationsTable)
        .set({ updatedAt: new Date() })
        .where(eq(marketplaceConversationsTable.id, conversationId));

      return message;
    });
  }

  async findMessages(conversationId: number, pagination: { limit: number; offset: number }) {
    const whereClause = eq(marketplaceMessagesTable.conversationId, conversationId);

    const [items, totalResult] = await Promise.all([
      this.db.query.marketplaceMessagesTable.findMany({
        where: whereClause,
        orderBy: [desc(marketplaceMessagesTable.createdAt)],
        limit: pagination.limit,
        offset: pagination.offset,
      }),
      this.db.select({ total: count() }).from(marketplaceMessagesTable).where(whereClause),
    ]);

    return { items, total: totalResult[0]?.total ?? 0 };
  }

  async markRead(conversationId: number, userId: number): Promise<void> {
    await this.db
      .update(marketplaceMessagesTable)
      .set({ readAt: new Date() })
      .where(
        and(
          eq(marketplaceMessagesTable.conversationId, conversationId),
          ne(marketplaceMessagesTable.senderId, userId),
          isNull(marketplaceMessagesTable.readAt),
        ),
      );
  }

  async countTotalUnread(userId: number): Promise<number> {
    const [row] = await this.db
      .select({ total: count() })
      .from(marketplaceMessagesTable)
      .innerJoin(marketplaceConversationsTable, eq(marketplaceMessagesTable.conversationId, marketplaceConversationsTable.id))
      .where(
        and(
          or(eq(marketplaceConversationsTable.posterId, userId), eq(marketplaceConversationsTable.initiatorId, userId)),
          ne(marketplaceMessagesTable.senderId, userId),
          isNull(marketplaceMessagesTable.readAt),
        ),
      );

    return row?.total ?? 0;
  }
}
