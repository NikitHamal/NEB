import { Body, Controller, Delete, Get, Param, ParseIntPipe, Patch, Post, Put, Query, UseGuards } from "@nestjs/common";

import { CurrentUser } from "../../common/decorators/current-user.decorator";
import { ApiResponse } from "../../common/dto/api-response";
import { PaginationQueryDto } from "../../common/dto/pagination-query.dto";
import { ClerkAuthGuard, type AuthenticatedUser } from "../../common/guards/clerk-auth.guard";
import { buildPaginationMeta, getPaginationOffset } from "../../common/utils/pagination";
import { SetVoteDto } from "./dto/set-vote.dto";
import { UpdateProfileDto } from "./dto/update-profile.dto";
import { MeService } from "./me.service";

@Controller("me")
@UseGuards(ClerkAuthGuard)
export class MeController {
  constructor(private readonly meService: MeService) {}

  /** GET /api/me - the currently authenticated user's profile. */
  @Get()
  getProfile(@CurrentUser() user: AuthenticatedUser) {
    return this.meService.getProfile(user.id);
  }

  /** PATCH /api/me - update the currently authenticated user's profile. */
  @Patch()
  async updateProfile(@CurrentUser() user: AuthenticatedUser, @Body() dto: UpdateProfileDto) {
    await this.meService.updateProfile(user.id, dto);
    return ApiResponse.of(null, "Profile updated successfully");
  }

  /** GET /api/me/weekly-summary - resources shared, viewed, and bookmarked in the last 7 days. */
  @Get("weekly-summary")
  getWeeklySummary(@CurrentUser() user: AuthenticatedUser) {
    return this.meService.getWeeklySummary(user.id);
  }

  /** GET /api/me/resources - resources uploaded by the current user, paginated. */
  @Get("resources")
  async getUploadedResources(@CurrentUser() user: AuthenticatedUser, @Query() query: PaginationQueryDto) {
    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.meService.getUploadedResources(user.id, { limit: query.limit, offset });
    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }

  /** GET /api/me/marketplace/listings - marketplace listings posted by the current user (any status), paginated. */
  @Get("marketplace/listings")
  async getMyMarketplaceListings(@CurrentUser() user: AuthenticatedUser, @Query() query: PaginationQueryDto) {
    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.meService.getMyMarketplaceListings(user.id, { limit: query.limit, offset });
    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }

  /** GET /api/me/recent-resources - recently accessed resources, paginated. */
  @Get("recent-resources")
  async getRecentResources(@CurrentUser() user: AuthenticatedUser, @Query() query: PaginationQueryDto) {
    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.meService.getRecentlyAccessedResources(user.id, {
      limit: query.limit,
      offset,
    });
    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }

  /** GET /api/me/bookmarked-resources - bookmarked resources, paginated. */
  @Get("bookmarked-resources")
  async getBookmarkedResources(@CurrentUser() user: AuthenticatedUser, @Query() query: PaginationQueryDto) {
    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.meService.getBookmarkedResources(user.id, { limit: query.limit, offset });
    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }

  // Uncapped, IDs only - backs the bookmark icon on every resource card.
  @Get("bookmarked-resource-ids")
  getBookmarkedResourceIds(@CurrentUser() user: AuthenticatedUser) {
    return this.meService.getBookmarkedResourceIds(user.id);
  }

  /** POST /api/me/resources/:resourceId/recent - mark a resource as recently accessed. */
  @Post("resources/:resourceId/recent")
  async markRecentlyAccessed(
    @CurrentUser() user: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
  ) {
    await this.meService.markResourceAsRecentlyAccessed(user, resourceId);
    return ApiResponse.of(null, "Resource marked as recently accessed");
  }

  /** POST /api/me/resources/:resourceId/bookmark - bookmark a resource. */
  @Post("resources/:resourceId/bookmark")
  async markBookmarked(
    @CurrentUser() user: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
  ) {
    await this.meService.markResourceAsBookmarked(user, resourceId);
    return ApiResponse.of(null, "Resource bookmarked");
  }

  /** DELETE /api/me/resources/:resourceId/bookmark - unbookmark a resource. */
  @Delete("resources/:resourceId/bookmark")
  async unmarkBookmarked(
    @CurrentUser() user: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
  ) {
    await this.meService.unmarkResourceAsBookmarked(user.id, resourceId);
    return ApiResponse.of(null, "Resource unbookmarked");
  }

  /** GET /api/me/resources/vote-values - every resource the current user has voted on, mapped to their vote (1 or -1). */
  @Get("resources/vote-values")
  getVoteValues(@CurrentUser() user: AuthenticatedUser) {
    return this.meService.getVoteValues(user.id);
  }

  /** PUT /api/me/resources/:resourceId/vote - set (or switch) the current user's vote. */
  @Put("resources/:resourceId/vote")
  async setVote(
    @CurrentUser() user: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
    @Body() dto: SetVoteDto,
  ) {
    await this.meService.setResourceVote(user.id, resourceId, dto.value);
    return ApiResponse.of(null, "Vote recorded");
  }

  /** DELETE /api/me/resources/:resourceId/vote - clear the current user's vote. */
  @Delete("resources/:resourceId/vote")
  async clearVote(@CurrentUser() user: AuthenticatedUser, @Param("resourceId", ParseIntPipe) resourceId: number) {
    await this.meService.clearResourceVote(user.id, resourceId);
    return ApiResponse.of(null, "Vote cleared");
  }
}
