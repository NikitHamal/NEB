import { Controller, Get, HttpCode, HttpStatus, Param, ParseIntPipe, Post, Query, UseGuards } from "@nestjs/common";

import { CurrentUser } from "../../common/decorators/current-user.decorator";
import { Roles } from "../../common/decorators/roles.decorator";
import { ApiResponse } from "../../common/dto/api-response";
import { PaginationQueryDto } from "../../common/dto/pagination-query.dto";
import { ClerkAuthGuard, type AuthenticatedUser } from "../../common/guards/clerk-auth.guard";
import { RolesGuard } from "../../common/guards/roles.guard";
import { buildPaginationMeta, getPaginationOffset } from "../../common/utils/pagination";
import { ModerationService } from "./moderation.service";

/** Every route here is MODERATOR-or-ADMIN-only, enforced by this guard pair. */
@Controller("moderation")
@UseGuards(ClerkAuthGuard, RolesGuard)
@Roles("MODERATOR", "ADMIN")
export class ModerationController {
  constructor(private readonly moderationService: ModerationService) {}

  // The review queue: resources awaiting a decision, oldest first.
  @Get("resources/pending")
  async findPendingResources(@Query() query: PaginationQueryDto) {
    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.moderationService.findPendingResources({ limit: query.limit, offset });
    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }

  // Each report includes the reporter's identity, never exposed to the uploader.
  @Get("resources/reports")
  async findResourceReports(@Query() query: PaginationQueryDto) {
    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.moderationService.findOpenResourceReports({ limit: query.limit, offset });
    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }

  // The "unfounded report" case: closes the report with no change to the resource.
  @Post("resources/reports/:reportId/dismiss")
  @HttpCode(HttpStatus.OK)
  async dismissResourceReport(
    @CurrentUser() moderator: AuthenticatedUser,
    @Param("reportId", ParseIntPipe) reportId: number,
  ) {
    await this.moderationService.dismissResourceReport(moderator.id, reportId);
    return ApiResponse.of(null, "Report dismissed");
  }

  // The review queue: listings awaiting a decision, oldest first.
  @Get("listings/pending")
  async findPendingListings(@Query() query: PaginationQueryDto) {
    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.moderationService.findPendingListings({ limit: query.limit, offset });
    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }

  // Open marketplace-listing reports, oldest first.
  @Get("listings/reports")
  async findListingReports(@Query() query: PaginationQueryDto) {
    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.moderationService.findOpenListingReports({ limit: query.limit, offset });
    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }

  // The "unfounded report" case for a listing: closes the report with no change to the listing.
  @Post("listings/reports/:reportId/dismiss")
  @HttpCode(HttpStatus.OK)
  async dismissListingReport(
    @CurrentUser() moderator: AuthenticatedUser,
    @Param("reportId", ParseIntPipe) reportId: number,
  ) {
    await this.moderationService.dismissListingReport(moderator.id, reportId);
    return ApiResponse.of(null, "Report dismissed");
  }
}
