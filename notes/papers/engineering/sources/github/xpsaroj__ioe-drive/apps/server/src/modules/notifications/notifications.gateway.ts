import { Injectable } from "@nestjs/common";
import { OnGatewayConnection, WebSocketGateway, WebSocketServer } from "@nestjs/websockets";
import type { Server, Socket } from "socket.io";

import { ClerkIdentityResolver } from "../../clerk/clerk-identity.resolver";
import { toSocketFetchRequest } from "../../common/utils/fetch-request";
import type { NotificationSummary } from "./notifications.service";

// Push-only, unlike MessagingGateway - no client ever sends a message here, notifications
// are only ever created server-side (from ModerationService). Every connected socket still
// joins its own personal room on connect, the same pattern MessagingGateway uses.
@Injectable()
@WebSocketGateway({ namespace: "/notifications" })
export class NotificationsGateway implements OnGatewayConnection {
  @WebSocketServer() private readonly server!: Server;

  constructor(private readonly clerkIdentityResolver: ClerkIdentityResolver) {}

  async handleConnection(client: Socket): Promise<void> {
    const user = await this.clerkIdentityResolver.resolve(toSocketFetchRequest(client));

    if (!user) {
      client.disconnect(true);
      return;
    }

    await client.join(`user:${user.id}`);
  }

  notifyUser(userId: number, notification: NotificationSummary): void {
    this.server.to(`user:${userId}`).emit("notification_created", notification);
  }
}
