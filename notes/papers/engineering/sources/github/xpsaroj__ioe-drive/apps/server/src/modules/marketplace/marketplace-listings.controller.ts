import {
  BadRequestException,
  Body,
  Controller,
  Delete,
  Get,
  HttpCode,
  HttpStatus,
  Param,
  ParseIntPipe,
  Patch,
  Post,
  Query,
  UploadedFiles,
  UseGuards,
  UseInterceptors,
} from "@nestjs/common";
import { FilesInterceptor } from "@nestjs/platform-express";

import { ApiResponse } from "../../common/dto/api-response";
import { CurrentUser, OptionalCurrentUser } from "../../common/decorators/current-user.decorator";
import { Roles } from "../../common/decorators/roles.decorator";
import { ClerkAuthGuard, type AuthenticatedUser } from "../../common/guards/clerk-auth.guard";
import { OptionalClerkAuthGuard } from "../../common/guards/optional-clerk-auth.guard";
import { RolesGuard } from "../../common/guards/roles.guard";
import { buildPaginationMeta, getPaginationOffset } from "../../common/utils/pagination";
import {
  createListingPhotoValidationPipe,
  LISTING_PHOTO_FIELD,
  listingPhotoMulterOptions,
  MAX_LISTING_PHOTOS,
} from "../../storage/listing-photo-upload.config";
import { ModerationService } from "../moderation/moderation.service";
import { CreateListingDto } from "./dto/create-listing.dto";
import { GetListingsQueryDto } from "./dto/get-listings-query.dto";
import { ModerateListingDto } from "./dto/moderate-listing.dto";
import { ReportListingDto } from "./dto/report-listing.dto";
import { SearchSuggestionsQueryDto } from "./dto/search-suggestions-query.dto";
import { UpdateListingDto } from "./dto/update-listing.dto";
import { MarketplaceListingsService } from "./marketplace-listings.service";

@Controller("marketplace/listings")
export class MarketplaceListingsController {
  constructor(
    private readonly marketplaceListingsService: MarketplaceListingsService,
    private readonly moderationService: ModerationService,
  ) {}

  /** POST /api/marketplace/listings - create a new listing (requires authentication, at least one photo). */
  @Post()
  @UseGuards(ClerkAuthGuard)
  @HttpCode(HttpStatus.CREATED)
  @UseInterceptors(FilesInterceptor(LISTING_PHOTO_FIELD, MAX_LISTING_PHOTOS, listingPhotoMulterOptions))
  async create(
    @CurrentUser() user: AuthenticatedUser,
    @Body() dto: CreateListingDto,
    @UploadedFiles(createListingPhotoValidationPipe()) photos: Express.Multer.File[],
  ) {
    const listing = await this.marketplaceListingsService.createListing(user.id, dto, photos ?? []);
    return ApiResponse.of(listing, "Listing created successfully");
  }

  // PATCH /api/marketplace/listings/:listingId - must be the poster.
  @Patch(":listingId")
  @UseGuards(ClerkAuthGuard)
  async update(
    @CurrentUser() user: AuthenticatedUser,
    @Param("listingId", ParseIntPipe) listingId: number,
    @Body() dto: UpdateListingDto,
  ) {
    if (
      dto.title === undefined &&
      dto.description === undefined &&
      dto.type === undefined &&
      dto.category === undefined &&
      dto.price === undefined &&
      dto.offeringId === undefined
    ) {
      throw new BadRequestException("At least one field must be provided for update");
    }

    const listing = await this.marketplaceListingsService.updateListing(user.id, listingId, dto);
    return ApiResponse.of(listing, "Listing updated successfully");
  }

  // DELETE /api/marketplace/listings/:listingId - must be the poster.
  @Delete(":listingId")
  @UseGuards(ClerkAuthGuard)
  async remove(@CurrentUser() user: AuthenticatedUser, @Param("listingId", ParseIntPipe) listingId: number) {
    await this.marketplaceListingsService.deleteListing(user.id, listingId);
    return ApiResponse.of(null, "Listing deleted successfully");
  }

  // POST /api/marketplace/listings/:listingId/mark-fulfilled - owner-only, ACTIVE -> FULFILLED.
  @Post(":listingId/mark-fulfilled")
  @UseGuards(ClerkAuthGuard)
  @HttpCode(HttpStatus.OK)
  async markFulfilled(@CurrentUser() user: AuthenticatedUser, @Param("listingId", ParseIntPipe) listingId: number) {
    const listing = await this.marketplaceListingsService.markFulfilled(user.id, listingId);
    return ApiResponse.of(listing, "Listing marked as fulfilled");
  }

  // POST /api/marketplace/listings/:listingId/reactivate - owner-only, FULFILLED -> ACTIVE.
  @Post(":listingId/reactivate")
  @UseGuards(ClerkAuthGuard)
  @HttpCode(HttpStatus.OK)
  async reactivate(@CurrentUser() user: AuthenticatedUser, @Param("listingId", ParseIntPipe) listingId: number) {
    const listing = await this.marketplaceListingsService.reactivate(user.id, listingId);
    return ApiResponse.of(listing, "Listing reactivated");
  }

  // POST /api/marketplace/listings/:listingId/approve - moderator-only.
  @Post(":listingId/approve")
  @UseGuards(ClerkAuthGuard, RolesGuard)
  @Roles("MODERATOR", "ADMIN")
  @HttpCode(HttpStatus.OK)
  async approve(@CurrentUser() moderator: AuthenticatedUser, @Param("listingId", ParseIntPipe) listingId: number) {
    const listing = await this.moderationService.approveListing(moderator.id, listingId);
    return ApiResponse.of(listing, "Listing approved");
  }

  // POST /api/marketplace/listings/:listingId/reject - moderator-only; resubmittable, resets to pending on edit.
  @Post(":listingId/reject")
  @UseGuards(ClerkAuthGuard, RolesGuard)
  @Roles("MODERATOR", "ADMIN")
  @HttpCode(HttpStatus.OK)
  async reject(
    @CurrentUser() moderator: AuthenticatedUser,
    @Param("listingId", ParseIntPipe) listingId: number,
    @Body() dto: ModerateListingDto,
  ) {
    const listing = await this.moderationService.rejectListing(moderator.id, listingId, dto);
    return ApiResponse.of(listing, "Listing rejected");
  }

  // POST /api/marketplace/listings/:listingId/report - reporter identity is never surfaced to the poster.
  @Post(":listingId/report")
  @UseGuards(ClerkAuthGuard)
  @HttpCode(HttpStatus.OK)
  async report(
    @CurrentUser() user: AuthenticatedUser,
    @Param("listingId", ParseIntPipe) listingId: number,
    @Body() dto: ReportListingDto,
  ) {
    await this.moderationService.reportListing(user.id, listingId, dto);
    return ApiResponse.of(null, "Listing reported");
  }

  // POST /api/marketplace/listings/:listingId/remove - moderator-only, purges photos, permanent.
  @Post(":listingId/remove")
  @UseGuards(ClerkAuthGuard, RolesGuard)
  @Roles("MODERATOR", "ADMIN")
  @HttpCode(HttpStatus.OK)
  async removeAsModerator(
    @CurrentUser() moderator: AuthenticatedUser,
    @Param("listingId", ParseIntPipe) listingId: number,
    @Body() dto: ModerateListingDto,
  ) {
    const listing = await this.moderationService.removeListing(moderator.id, listingId, dto);
    return ApiResponse.of(listing, "Listing removed");
  }

  // POST /api/marketplace/listings/:listingId/photos - must be the poster.
  @Post(":listingId/photos")
  @UseGuards(ClerkAuthGuard)
  @UseInterceptors(FilesInterceptor(LISTING_PHOTO_FIELD, MAX_LISTING_PHOTOS, listingPhotoMulterOptions))
  async addPhotos(
    @CurrentUser() user: AuthenticatedUser,
    @Param("listingId", ParseIntPipe) listingId: number,
    @UploadedFiles(createListingPhotoValidationPipe()) photos: Express.Multer.File[],
  ) {
    await this.marketplaceListingsService.addListingPhotos(user.id, listingId, photos ?? []);
    return ApiResponse.of(null, "Photos added successfully");
  }

  // DELETE /api/marketplace/listings/:listingId/photos/:photoId - must be the poster; must leave >=1 photo.
  @Delete(":listingId/photos/:photoId")
  @UseGuards(ClerkAuthGuard)
  async removePhoto(
    @CurrentUser() user: AuthenticatedUser,
    @Param("listingId", ParseIntPipe) listingId: number,
    @Param("photoId", ParseIntPipe) photoId: number,
  ) {
    await this.marketplaceListingsService.removeListingPhoto(user.id, listingId, photoId);
    return ApiResponse.of(null, "Photo removed successfully");
  }

  // Must stay registered before `:listingId` below so "search-suggestions" isn't swallowed as a param.
  @Get("search-suggestions")
  async searchSuggestions(@Query() query: SearchSuggestionsQueryDto) {
    const suggestions = await this.marketplaceListingsService.searchSuggestions(query.q, query.limit ?? 8);
    return ApiResponse.of(suggestions);
  }

  // Public for ACTIVE/FULFILLED; REMOVED only visible to its poster or a moderator (404 otherwise).
  @Get(":listingId")
  @UseGuards(OptionalClerkAuthGuard)
  findById(
    @Param("listingId", ParseIntPipe) listingId: number,
    @OptionalCurrentUser() viewer?: AuthenticatedUser,
  ) {
    return this.marketplaceListingsService.findListingById(listingId, viewer);
  }

  // Listings filtered by type, category, offering, price range, or a search query - fully public, unfiltered browse allowed.
  @Get()
  async findMany(@Query() query: GetListingsQueryDto) {
    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.marketplaceListingsService.findListings(
      {
        type: query.type,
        category: query.category,
        offeringId: query.offeringId,
        userId: query.userId,
        minPrice: query.minPrice,
        maxPrice: query.maxPrice,
        q: query.q,
      },
      { limit: query.limit, offset },
    );

    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }
}
