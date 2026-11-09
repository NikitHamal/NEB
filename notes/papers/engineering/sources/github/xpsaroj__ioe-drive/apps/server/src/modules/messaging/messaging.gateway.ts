import { Injectable, UseFilters } from "@nestjs/common";
import {
  ConnectedSocket,
  MessageBody,
  OnGatewayConnection,
  SubscribeMessage,
  WebSocketGateway,
  WebSocketServer,
} from "@nestjs/websockets";
import type { Server, Socket } from "socket.io";

import { ClerkIdentityResolver } from "../../clerk/clerk-identity.resolver";
import { WsExceptionFilter } from "../../common/filters/ws-exception.filter";
import type { AuthenticatedUser } from "../../common/guards/clerk-auth.guard";
import { toSocketFetchRequest } from "../../common/utils/fetch-request";
import type { Message } from "../../database/types";
import { JoinConversationDto } from "./dto/join-conversation.dto";
import { SendMessageDto } from "./dto/send-message.dto";
import { MessagingService } from "./messaging.service";

type AuthenticatedSocket = Socket & { data: { authUser: AuthenticatedUser } };

@Injectable()
@UseFilters(WsExceptionFilter)
@WebSocketGateway({ namespace: "/marketplace-messaging" })
export class MessagingGateway implements OnGatewayConnection {
  @WebSocketServer() private readonly server!: Server;

  constructor(
    private readonly clerkIdentityResolver: ClerkIdentityResolver,
    private readonly messagingService: MessagingService,
  ) {}

  // Every connected socket joins its own personal room - this is what lets the nav
  // badge/inbox update live even when the user doesn't have a specific thread open.
  async handleConnection(client: Socket): Promise<void> {
    const user = await this.clerkIdentityResolver.resolve(toSocketFetchRequest(client));

    if (!user) {
      client.disconnect(true);
      return;
    }

    (client as AuthenticatedSocket).data.authUser = user;
    await client.join(`user:${user.id}`);
  }

  @SubscribeMessage("join_conversation")
  async onJoinConversation(@ConnectedSocket() client: AuthenticatedSocket, @MessageBody() dto: JoinConversationDto): Promise<void> {
    await this.messagingService.assertParticipant(client.data.authUser.id, dto.conversationId);
    await client.join(`conversation:${dto.conversationId}`);
  }

  @SubscribeMessage("leave_conversation")
  async onLeaveConversation(@ConnectedSocket() client: AuthenticatedSocket, @MessageBody() dto: JoinConversationDto): Promise<void> {
    await client.leave(`conversation:${dto.conversationId}`);
  }

  @SubscribeMessage("send_message")
  async onSendMessage(@ConnectedSocket() client: AuthenticatedSocket, @MessageBody() dto: SendMessageDto): Promise<void> {
    await this.messagingService.sendMessage(client.data.authUser.id, dto.conversationId, dto.body);
  }

  // Called by MessagingService (via ModuleRef, see there) so every message-creation
  // path emits the same way, instead of only the socket path doing it here.
  emitNewMessage(conversationId: number, message: Message): void {
    this.server.to(`conversation:${conversationId}`).emit("new_message", message);
  }

  emitConversationUpdated(userId: number, payload: { conversationId: number; lastMessage: Message; unreadDelta: number }): void {
    this.server.to(`user:${userId}`).emit("conversation_updated", payload);
  }
}
