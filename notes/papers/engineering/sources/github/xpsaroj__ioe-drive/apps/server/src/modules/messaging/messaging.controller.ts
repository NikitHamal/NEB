import { Body, Controller, Get, HttpCode, HttpStatus, Param, ParseIntPipe, Patch, Post, Query, UseGuards } from "@nestjs/common";

import { CurrentUser } from "../../common/decorators/current-user.decorator";
import { ApiResponse } from "../../common/dto/api-response";
import { PaginationQueryDto } from "../../common/dto/pagination-query.dto";
import { ClerkAuthGuard, type AuthenticatedUser } from "../../common/guards/clerk-auth.guard";
import { buildPaginationMeta, getPaginationOffset } from "../../common/utils/pagination";
import { StartConversationDto } from "./dto/start-conversation.dto";
import { MessagingService } from "./messaging.service";

@Controller("messaging")
@UseGuards(ClerkAuthGuard)
export class MessagingController {
  constructor(private readonly messagingService: MessagingService) {}

  /** GET /api/messaging/conversations - this user's inbox, paginated, newest activity first. */
  @Get("conversations")
  async getConversations(@CurrentUser() user: AuthenticatedUser, @Query() query: PaginationQueryDto) {
    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.messagingService.getConversations(user.id, { limit: query.limit, offset });
    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }

  /** GET /api/messaging/conversations/:conversationId - thread header detail (listing + both participants). */
  @Get("conversations/:conversationId")
  async getConversation(
    @CurrentUser() user: AuthenticatedUser,
    @Param("conversationId", ParseIntPipe) conversationId: number,
  ) {
    const conversation = await this.messagingService.getConversationById(user.id, conversationId);
    return ApiResponse.of(conversation);
  }

  /** GET /api/messaging/conversations/:conversationId/messages - paginated, newest-first (reverse client-side to display). */
  @Get("conversations/:conversationId/messages")
  async getMessages(
    @CurrentUser() user: AuthenticatedUser,
    @Param("conversationId", ParseIntPipe) conversationId: number,
    @Query() query: PaginationQueryDto,
  ) {
    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.messagingService.getConversationMessages(user.id, conversationId, {
      limit: query.limit,
      offset,
    });
    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }

  /** POST /api/messaging/conversations - start (or reuse) a thread with a listing's poster; the first message. */
  @Post("conversations")
  @HttpCode(HttpStatus.CREATED)
  async startConversation(@CurrentUser() user: AuthenticatedUser, @Body() dto: StartConversationDto) {
    const result = await this.messagingService.startConversation(user.id, dto.listingId, dto.message);
    return ApiResponse.of(result, "Message sent");
  }

  /** PATCH /api/messaging/conversations/:conversationId/read - marks the other participant's messages as read. */
  @Patch("conversations/:conversationId/read")
  @HttpCode(HttpStatus.OK)
  async markRead(@CurrentUser() user: AuthenticatedUser, @Param("conversationId", ParseIntPipe) conversationId: number) {
    await this.messagingService.markConversationRead(user.id, conversationId);
    return ApiResponse.of(null, "Conversation marked as read");
  }

  /** GET /api/messaging/unread-count - cold-start value for the nav badge, before the socket takes over. */
  @Get("unread-count")
  async getUnreadCount(@CurrentUser() user: AuthenticatedUser) {
    const unreadCount = await this.messagingService.getUnreadCount(user.id);
    return ApiResponse.of({ unreadCount });
  }
}
