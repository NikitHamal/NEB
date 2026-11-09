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
  createResourceFileValidationPipe,
  MAX_RESOURCE_FILES,
  RESOURCE_FILE_FIELD,
  resourceFileMulterOptions,
} from "../../storage/file-upload.config";
import { ModerationService } from "../moderation/moderation.service";
import { AddResourceLinksDto } from "./dto/add-resource-links.dto";
import { CreateResourceDto } from "./dto/create-resource.dto";
import { GetFileDownloadUrlQueryDto } from "./dto/get-file-download-url-query.dto";
import { GetResourcesQueryDto } from "./dto/get-resources-query.dto";
import { GetSimilarResourcesQueryDto } from "./dto/get-similar-resources-query.dto";
import { ModerateResourceDto } from "./dto/moderate-resource.dto";
import { ReportResourceDto } from "./dto/report-resource.dto";
import { SearchSuggestionsQueryDto } from "./dto/search-suggestions-query.dto";
import { UpdateResourceDto } from "./dto/update-resource.dto";
import { ResourcesService } from "./resources.service";

@Controller("resources")
export class ResourcesController {
  constructor(
    private readonly resourcesService: ResourcesService,
    private readonly moderationService: ModerationService,
  ) {}

  /** POST /api/resources - create a new resource (requires authentication). */
  @Post()
  @UseGuards(ClerkAuthGuard)
  @HttpCode(HttpStatus.CREATED)
  @UseInterceptors(FilesInterceptor(RESOURCE_FILE_FIELD, MAX_RESOURCE_FILES, resourceFileMulterOptions))
  async create(
    @CurrentUser() user: AuthenticatedUser,
    @Body() dto: CreateResourceDto,
    @UploadedFiles(createResourceFileValidationPipe()) files: Express.Multer.File[],
  ) {
    const { links, ...resourceFields } = dto;
    const resource = await this.resourcesService.createResource(user.id, resourceFields, files ?? [], links);
    return ApiResponse.of(resource, "Resource created successfully");
  }

  // PATCH /api/resources/:resourceId - must be the uploader.
  @Patch(":resourceId")
  @UseGuards(ClerkAuthGuard)
  async update(
    @CurrentUser() user: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
    @Body() dto: UpdateResourceDto,
  ) {
    if (
      dto.title === undefined &&
      dto.description === undefined &&
      dto.type === undefined &&
      dto.offeringId === undefined
    ) {
      throw new BadRequestException("At least one field must be provided for update");
    }

    const resource = await this.resourcesService.updateResource(user.id, resourceId, dto);
    return ApiResponse.of(resource, "Resource updated successfully");
  }

  // DELETE /api/resources/:resourceId - must be the uploader.
  @Delete(":resourceId")
  @UseGuards(ClerkAuthGuard)
  async remove(@CurrentUser() user: AuthenticatedUser, @Param("resourceId", ParseIntPipe) resourceId: number) {
    await this.resourcesService.deleteResource(user.id, resourceId);
    return ApiResponse.of(null, "Resource deleted successfully");
  }

  // POST /api/resources/:resourceId/approve - moderator-only.
  @Post(":resourceId/approve")
  @UseGuards(ClerkAuthGuard, RolesGuard)
  @Roles("MODERATOR", "ADMIN")
  @HttpCode(HttpStatus.OK)
  async approve(@CurrentUser() moderator: AuthenticatedUser, @Param("resourceId", ParseIntPipe) resourceId: number) {
    const resource = await this.moderationService.approveResource(moderator.id, resourceId);
    return ApiResponse.of(resource, "Resource approved");
  }

  // POST /api/resources/:resourceId/reject - moderator-only; resubmittable, resets to pending on edit.
  @Post(":resourceId/reject")
  @UseGuards(ClerkAuthGuard, RolesGuard)
  @Roles("MODERATOR", "ADMIN")
  @HttpCode(HttpStatus.OK)
  async reject(
    @CurrentUser() moderator: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
    @Body() dto: ModerateResourceDto,
  ) {
    const resource = await this.moderationService.rejectResource(moderator.id, resourceId, dto);
    return ApiResponse.of(resource, "Resource rejected");
  }

  // POST /api/resources/:resourceId/remove - moderator-only, purges files, permanent, not resubmittable.
  @Post(":resourceId/remove")
  @UseGuards(ClerkAuthGuard, RolesGuard)
  @Roles("MODERATOR", "ADMIN")
  @HttpCode(HttpStatus.OK)
  async removeAsModerator(
    @CurrentUser() moderator: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
    @Body() dto: ModerateResourceDto,
  ) {
    const resource = await this.moderationService.removeResource(moderator.id, resourceId, dto);
    return ApiResponse.of(resource, "Resource removed");
  }

  // POST /api/resources/:resourceId/report - reporter identity is never surfaced to the uploader.
  @Post(":resourceId/report")
  @UseGuards(ClerkAuthGuard)
  @HttpCode(HttpStatus.OK)
  async report(
    @CurrentUser() user: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
    @Body() dto: ReportResourceDto,
  ) {
    await this.moderationService.reportResource(user.id, resourceId, dto);
    return ApiResponse.of(null, "Resource reported");
  }

  // POST /api/resources/:resourceId/files - must be the uploader.
  @Post(":resourceId/files")
  @UseGuards(ClerkAuthGuard)
  @UseInterceptors(FilesInterceptor(RESOURCE_FILE_FIELD, MAX_RESOURCE_FILES, resourceFileMulterOptions))
  async addFiles(
    @CurrentUser() user: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
    @UploadedFiles(createResourceFileValidationPipe()) files: Express.Multer.File[],
  ) {
    await this.resourcesService.addResourceFiles(user.id, resourceId, files ?? []);
    return ApiResponse.of(null, "Files added successfully");
  }

  // DELETE /api/resources/:resourceId/files/:fileId - must be the uploader.
  @Delete(":resourceId/files/:fileId")
  @UseGuards(ClerkAuthGuard)
  async removeFile(
    @CurrentUser() user: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
    @Param("fileId", ParseIntPipe) fileId: number,
  ) {
    await this.resourcesService.removeResourceFile(user.id, resourceId, fileId);
    return ApiResponse.of(null, "File removed successfully");
  }

  // POST /api/resources/:resourceId/links - must be the uploader.
  @Post(":resourceId/links")
  @UseGuards(ClerkAuthGuard)
  @HttpCode(HttpStatus.CREATED)
  async addLinks(
    @CurrentUser() user: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
    @Body() dto: AddResourceLinksDto,
  ) {
    await this.resourcesService.addResourceLinks(user.id, resourceId, dto.links);
    return ApiResponse.of(null, "Links added successfully");
  }

  // DELETE /api/resources/:resourceId/links/:linkId - must be the uploader.
  @Delete(":resourceId/links/:linkId")
  @UseGuards(ClerkAuthGuard)
  async removeLink(
    @CurrentUser() user: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
    @Param("linkId", ParseIntPipe) linkId: number,
  ) {
    await this.resourcesService.removeResourceLink(user.id, resourceId, linkId);
    return ApiResponse.of(null, "Link removed successfully");
  }

  // GET .../download-url - any signed-in user for APPROVED; otherwise only the uploader/a moderator.
  @Get(":resourceId/files/:fileId/download-url")
  @UseGuards(ClerkAuthGuard)
  async getFileDownloadUrl(
    @CurrentUser() user: AuthenticatedUser,
    @Param("resourceId", ParseIntPipe) resourceId: number,
    @Param("fileId", ParseIntPipe) fileId: number,
    @Query() query: GetFileDownloadUrlQueryDto,
  ) {
    const url = await this.resourcesService.getFileDownloadUrl(resourceId, fileId, user, query.download === "true");
    return { url };
  }

  // Must stay registered before `:resourceId` below so "search-suggestions" isn't swallowed as a param.
  @Get("search-suggestions")
  async searchSuggestions(@Query() query: SearchSuggestionsQueryDto) {
    const suggestions = await this.resourcesService.searchSuggestions(query.q, query.limit ?? 8);
    return ApiResponse.of(suggestions);
  }

  // Must stay registered before `:resourceId` below so "approved-ids" isn't swallowed as a param.
  @Get("approved-ids")
  findApprovedIds() {
    return this.resourcesService.findAllApprovedResourceIds();
  }

  // Public for APPROVED; non-approved only visible to its uploader or a moderator (404 otherwise).
  @Get(":resourceId")
  @UseGuards(OptionalClerkAuthGuard)
  findById(
    @Param("resourceId", ParseIntPipe) resourceId: number,
    @OptionalCurrentUser() viewer?: AuthenticatedUser,
  ) {
    return this.resourcesService.findResourceById(resourceId, viewer);
  }

  // Other resources from the same subject offering, for the "Similar Resources" panel. Same visibility as GET /:resourceId.
  @Get(":resourceId/similar")
  @UseGuards(OptionalClerkAuthGuard)
  async findSimilar(
    @Param("resourceId", ParseIntPipe) resourceId: number,
    @Query() query: GetSimilarResourcesQueryDto,
    @OptionalCurrentUser() viewer?: AuthenticatedUser,
  ) {
    const similar = await this.resourcesService.findSimilarResources(resourceId, query.limit ?? 5, viewer);
    return ApiResponse.of(similar);
  }

  // Resources filtered by subject offering, uploader, or a search query, paginated (public).
  @Get()
  async findMany(@Query() query: GetResourcesQueryDto) {
    if (!query.offeringId && !query.userId && !query.q) {
      throw new BadRequestException("Either offeringId, userId, or q must be provided");
    }

    const offset = getPaginationOffset(query.page, query.limit);
    const { items, total } = await this.resourcesService.findResources(
      { offeringId: query.offeringId, userId: query.userId, q: query.q },
      { limit: query.limit, offset },
    );

    return ApiResponse.of(items, undefined, buildPaginationMeta(query.page, query.limit, total));
  }
}
