import { Injectable } from "@nestjs/common";

import type { NotificationType } from "../../database/schema";
import type { Notification } from "../../database/types";
import { NotificationsGateway } from "./notifications.gateway";
import { NotificationsRepository } from "./notifications.repository";

export interface NotificationSummary {
  id: number;
  type: NotificationType;
  message: string;
  link: string | null;
  isRead: boolean;
  createdAt: Date;
}

// The DB stores `readAt` (nullable timestamp, matching marketplaceMessagesTable's own
// unread convention) - callers get a computed `isRead: boolean` instead, so the wire
// shape stays simple regardless of how "unread" is tracked internally.
const toSummary = (notification: Notification): NotificationSummary => ({
  id: notification.id,
  type: notification.type,
  message: notification.message,
  link: notification.link,
  isRead: notification.readAt !== null,
  createdAt: notification.createdAt,
});

@Injectable()
export class NotificationsService {
  constructor(
    private readonly notificationsRepository: NotificationsRepository,
    private readonly notificationsGateway: NotificationsGateway,
  ) {}

  async create(userId: number, type: NotificationType, message: string, link: string | null = null) {
    const notification = await this.notificationsRepository.create({ userId, type, message, link });
    const summary = toSummary(notification);
    this.notificationsGateway.notifyUser(userId, summary);
    return summary;
  }

  async findForUser(userId: number, pagination: { limit: number; offset: number }) {
    const { items, total } = await this.notificationsRepository.findForUser(userId, pagination);
    return { items: items.map(toSummary), total };
  }

  getUnreadCount(userId: number) {
    return this.notificationsRepository.countUnread(userId);
  }

  markRead(userId: number, notificationId: number) {
    return this.notificationsRepository.markRead(userId, notificationId);
  }

  markAllRead(userId: number) {
    return this.notificationsRepository.markAllRead(userId);
  }
}
