import { Inject, Injectable } from "@nestjs/common";
import { and, asc, count, desc, eq, gte, ilike, lte, max, or } from "drizzle-orm";

import { DRIZZLE } from "../../database/database.constants";
import type { DrizzleDb } from "../../database/database.types";
import { marketplaceListingPhotosTable, marketplaceListingsTable } from "../../database/schema";
import type { MarketplaceCategory, MarketplaceListingType } from "../../database/schema";
import type { FileMetadata } from "../../storage/file-metadata.interface";
import type { CreateListingData, UpdateListingData } from "./marketplace-listing.types";

/** Shared `with` shape for a listing's joined detail (poster + profile picture, subject/offering, photos ordered lowest-sortOrder-first). */
export const MARKETPLACE_LISTING_DETAIL_RELATIONS = {
  subjectOffering: {
    columns: { id: true, subjectId: true },
    with: {
      subject: {
        columns: { id: true, code: true, name: true },
      },
    },
  },
  poster: {
    columns: { id: true, fullName: true },
    with: {
      profile: {
        columns: { id: true, userId: true, profilePictureUrl: true },
      },
    },
  },
  photos: {
    orderBy: asc(marketplaceListingPhotosTable.sortOrder),
  },
} as const;

export interface MarketplaceListingFilters {
  type?: MarketplaceListingType;
  category?: MarketplaceCategory;
  offeringId?: number;
  userId?: number;
  minPrice?: number;
  maxPrice?: number;
  q?: string;
  includeAllStatuses?: boolean;
}

@Injectable()
export class MarketplaceListingsRepository {
  constructor(@Inject(DRIZZLE) private readonly db: DrizzleDb) {}

  /** Lean, capped-list search for the live-typing search palette - just a flat, small
   * list of preview rows (title, price, category, cover photo), not the full paginated
   * browse shape `findMany` returns. Mirrors ResourcesRepository.searchSuggestions. */
  async searchSuggestions(q: string, limit: number) {
    return this.db.query.marketplaceListingsTable.findMany({
      where: and(
        eq(marketplaceListingsTable.status, "ACTIVE"),
        or(ilike(marketplaceListingsTable.title, `%${q}%`), ilike(marketplaceListingsTable.description, `%${q}%`)),
      ),
      orderBy: [desc(marketplaceListingsTable.createdAt)],
      limit,
      columns: { id: true, title: true, price: true, category: true },
      with: {
        photos: {
          orderBy: asc(marketplaceListingPhotosTable.sortOrder),
          limit: 1,
          columns: { blobName: true, photoUrl: true },
        },
      },
    });
  }

  async create(listingData: CreateListingData, photos: FileMetadata[]) {
    return this.db.transaction(async (tx) => {
      const [createdListing] = await tx.insert(marketplaceListingsTable).values(listingData).returning();

      if (!createdListing) {
        throw new Error("Failed to create listing");
      }

      await tx.insert(marketplaceListingPhotosTable).values(
        photos.map((photo, index) => ({
          listingId: createdListing.id,
          photoUrl: photo.url,
          fileSize: photo.size,
          blobName: photo.blobName,
          originalFileName: photo.originalName,
          mimeType: photo.mimeType,
          sortOrder: index,
        })),
      );

      return createdListing;
    });
  }

  async update(listingId: number, userId: number, updateData: UpdateListingData) {
    const [updatedListing] = await this.db
      .update(marketplaceListingsTable)
      .set(updateData)
      .where(and(eq(marketplaceListingsTable.id, listingId), eq(marketplaceListingsTable.postedBy, userId)))
      .returning();

    return updatedListing;
  }

  async updateStatus(listingId: number, userId: number, status: "ACTIVE" | "FULFILLED") {
    const [updatedListing] = await this.db
      .update(marketplaceListingsTable)
      .set({ status })
      .where(and(eq(marketplaceListingsTable.id, listingId), eq(marketplaceListingsTable.postedBy, userId)))
      .returning();

    return updatedListing;
  }

  findById(listingId: number) {
    return this.db.query.marketplaceListingsTable.findFirst({
      where: eq(marketplaceListingsTable.id, listingId),
      with: MARKETPLACE_LISTING_DETAIL_RELATIONS,
    });
  }

  /** Minimal data needed to authorize + perform a deletion: the owning user and every attached photo's blob name. */
  findForDeletion(listingId: number) {
    return this.db.query.marketplaceListingsTable.findFirst({
      where: eq(marketplaceListingsTable.id, listingId),
      columns: { id: true, postedBy: true },
      with: { photos: { columns: { blobName: true } } },
    });
  }

  async delete(listingId: number): Promise<void> {
    // marketplace_listing_photos rows cascade-delete via the FK.
    await this.db.delete(marketplaceListingsTable).where(eq(marketplaceListingsTable.id, listingId));
  }

  /** Minimal data needed to authorize an action against a listing, without pulling in related data. */
  findOwnership(listingId: number) {
    return this.db.query.marketplaceListingsTable.findFirst({
      where: eq(marketplaceListingsTable.id, listingId),
      columns: { id: true, postedBy: true, status: true },
    });
  }

  async countPhotos(listingId: number): Promise<number> {
    const [row] = await this.db
      .select({ total: count() })
      .from(marketplaceListingPhotosTable)
      .where(eq(marketplaceListingPhotosTable.listingId, listingId));

    return row?.total ?? 0;
  }

  // Photo count isn't a safe stand-in for "next sortOrder" once any photo has been removed -
  // the remaining sortOrders are no longer a dense 0..count-1 sequence, so this reads the actual max instead.
  async findMaxPhotoSortOrder(listingId: number): Promise<number | null> {
    const [row] = await this.db
      .select({ max: max(marketplaceListingPhotosTable.sortOrder) })
      .from(marketplaceListingPhotosTable)
      .where(eq(marketplaceListingPhotosTable.listingId, listingId));

    return row?.max ?? null;
  }

  async addPhotos(listingId: number, photos: FileMetadata[], startSortOrder: number): Promise<void> {
    if (photos.length === 0) return;

    await this.db.insert(marketplaceListingPhotosTable).values(
      photos.map((photo, index) => ({
        listingId,
        photoUrl: photo.url,
        fileSize: photo.size,
        blobName: photo.blobName,
        originalFileName: photo.originalName,
        mimeType: photo.mimeType,
        sortOrder: startSortOrder + index,
      })),
    );
  }

  /** Scoped to a specific listingId, so a photo id can't be used to reach into a different listing. */
  findPhoto(listingId: number, photoId: number) {
    return this.db.query.marketplaceListingPhotosTable.findFirst({
      where: (fields, { and, eq }) => and(eq(fields.id, photoId), eq(fields.listingId, listingId)),
      columns: { id: true, blobName: true },
    });
  }

  async deletePhoto(photoId: number): Promise<void> {
    await this.db.delete(marketplaceListingPhotosTable).where(eq(marketplaceListingPhotosTable.id, photoId));
  }

  async findMany(filters: MarketplaceListingFilters, pagination: { limit: number; offset: number }) {
    const conditions = [];

    // Default browse only shows ACTIVE listings - FULFILLED is hidden (still reachable directly or
    // via the owner's own list), REMOVED only ever shown to the owner/a moderator.
    if (!filters.includeAllStatuses) {
      conditions.push(eq(marketplaceListingsTable.status, "ACTIVE"));
    }

    if (filters.type) {
      conditions.push(eq(marketplaceListingsTable.type, filters.type));
    }

    if (filters.category) {
      conditions.push(eq(marketplaceListingsTable.category, filters.category));
    }

    if (filters.offeringId) {
      conditions.push(eq(marketplaceListingsTable.offeringId, filters.offeringId));
    }

    if (filters.userId) {
      conditions.push(eq(marketplaceListingsTable.postedBy, filters.userId));
    }

    if (filters.minPrice !== undefined) {
      conditions.push(gte(marketplaceListingsTable.price, filters.minPrice));
    }

    if (filters.maxPrice !== undefined) {
      conditions.push(lte(marketplaceListingsTable.price, filters.maxPrice));
    }

    if (filters.q) {
      conditions.push(or(ilike(marketplaceListingsTable.title, `%${filters.q}%`), ilike(marketplaceListingsTable.description, `%${filters.q}%`)));
    }

    const whereClause = conditions.length > 0 ? and(...conditions) : undefined;

    const [items, totalResult] = await Promise.all([
      this.db.query.marketplaceListingsTable.findMany({
        where: whereClause,
        orderBy: [desc(marketplaceListingsTable.createdAt)],
        limit: pagination.limit,
        offset: pagination.offset,
        with: MARKETPLACE_LISTING_DETAIL_RELATIONS,
      }),
      this.db.select({ total: count() }).from(marketplaceListingsTable).where(whereClause),
    ]);

    return { items, total: totalResult[0]?.total ?? 0 };
  }
}
