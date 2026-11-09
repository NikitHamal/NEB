import { BadRequestException, Inject, Injectable, NotFoundException } from "@nestjs/common";

import { DRIZZLE } from "../../database/database.constants";
import type { DrizzleDb } from "../../database/database.types";
import type { AuthenticatedUser } from "../../common/guards/clerk-auth.guard";
import { AzureBlobService } from "../../storage/azure-blob.service";
import { MAX_RESOURCE_TOTAL_SIZE_BYTES } from "../../storage/file-upload.config";
import type { ResourceLinkInput } from "./dto/resource-link-input.dto";
import { ResourcesRepository } from "./resources.repository";
import { MAX_RESOURCE_LINKS, type CreateResourceData, type UpdateResourceData } from "./resources.types";

@Injectable()
export class ResourcesService {
  constructor(
    private readonly resourcesRepository: ResourcesRepository,
    private readonly azureBlobService: AzureBlobService,
    @Inject(DRIZZLE) private readonly db: DrizzleDb,
  ) { }

  /** Checked before uploading to Azure, so a rejected request doesn't burn storage/bandwidth. */
  private assertWithinTotalSizeLimit(existingBytes: number, incomingFiles: Express.Multer.File[]): void {
    const incomingBytes = incomingFiles.reduce((total, file) => total + file.size, 0);

    if (existingBytes + incomingBytes > MAX_RESOURCE_TOTAL_SIZE_BYTES) {
      const maxMb = MAX_RESOURCE_TOTAL_SIZE_BYTES / (1024 * 1024);
      throw new BadRequestException(`A resource's files can total at most ${maxMb} MB combined.`);
    }
  }

  private assertWithinLinkCap(existingCount: number, incomingCount: number): void {
    if (existingCount + incomingCount > MAX_RESOURCE_LINKS) {
      throw new BadRequestException(`A resource can have at most ${MAX_RESOURCE_LINKS} links.`);
    }
  }

  private async uploadFiles(files: Express.Multer.File[]) {
    return Promise.all(
      files.map(async (file) => {
        const blobName = this.azureBlobService.generateBlobName(file.originalname, "resources");
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

  async createResource(
    userId: number,
    resourceData: Omit<CreateResourceData, "uploadedBy" | "status">,
    resourceFiles: Express.Multer.File[],
    links: ResourceLinkInput[] = [],
  ) {
    if (resourceFiles.length === 0 && links.length === 0) {
      throw new BadRequestException("A resource needs at least one file or link.");
    }

    const existingSubject = await this.db.query.subjectOfferingsTable.findFirst({
      where: (fields, { eq }) => eq(fields.id, resourceData.offeringId),
      columns: { id: true },
    });

    if (!existingSubject) {
      throw new NotFoundException("Subject offering not found");
    }

    this.assertWithinTotalSizeLimit(0, resourceFiles);
    this.assertWithinLinkCap(0, links.length);

    const uploadedFiles = await this.uploadFiles(resourceFiles);

    return this.resourcesRepository.create(
      { ...resourceData, uploadedBy: userId, status: "PENDING" },
      uploadedFiles,
      links,
    );
  }

  async updateResource(userId: number, resourceId: number, updateData: UpdateResourceData) {
    const existingResource = await this.resourcesRepository.findById(resourceId);

    if (!existingResource || existingResource.uploadedBy !== userId) {
      throw new NotFoundException("Resource not found");
    }

    if (existingResource.status === "REMOVED") {
      throw new BadRequestException("This resource has been removed and can no longer be edited.");
    }

    // Editing a rejected resource is treated as an implicit resubmission - back to the
    // review queue, with the previous moderation verdict cleared. Approved/pending
    // resources are left as-is by an edit.
    const resubmission =
      existingResource.status === "REJECTED"
        ? {
            status: "PENDING" as const,
            moderatedBy: null,
            moderationReason: null,
            moderationNote: null,
            moderatedAt: null,
          }
        : {};

    return this.resourcesRepository.update(resourceId, userId, { ...updateData, ...resubmission });
  }

  async deleteResource(userId: number, resourceId: number): Promise<void> {
    const existingResource = await this.resourcesRepository.findForDeletion(resourceId);

    if (!existingResource || existingResource.uploadedBy !== userId) {
      throw new NotFoundException("Resource not found");
    }

    await Promise.all(existingResource.files.map((file) => this.azureBlobService.delete(file.blobName)));
    await this.resourcesRepository.delete(resourceId);
  }

  /** Verifies a resource exists and is owned by the given user - shared by every
   * action below that mutates an existing resource or its files. A resource that
   * doesn't exist and one that isn't yours are indistinguishable (both 404), so a
   * non-owner can't probe for a resource's existence. A REMOVED resource's files were
   * already purged by moderation, so it's terminal - no further file changes either. */
  private async assertOwnership(userId: number, resourceId: number): Promise<void> {
    const resource = await this.resourcesRepository.findOwnership(resourceId);

    if (!resource || resource.uploadedBy !== userId) {
      throw new NotFoundException("Resource not found");
    }

    if (resource.status === "REMOVED") {
      throw new BadRequestException("This resource has been removed and can no longer be edited.");
    }
  }

  async addResourceFiles(userId: number, resourceId: number, files: Express.Multer.File[]): Promise<void> {
    await this.assertOwnership(userId, resourceId);

    const existingBytes = await this.resourcesRepository.sumFileSizesByResourceId(resourceId);
    this.assertWithinTotalSizeLimit(existingBytes, files);

    const uploadedFiles = await this.uploadFiles(files);
    await this.resourcesRepository.addFiles(resourceId, uploadedFiles);
  }

  /** Blocks deleting a resource's last remaining file/link - it always needs at least one. */
  private async assertContentRemainsAfterRemoval(
    resourceId: number,
    removing: { files?: number; links?: number },
  ): Promise<void> {
    const [fileCount, linkCount] = await Promise.all([
      this.resourcesRepository.countFilesByResourceId(resourceId),
      this.resourcesRepository.countLinksByResourceId(resourceId),
    ]);

    const remainingFiles = fileCount - (removing.files ?? 0);
    const remainingLinks = linkCount - (removing.links ?? 0);

    if (remainingFiles <= 0 && remainingLinks <= 0) {
      throw new BadRequestException("A resource needs at least one file or link - add another before removing this one.");
    }
  }

  async removeResourceFile(userId: number, resourceId: number, fileId: number): Promise<void> {
    await this.assertOwnership(userId, resourceId);

    const file = await this.resourcesRepository.findFile(resourceId, fileId);

    if (!file) {
      throw new NotFoundException("File not found");
    }

    await this.assertContentRemainsAfterRemoval(resourceId, { files: 1 });

    await this.azureBlobService.delete(file.blobName);
    await this.resourcesRepository.deleteFile(fileId);
  }

  async addResourceLinks(userId: number, resourceId: number, links: ResourceLinkInput[]): Promise<void> {
    await this.assertOwnership(userId, resourceId);

    const existingCount = await this.resourcesRepository.countLinksByResourceId(resourceId);
    this.assertWithinLinkCap(existingCount, links.length);

    await this.resourcesRepository.addLinks(resourceId, links);
  }

  async removeResourceLink(userId: number, resourceId: number, linkId: number): Promise<void> {
    await this.assertOwnership(userId, resourceId);

    const link = await this.resourcesRepository.findLink(resourceId, linkId);

    if (!link) {
      throw new NotFoundException("Link not found");
    }

    await this.assertContentRemainsAfterRemoval(resourceId, { links: 1 });

    await this.resourcesRepository.deleteLink(linkId);
  }

  /** PENDING/REJECTED/REMOVED files are only downloadable by their uploader or a moderator/admin - everyone else gets the same 404 as a nonexistent file. */
  async getFileDownloadUrl(
    resourceId: number,
    fileId: number,
    viewer: AuthenticatedUser,
    forceDownload = false,
  ): Promise<string> {
    const file = await this.resourcesRepository.findFile(resourceId, fileId);

    if (!file) {
      throw new NotFoundException("File not found");
    }

    const isVisible =
      file.resource.status === "APPROVED" ||
      viewer.id === file.resource.uploadedBy ||
      viewer.role === "MODERATOR" ||
      viewer.role === "ADMIN";

    if (!isVisible) {
      throw new NotFoundException("File not found");
    }

    if (forceDownload) {
      await this.resourcesRepository.incrementDownloadCount(resourceId);
    }

    // Strip chars that'd break Content-Disposition syntax (user-supplied filename).
    const safeFileName = file.originalFileName.replace(/["\r\n]/g, "");
    const disposition = forceDownload ? "attachment" : "inline";

    return this.azureBlobService.generateSasUrl(file.blobName, {
      contentDisposition: `${disposition}; filename="${safeFileName}"`,
    });
  }

  /** `viewer` is absent for an anonymous request (OptionalClerkAuthGuard). An APPROVED
   * resource is visible to anyone; anything else (PENDING/REJECTED/REMOVED) only to its
   * own uploader or a moderator/admin - everyone else gets the same 404 as a nonexistent
   * resource, so a pending resource's existence can't be probed for. */
  async findResourceById(resourceId: number, viewer?: AuthenticatedUser) {
    const resource = await this.resourcesRepository.findById(resourceId);

    if (!resource) {
      throw new NotFoundException("Resource not found");
    }

    const isVisible =
      resource.status === "APPROVED" ||
      (viewer && (viewer.id === resource.uploadedBy || viewer.role === "MODERATOR" || viewer.role === "ADMIN"));

    if (!isVisible) {
      throw new NotFoundException("Resource not found");
    }

    return resource;
  }

  findResources(
    filters: { offeringId?: number; userId?: number; q?: string; includeAllStatuses?: boolean },
    pagination: { limit: number; offset: number },
  ) {
    return this.resourcesRepository.findMany(filters, pagination);
  }

  searchSuggestions(q: string, limit: number) {
    return this.resourcesRepository.searchSuggestions(q, limit);
  }

  findAllApprovedResourceIds() {
    return this.resourcesRepository.findAllApprovedIds();
  }

  /** Same visibility rule as findResourceById, so this can't leak non-approved resource existence. */
  async findSimilarResources(resourceId: number, limit: number, viewer?: AuthenticatedUser) {
    const resource = await this.resourcesRepository.findOfferingId(resourceId);

    const isVisible =
      resource &&
      (resource.status === "APPROVED" ||
        (viewer && (viewer.id === resource.uploadedBy || viewer.role === "MODERATOR" || viewer.role === "ADMIN")));

    if (!isVisible) {
      throw new NotFoundException("Resource not found");
    }

    return this.resourcesRepository.findSimilar(resourceId, resource.offeringId, limit);
  }
}
