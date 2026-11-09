import { Inject, Injectable } from "@nestjs/common";
import { and, asc, count, desc, eq, ilike, ne, or, sql, sum } from "drizzle-orm";

import { DRIZZLE } from "../../database/database.constants";
import type { DrizzleDb } from "../../database/database.types";
import { resourceFilesTable, resourceLinksTable, resourcesTable } from "../../database/schema";
import type { FileMetadata } from "../../storage/file-metadata.interface";
import type { ResourceLinkInput } from "./dto/resource-link-input.dto";
import type { CreateResourceData, UpdateResourceData } from "./resources.types";

/**
 * Shared `with` shape for a resource's joined detail (subject/program, uploader +
 * profile picture, files) - used by findById/findMany below, and reused as-is by
 * MeRepository for the recent/bookmarked resource lists (same shape, joined off a
 * different table).
 */
export const RESOURCE_DETAIL_RELATIONS = {
  subjectOffering: {
    columns: {
      id: true,
      subjectId: true,
    },
    with: {
      subject: {
        columns: {
          id: true,
          code: true,
          name: true,
        },
      },
    },
  },
  uploader: {
    columns: {
      id: true,
      fullName: true,
    },
    with: {
      profile: {
        columns: {
          id: true,
          userId: true,
          profilePictureUrl: true,
        },
      },
    },
  },
  files: {
    columns: {
      id: true,
      resourceId: true,
      fileUrl: true,
      fileSize: true,
      originalFileName: true,
      mimeType: true,
    },
  },
  links: {
    columns: {
      id: true,
      resourceId: true,
      url: true,
      label: true,
    },
    orderBy: asc(resourceLinksTable.createdAt),
  },
} as const;

/** Lean projection for a compact resource preview row (title, type, subject code) -
 * shared by searchSuggestions and findSimilar below, which both render the same kind
 * of row. Deliberately excludes everything RESOURCE_DETAIL_RELATIONS carries that a
 * preview row never renders: description, uploader, and the files list. */
export const RESOURCE_PREVIEW_RELATIONS = {
  subjectOffering: {
    columns: { id: true },
    with: {
      subject: {
        columns: { code: true },
      },
    },
  },
} as const;

@Injectable()
export class ResourcesRepository {
  constructor(@Inject(DRIZZLE) private readonly db: DrizzleDb) {}

  async create(resourceData: CreateResourceData, files: FileMetadata[], links: ResourceLinkInput[] = []) {
    return this.db.transaction(async (tx) => {
      const [createdResource] = await tx.insert(resourcesTable).values(resourceData).returning();

      if (!createdResource) {
        throw new Error("Failed to create resource");
      }

      if (files.length > 0) {
        await tx.insert(resourceFilesTable).values(
          files.map((file) => ({
            resourceId: createdResource.id,
            fileUrl: file.url,
            fileSize: file.size,
            blobName: file.blobName,
            originalFileName: file.originalName,
            mimeType: file.mimeType,
          })),
        );
      }

      if (links.length > 0) {
        await tx.insert(resourceLinksTable).values(
          links.map((link) => ({ resourceId: createdResource.id, url: link.url, label: link.label })),
        );
      }

      return createdResource;
    });
  }

  async update(resourceId: number, userId: number, updateData: UpdateResourceData) {
    const [updatedResource] = await this.db
      .update(resourcesTable)
      .set(updateData)
      .where(and(eq(resourcesTable.id, resourceId), eq(resourcesTable.uploadedBy, userId)))
      .returning();

    return updatedResource;
  }

  findById(resourceId: number) {
    return this.db.query.resourcesTable.findFirst({
      where: eq(resourcesTable.id, resourceId),
      with: RESOURCE_DETAIL_RELATIONS,
    });
  }

  /** Minimal data needed to authorize + perform a deletion: the owning user and every
   * attached file's blob name (so they can be removed from Azure before the row is). */
  findForDeletion(resourceId: number) {
    return this.db.query.resourcesTable.findFirst({
      where: eq(resourcesTable.id, resourceId),
      columns: { id: true, uploadedBy: true },
      with: { files: { columns: { blobName: true } } },
    });
  }

  async delete(resourceId: number): Promise<void> {
    // resource_files rows cascade-delete via the FK.
    await this.db.delete(resourcesTable).where(eq(resourcesTable.id, resourceId));
  }

  /** Minimal data needed to authorize an action against a resource, without pulling in
   * any related data. Includes `status` so callers can also block mutating a REMOVED resource. */
  findOwnership(resourceId: number) {
    return this.db.query.resourcesTable.findFirst({
      where: eq(resourcesTable.id, resourceId),
      columns: { id: true, uploadedBy: true, status: true },
    });
  }

  /** Includes status/uploadedBy for the visibility check in findSimilarResources. */
  findOfferingId(resourceId: number) {
    return this.db.query.resourcesTable.findFirst({
      where: eq(resourcesTable.id, resourceId),
      columns: { offeringId: true, status: true, uploadedBy: true },
    });
  }

  async addFiles(resourceId: number, files: FileMetadata[]): Promise<void> {
    if (files.length === 0) return;

    await this.db.insert(resourceFilesTable).values(
      files.map((file) => ({
        resourceId,
        fileUrl: file.url,
        fileSize: file.size,
        blobName: file.blobName,
        originalFileName: file.originalName,
        mimeType: file.mimeType,
      })),
    );
  }

  /** Scoped to a specific resourceId, so a file id can't be used to reach into a
   * different resource than the one the caller is authorized for. Carries the parent
   * resource's status/uploadedBy too, so callers that need to check visibility (e.g.
   * getFileDownloadUrl) don't need a second query. */
  findFile(resourceId: number, fileId: number) {
    return this.db.query.resourceFilesTable.findFirst({
      where: (fields, { and, eq }) => and(eq(fields.id, fileId), eq(fields.resourceId, resourceId)),
      columns: { id: true, blobName: true, originalFileName: true },
      with: { resource: { columns: { status: true, uploadedBy: true } } },
    });
  }

  async deleteFile(fileId: number): Promise<void> {
    await this.db.delete(resourceFilesTable).where(eq(resourceFilesTable.id, fileId));
  }

  async addLinks(resourceId: number, links: ResourceLinkInput[]): Promise<void> {
    if (links.length === 0) return;

    await this.db.insert(resourceLinksTable).values(
      links.map((link) => ({ resourceId, url: link.url, label: link.label })),
    );
  }

  /** Scoped to a specific resourceId, same reasoning as findFile above. */
  findLink(resourceId: number, linkId: number) {
    return this.db.query.resourceLinksTable.findFirst({
      where: (fields, { and, eq }) => and(eq(fields.id, linkId), eq(fields.resourceId, resourceId)),
      columns: { id: true },
    });
  }

  async deleteLink(linkId: number): Promise<void> {
    await this.db.delete(resourceLinksTable).where(eq(resourceLinksTable.id, linkId));
  }

  async countFilesByResourceId(resourceId: number): Promise<number> {
    const [row] = await this.db
      .select({ total: count() })
      .from(resourceFilesTable)
      .where(eq(resourceFilesTable.resourceId, resourceId));

    return row?.total ?? 0;
  }

  async countLinksByResourceId(resourceId: number): Promise<number> {
    const [row] = await this.db
      .select({ total: count() })
      .from(resourceLinksTable)
      .where(eq(resourceLinksTable.resourceId, resourceId));

    return row?.total ?? 0;
  }

  /** Combined size of a resource's existing files, for enforcing the total-size cap. */
  async sumFileSizesByResourceId(resourceId: number): Promise<number> {
    const [row] = await this.db
      .select({ total: sum(resourceFilesTable.fileSize) })
      .from(resourceFilesTable)
      .where(eq(resourceFilesTable.resourceId, resourceId));

    return Number(row?.total ?? 0);
  }

  async incrementDownloadCount(resourceId: number): Promise<void> {
    await this.db
      .update(resourcesTable)
      .set({ downloadCount: sql`${resourcesTable.downloadCount} + 1` })
      .where(eq(resourcesTable.id, resourceId));
  }

  async sumUpvotesByUploader(userId: number): Promise<number> {
    const [row] = await this.db
      .select({ total: sum(resourcesTable.upvoteCount) })
      .from(resourcesTable)
      .where(and(eq(resourcesTable.uploadedBy, userId), eq(resourcesTable.status, "APPROVED")));

    return Number(row?.total ?? 0);
  }

  async findMany(
    filters: { offeringId?: number; userId?: number; q?: string; includeAllStatuses?: boolean },
    pagination: { limit: number; offset: number },
  ) {
    const conditions = [];

    if (!filters.includeAllStatuses) {
      conditions.push(eq(resourcesTable.status, "APPROVED"));
    }

    if (filters.offeringId) {
      conditions.push(eq(resourcesTable.offeringId, filters.offeringId));
    }

    if (filters.userId) {
      conditions.push(eq(resourcesTable.uploadedBy, filters.userId));
    }

    if (filters.q) {
      conditions.push(or(ilike(resourcesTable.title, `%${filters.q}%`), ilike(resourcesTable.description, `%${filters.q}%`)));
    }

    const whereClause = conditions.length > 0 ? and(...conditions) : undefined;

    const [items, totalResult] = await Promise.all([
      this.db.query.resourcesTable.findMany({
        where: whereClause,
        orderBy: [desc(resourcesTable.createdAt)],
        limit: pagination.limit,
        offset: pagination.offset,
        with: RESOURCE_DETAIL_RELATIONS,
      }),
      this.db.select({ total: count() }).from(resourcesTable).where(whereClause),
    ]);

    return { items, total: totalResult[0]?.total ?? 0 };
  }

  // Flat ids only, no joins - backs the sitemap, which never needs more than the id.
  async findAllApprovedIds(): Promise<number[]> {
    const rows = await this.db.query.resourcesTable.findMany({
      where: eq(resourcesTable.status, "APPROVED"),
      columns: { id: true },
    });

    return rows.map((row) => row.id);
  }

  /** Lean, uncapped-pagination search for live-typing UI (the search palette) - just a
   * flat, capped list of preview rows, not the full paginated browse shape `findMany`
   * returns. Flattens `subjectOffering.subject.code` to a top-level `subjectCode` since
   * nothing downstream needs the nested shape once it's this narrow. */
  async searchSuggestions(q: string, limit: number) {
    const results = await this.db.query.resourcesTable.findMany({
      where: and(
        eq(resourcesTable.status, "APPROVED"),
        or(ilike(resourcesTable.title, `%${q}%`), ilike(resourcesTable.description, `%${q}%`)),
      ),
      orderBy: [desc(resourcesTable.createdAt)],
      limit,
      columns: { id: true, title: true, type: true },
      with: RESOURCE_PREVIEW_RELATIONS,
    });

    return results.map((r) => ({
      id: r.id,
      title: r.title,
      type: r.type,
      subjectCode: r.subjectOffering.subject.code,
    }));
  }

  /** Other resources from the same subject offering (excluding this one) - the
   * simplest correct notion of "similar" given there's no recommendation engine: same
   * course, most recently shared first. Same lean preview shape as searchSuggestions
   * above, for the same reason (a compact row, not the full detail shape). */
  async findSimilar(resourceId: number, offeringId: number, limit: number) {
    const results = await this.db.query.resourcesTable.findMany({
      where: and(
        eq(resourcesTable.status, "APPROVED"),
        eq(resourcesTable.offeringId, offeringId),
        ne(resourcesTable.id, resourceId),
      ),
      orderBy: [desc(resourcesTable.createdAt)],
      limit,
      columns: { id: true, title: true, type: true },
      with: RESOURCE_PREVIEW_RELATIONS,
    });

    return results.map((r) => ({
      id: r.id,
      title: r.title,
      type: r.type,
      subjectCode: r.subjectOffering.subject.code,
    }));
  }
}
