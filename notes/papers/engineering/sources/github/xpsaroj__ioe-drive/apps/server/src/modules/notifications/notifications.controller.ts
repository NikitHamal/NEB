import { Controller, Get, HttpCode, HttpStatus, Param, ParseIntPipe, Patch, Query, UseGuards } from "@nestjs/common";

import { CurrentUser } from "../../common/decorators/current-user.decorator";
import { ApiResponse } from "../../common/dto/api-response";
import { PaginationQueryDto } from "../../common/dto/pagination-query.dto";
import { ClerkAuthGuard, type AuthenticatedUser } from "../../common/guards/clerk-auth.guard";
import { buildPaginationMeta, getPaginationOffset } from "../../common/utils/pagination";
import { NotificationsService } from "./notifications.service";

@Controller("notifications")
@UseGuards(ClerkAuthGuard)
export class NotificationsController {
  constructor(private readonly notificationsService: NotificationsService) {}

  /** GET /api/notifications - this user's notifications, paginated, newest first. */
  @Get()
  async getNotifications(@CurrentUser() user: AuthenticatedUser, @Query() query: PaginationQueryDto) {
    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.notificationsService.findForUser(user.id, { limit: query.limit, offset });
    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }

  /** GET /api/notifications/unread-count - cold-start value for the bell badge, before the socket takes over. */
  @Get("unread-count")
  async getUnreadCount(@CurrentUser() user: AuthenticatedUser) {
    const unreadCount = await this.notificationsService.getUnreadCount(user.id);
    return ApiResponse.of({ unreadCount });
  }

  /** PATCH /api/notifications/:id/read */
  @Patch(":id/read")
  @HttpCode(HttpStatus.OK)
  async markRead(@CurrentUser() user: AuthenticatedUser, @Param("id", ParseIntPipe) id: number) {
    await this.notificationsService.markRead(user.id, id);
    return ApiResponse.of(null, "Notification marked as read");
  }

  /** PATCH /api/notifications/read-all */
  @Patch("read-all")
  @HttpCode(HttpStatus.OK)
  async markAllRead(@CurrentUser() user: AuthenticatedUser) {
    await this.notificationsService.markAllRead(user.id);
    return ApiResponse.of(null, "All notifications marked as read");
  }
}
