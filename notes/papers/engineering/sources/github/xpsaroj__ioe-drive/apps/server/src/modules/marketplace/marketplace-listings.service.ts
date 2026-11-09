import { BadRequestException, Inject, Injectable, NotFoundException } from "@nestjs/common";

import { DRIZZLE } from "../../database/database.constants";
import type { DrizzleDb } from "../../database/database.types";
import type { AuthenticatedUser } from "../../common/guards/clerk-auth.guard";
import { AzureBlobService } from "../../storage/azure-blob.service";
import { MarketplaceListingFilters, MarketplaceListingsRepository } from "./marketplace-listings.repository";
import type { CreateListingData, UpdateListingData } from "./marketplace-listing.types";

@Injectable()
export class MarketplaceListingsService {
  constructor(
    private readonly marketplaceListingsRepository: MarketplaceListingsRepository,
    private readonly azureBlobService: AzureBlobService,
    @Inject(DRIZZLE) private readonly db: DrizzleDb,
  ) {}

  // Listing photos are stored the same way as gated resource files (private container, unsigned
  // stored URL 403s) but need to render as thumbnails across many cards at once, so every read path
  // signs them here rather than behind a per-file download-url endpoint like resources use.
  private async signPhotoUrls<T extends { photos: { blobName: string; photoUrl: string }[] }>(
    listing: T,
  ): Promise<T> {
    const photos = await Promise.all(
      listing.photos.map(async (photo) => ({
        ...photo,
        photoUrl: await this.azureBlobService.generateSasUrl(photo.blobName, { expiresInMinutes: 60 }),
      })),
    );

    return { ...listing, photos };
  }

  private async uploadPhotos(files: Express.Multer.File[]) {
    return Promise.all(
      files.map(async (file) => {
        const blobName = this.azureBlobService.generateBlobName(file.originalname, "listings");
        const url = await this.azureBlobService.upload(file.buffer, blobName, file.mimetype);

        return {
          blobName,
          url,
          originalName: file.originalname,
          mimeType: file.mimetype,
          size: file.size,
        };
      }),
    );
  }

  async createListing(
    userId: number,
    listingData: Omit<CreateListingData, "postedBy" | "status">,
    photos: Express.Multer.File[],
  ) {
    if (photos.length === 0) {
      throw new BadRequestException("At least one photo is required");
    }

    const { offeringId } = listingData;

    if (offeringId) {
      const existingSubject = await this.db.query.subjectOfferingsTable.findFirst({
        where: (fields, { eq }) => eq(fields.id, offeringId),
        columns: { id: true },
      });

      if (!existingSubject) {
        throw new NotFoundException("Subject offering not found");
      }
    }

    const uploadedPhotos = await this.uploadPhotos(photos);

    return this.marketplaceListingsRepository.create(
      { ...listingData, postedBy: userId, status: "PENDING" },
      uploadedPhotos,
    );
  }

  async updateListing(userId: number, listingId: number, updateData: UpdateListingData) {
    const existingListing = await this.marketplaceListingsRepository.findOwnership(listingId);

    if (!existingListing || existingListing.postedBy !== userId) {
      throw new NotFoundException("Listing not found");
    }

    if (existingListing.status === "REMOVED") {
      throw new BadRequestException("This listing has been removed and can no longer be edited.");
    }

    // Editing a rejected listing is treated as an implicit resubmission - back to the
    // review queue, with the previous moderation verdict cleared. Pending/active/fulfilled
    // listings are left as-is by an edit.
    const resubmission =
      existingListing.status === "REJECTED"
        ? {
            status: "PENDING" as const,
            moderatedBy: null,
            moderationReason: null,
            moderationNote: null,
            moderatedAt: null,
          }
        : {};

    return this.marketplaceListingsRepository.update(listingId, userId, { ...updateData, ...resubmission });
  }

  async deleteListing(userId: number, listingId: number): Promise<void> {
    const existingListing = await this.marketplaceListingsRepository.findForDeletion(listingId);

    if (!existingListing || existingListing.postedBy !== userId) {
      throw new NotFoundException("Listing not found");
    }

    await Promise.all(existingListing.photos.map((photo) => this.azureBlobService.delete(photo.blobName)));
    await this.marketplaceListingsRepository.delete(listingId);
  }

  /** Verifies a listing exists and is owned by the given user - a listing that doesn't
   * exist and one that isn't yours are indistinguishable (both 404). A REMOVED listing's
   * photos were already purged by moderation, so it's terminal - no further edits either. */
  private async assertOwnership(userId: number, listingId: number): Promise<void> {
    const listing = await this.marketplaceListingsRepository.findOwnership(listingId);

    if (!listing || listing.postedBy !== userId) {
      throw new NotFoundException("Listing not found");
    }

    if (listing.status === "REMOVED") {
      throw new BadRequestException("This listing has been removed and can no longer be edited.");
    }
  }

  async markFulfilled(userId: number, listingId: number) {
    const listing = await this.marketplaceListingsRepository.findOwnership(listingId);

    if (!listing || listing.postedBy !== userId) {
      throw new NotFoundException("Listing not found");
    }

    if (listing.status !== "ACTIVE") {
      throw new BadRequestException("Only an active listing can be marked as fulfilled");
    }

    return this.marketplaceListingsRepository.updateStatus(listingId, userId, "FULFILLED");
  }

  async reactivate(userId: number, listingId: number) {
    const listing = await this.marketplaceListingsRepository.findOwnership(listingId);

    if (!listing || listing.postedBy !== userId) {
      throw new NotFoundException("Listing not found");
    }

    if (listing.status !== "FULFILLED") {
      throw new BadRequestException("Only a fulfilled listing can be reactivated");
    }

    return this.marketplaceListingsRepository.updateStatus(listingId, userId, "ACTIVE");
  }

  async addListingPhotos(userId: number, listingId: number, files: Express.Multer.File[]): Promise<void> {
    await this.assertOwnership(userId, listingId);

    if (files.length === 0) return;

    const maxSortOrder = await this.marketplaceListingsRepository.findMaxPhotoSortOrder(listingId);
    const uploadedPhotos = await this.uploadPhotos(files);
    await this.marketplaceListingsRepository.addPhotos(listingId, uploadedPhotos, (maxSortOrder ?? -1) + 1);
  }

  async removeListingPhoto(userId: number, listingId: number, photoId: number): Promise<void> {
    await this.assertOwnership(userId, listingId);

    const photo = await this.marketplaceListingsRepository.findPhoto(listingId, photoId);

    if (!photo) {
      throw new NotFoundException("Photo not found");
    }

    const currentPhotoCount = await this.marketplaceListingsRepository.countPhotos(listingId);

    if (currentPhotoCount <= 1) {
      throw new BadRequestException("A listing must have at least one photo");
    }

    await this.azureBlobService.delete(photo.blobName);
    await this.marketplaceListingsRepository.deletePhoto(photoId);
  }

  /** `viewer` is absent for an anonymous request. ACTIVE/FULFILLED are visible to anyone;
   * anything else (PENDING/REJECTED/REMOVED) only to its own poster or a moderator/admin -
   * everyone else gets the same 404 as a nonexistent listing. */
  async findListingById(listingId: number, viewer?: AuthenticatedUser) {
    const listing = await this.marketplaceListingsRepository.findById(listingId);

    if (!listing) {
      throw new NotFoundException("Listing not found");
    }

    const isVisible =
      listing.status === "ACTIVE" ||
      listing.status === "FULFILLED" ||
      (viewer && (viewer.id === listing.postedBy || viewer.role === "MODERATOR" || viewer.role === "ADMIN"));

    if (!isVisible) {
      throw new NotFoundException("Listing not found");
    }

    return this.signPhotoUrls(listing);
  }

  async findListings(filters: MarketplaceListingFilters, pagination: { limit: number; offset: number }) {
    const { items, total } = await this.marketplaceListingsRepository.findMany(filters, pagination);
    const signedItems = await Promise.all(items.map((item) => this.signPhotoUrls(item)));

    return { items: signedItems, total };
  }

  async searchSuggestions(q: string, limit: number) {
    const results = await this.marketplaceListingsRepository.searchSuggestions(q, limit);
    const signedResults = await Promise.all(results.map((r) => this.signPhotoUrls(r)));

    return signedResults.map((r) => ({
      id: r.id,
      title: r.title,
      price: r.price,
      category: r.category,
      photoUrl: r.photos[0]?.photoUrl,
    }));
  }
}
