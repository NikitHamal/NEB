import { BadRequestException, Injectable, NotFoundException } from "@nestjs/common";

import { AzureBlobService } from "../../storage/azure-blob.service";
import type { ModerateResourceDto } from "../resources/dto/moderate-resource.dto";
import type { ReportResourceDto } from "../resources/dto/report-resource.dto";
import type { ModerateListingDto } from "../marketplace/dto/moderate-listing.dto";
import type { ReportListingDto } from "../marketplace/dto/report-listing.dto";
import { NotificationsService } from "../notifications/notifications.service";
import { ModerationRepository } from "./moderation.repository";

@Injectable()
export class ModerationService {
  constructor(
    private readonly moderationRepository: ModerationRepository,
    private readonly azureBlobService: AzureBlobService,
    private readonly notificationsService: NotificationsService,
  ) {}

  findPendingResources(pagination: { limit: number; offset: number }) {
    return this.moderationRepository.findPendingResources(pagination);
  }

  findOpenResourceReports(pagination: { limit: number; offset: number }) {
    return this.moderationRepository.findOpenResourceReports(pagination);
  }

  async dismissResourceReport(moderatorId: number, reportId: number) {
    const dismissedReport = await this.moderationRepository.resolveResourceReport(reportId, moderatorId);

    if (!dismissedReport) {
      throw new NotFoundException("Report not found");
    }

    return dismissedReport;
  }

  async approveResource(moderatorId: number, resourceId: number) {
    const resource = await this.moderationRepository.findForResourceModeration(resourceId);

    if (!resource) {
      throw new NotFoundException("Resource not found");
    }

    if (resource.status !== "PENDING") {
      throw new BadRequestException("Only pending resources can be approved");
    }

    const updatedResource = await this.moderationRepository.recordResourceModerationAction(
      resourceId,
      "APPROVE",
      { status: "APPROVED", moderatedBy: moderatorId, moderationReason: null, moderationNote: null, moderatedAt: new Date() },
      ["PENDING"],
    );

    if (!updatedResource) {
      throw new BadRequestException("Only pending resources can be approved");
    }

    if (resource.uploadedBy) {
      await this.notificationsService.create(
        resource.uploadedBy,
        "RESOURCE_APPROVED",
        `Your resource "${resource.title}" was approved.`,
        `/resources/r/${resourceId}`,
      );
    }

    return updatedResource;
  }

  async rejectResource(moderatorId: number, resourceId: number, dto: ModerateResourceDto) {
    const resource = await this.moderationRepository.findForResourceModeration(resourceId);

    if (!resource) {
      throw new NotFoundException("Resource not found");
    }

    if (resource.status !== "PENDING" && resource.status !== "APPROVED") {
      throw new BadRequestException("Only pending or approved resources can be rejected");
    }

    const updatedResource = await this.moderationRepository.recordResourceModerationAction(
      resourceId,
      "REJECT",
      {
        status: "REJECTED",
        moderatedBy: moderatorId,
        moderationReason: dto.reason,
        moderationNote: dto.note ?? null,
        moderatedAt: new Date(),
      },
      ["PENDING", "APPROVED"],
    );

    if (!updatedResource) {
      throw new BadRequestException("Only pending or approved resources can be rejected");
    }

    await this.moderationRepository.resolveReportsForResource(resourceId, moderatorId);

    if (resource.uploadedBy) {
      await this.notificationsService.create(
        resource.uploadedBy,
        "RESOURCE_REJECTED",
        `Your resource "${resource.title}" was rejected.`,
        `/resources/r/${resourceId}`,
      );
    }

    return updatedResource;
  }

  // Unlike reject, not resubmittable - the row is kept, but its files are purged from Azure.
  async removeResource(moderatorId: number, resourceId: number, dto: ModerateResourceDto) {
    const resource = await this.moderationRepository.findForResourceModeration(resourceId);

    if (!resource) {
      throw new NotFoundException("Resource not found");
    }

    if (resource.status === "REMOVED") {
      throw new BadRequestException("Resource has already been removed");
    }

    await Promise.all(resource.files.map((file) => this.azureBlobService.delete(file.blobName)));
    await this.moderationRepository.deleteResourceFiles(resourceId);

    const updatedResource = await this.moderationRepository.recordResourceModerationAction(
      resourceId,
      "REMOVE",
      {
        status: "REMOVED",
        moderatedBy: moderatorId,
        moderationReason: dto.reason,
        moderationNote: dto.note ?? null,
        moderatedAt: new Date(),
      },
      ["PENDING", "APPROVED", "REJECTED"],
    );

    if (!updatedResource) {
      throw new BadRequestException("Resource has already been removed");
    }

    await this.moderationRepository.resolveReportsForResource(resourceId, moderatorId);

    if (resource.uploadedBy) {
      await this.notificationsService.create(
        resource.uploadedBy,
        "RESOURCE_REMOVED",
        `Your resource "${resource.title}" was removed.`,
        `/resources/r/${resourceId}`,
      );
    }

    return updatedResource;
  }

  async reportResource(userId: number, resourceId: number, dto: ReportResourceDto) {
    const resource = await this.moderationRepository.findForResourceModeration(resourceId);

    if (!resource) {
      throw new NotFoundException("Resource not found");
    }

    if (resource.status !== "APPROVED") {
      throw new BadRequestException("Only approved resources can be reported");
    }

    if (resource.uploadedBy === userId) {
      throw new BadRequestException("You can't report your own resource");
    }

    const existingReport = await this.moderationRepository.findExistingResourceReport(resourceId, userId);

    if (existingReport) {
      throw new BadRequestException("You have already reported this resource");
    }

    return this.moderationRepository.createResourceReport({
      resourceId,
      reportedBy: userId,
      reason: dto.reason,
      note: dto.note,
    });
  }

  findOpenListingReports(pagination: { limit: number; offset: number }) {
    return this.moderationRepository.findOpenListingReports(pagination);
  }

  async dismissListingReport(moderatorId: number, reportId: number) {
    const dismissedReport = await this.moderationRepository.resolveListingReport(reportId, moderatorId);

    if (!dismissedReport) {
      throw new NotFoundException("Report not found");
    }

    return dismissedReport;
  }

  findPendingListings(pagination: { limit: number; offset: number }) {
    return this.moderationRepository.findPendingListings(pagination);
  }

  async approveListing(moderatorId: number, listingId: number) {
    const listing = await this.moderationRepository.findForListingModeration(listingId);

    if (!listing) {
      throw new NotFoundException("Listing not found");
    }

    if (listing.status !== "PENDING") {
      throw new BadRequestException("Only pending listings can be approved");
    }

    const updatedListing = await this.moderationRepository.recordMarketplaceModerationAction(
      listingId,
      "APPROVE",
      { status: "ACTIVE", moderatedBy: moderatorId, moderationReason: null, moderationNote: null, moderatedAt: new Date() },
      ["PENDING"],
    );

    if (!updatedListing) {
      throw new BadRequestException("Only pending listings can be approved");
    }

    if (listing.postedBy) {
      await this.notificationsService.create(
        listing.postedBy,
        "LISTING_APPROVED",
        `Your listing "${listing.title}" was approved.`,
        `/market/${listingId}`,
      );
    }

    return updatedListing;
  }

  async rejectListing(moderatorId: number, listingId: number, dto: ModerateListingDto) {
    const listing = await this.moderationRepository.findForListingModeration(listingId);

    if (!listing) {
      throw new NotFoundException("Listing not found");
    }

    if (listing.status !== "PENDING" && listing.status !== "ACTIVE") {
      throw new BadRequestException("Only pending or active listings can be rejected");
    }

    const updatedListing = await this.moderationRepository.recordMarketplaceModerationAction(
      listingId,
      "REJECT",
      {
        status: "REJECTED",
        moderatedBy: moderatorId,
        moderationReason: dto.reason,
        moderationNote: dto.note ?? null,
        moderatedAt: new Date(),
      },
      ["PENDING", "ACTIVE"],
    );

    if (!updatedListing) {
      throw new BadRequestException("Only pending or active listings can be rejected");
    }

    await this.moderationRepository.resolveReportsForListing(listingId, moderatorId);

    if (listing.postedBy) {
      await this.notificationsService.create(
        listing.postedBy,
        "LISTING_REJECTED",
        `Your listing "${listing.title}" was rejected.`,
        `/market/${listingId}`,
      );
    }

    return updatedListing;
  }

  // Unlike reject, not resubmittable - the row is kept, but its photos are purged from Azure.
  async removeListing(moderatorId: number, listingId: number, dto: ModerateListingDto) {
    const listing = await this.moderationRepository.findForListingModeration(listingId);

    if (!listing) {
      throw new NotFoundException("Listing not found");
    }

    if (listing.status !== "ACTIVE" && listing.status !== "FULFILLED") {
      throw new BadRequestException("Only active or fulfilled listings can be removed");
    }

    await Promise.all(listing.photos.map((photo) => this.azureBlobService.delete(photo.blobName)));
    await this.moderationRepository.deleteListingPhotos(listingId);

    const updatedListing = await this.moderationRepository.recordMarketplaceModerationAction(
      listingId,
      "REMOVE",
      {
        status: "REMOVED",
        moderatedBy: moderatorId,
        moderationReason: dto.reason,
        moderationNote: dto.note ?? null,
        moderatedAt: new Date(),
      },
      ["ACTIVE", "FULFILLED"],
    );

    if (!updatedListing) {
      throw new BadRequestException("Only active or fulfilled listings can be removed");
    }

    await this.moderationRepository.resolveReportsForListing(listingId, moderatorId);

    if (listing.postedBy) {
      await this.notificationsService.create(
        listing.postedBy,
        "LISTING_REMOVED",
        `Your listing "${listing.title}" was removed.`,
        `/market/${listingId}`,
      );
    }

    return updatedListing;
  }

  async reportListing(userId: number, listingId: number, dto: ReportListingDto) {
    const listing = await this.moderationRepository.findForListingModeration(listingId);

    if (!listing) {
      throw new NotFoundException("Listing not found");
    }

    if (listing.status !== "ACTIVE" && listing.status !== "FULFILLED") {
      throw new BadRequestException("Only active or fulfilled listings can be reported");
    }

    if (listing.postedBy === userId) {
      throw new BadRequestException("You can't report your own listing");
    }

    const existingReport = await this.moderationRepository.findExistingListingReport(listingId, userId);

    if (existingReport) {
      throw new BadRequestException("You have already reported this listing");
    }

    return this.moderationRepository.createListingReport({
      listingId,
      reportedBy: userId,
      reason: dto.reason,
      note: dto.note,
    });
  }
}
