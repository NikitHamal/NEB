import { BadRequestException, ForbiddenException, Injectable, NotFoundException } from "@nestjs/common";

import type { AuthenticatedUser } from "../../common/guards/clerk-auth.guard";
import { MarketplaceListingsService } from "../marketplace/marketplace-listings.service";
import { ProgramsRepository } from "../programs/programs.repository";
import { ResourcesRepository } from "../resources/resources.repository";
import { ResourcesService } from "../resources/resources.service";
import { UsersRepository } from "../users/users.repository";
import type { UpdateProfileDto } from "./dto/update-profile.dto";
import { MeRepository } from "./me.repository";

// Only this program's students run to semester 10 - everyone else caps at 8.
const ARCHITECTURE_PROGRAM_CODE = "BAR";

@Injectable()
export class MeService {
  constructor(
    private readonly usersRepository: UsersRepository,
    private readonly resourcesService: ResourcesService,
    private readonly resourcesRepository: ResourcesRepository,
    private readonly marketplaceListingsService: MarketplaceListingsService,
    private readonly meRepository: MeRepository,
    private readonly programsRepository: ProgramsRepository,
  ) {}

  async getProfile(userId: number) {
    const profile = await this.usersRepository.findOwnProfileById(userId);

    if (!profile) {
      throw new NotFoundException("User not found");
    }

    return profile;
  }

  async updateProfile(userId: number, data: UpdateProfileDto): Promise<void> {
    const existingProfile = await this.usersRepository.findProfileByUserId(userId);

    if (!existingProfile) {
      throw new NotFoundException("User profile not found");
    }

    if (data.semester !== undefined && Number(data.semester) > 8) {
      const effectiveProgramId = data.programId ?? existingProfile.programId;
      const program = effectiveProgramId ? await this.programsRepository.findById(effectiveProgramId) : null;

      if (program?.code !== ARCHITECTURE_PROGRAM_CODE) {
        throw new BadRequestException("Only Architecture (BAR) students can select a semester beyond 8.");
      }
    }

    await this.usersRepository.updateProfile(userId, {
      ...(data.bio !== undefined ? { bio: data.bio } : {}),
      ...(data.programId !== undefined ? { programId: data.programId } : {}),
      ...(data.semester !== undefined ? { semester: data.semester } : {}),
      ...(data.college !== undefined ? { college: data.college } : {}),
    });
  }

  /** Delegates to ResourcesService.findResources - the exact same query as
   * GET /api/resources?userId=, just with the filter fixed to the caller and every
   * status included (not just APPROVED) - this is how an uploader sees their own
   * pending/rejected/removed resources and any moderation reason attached to them. */
  getUploadedResources(userId: number, pagination: { limit: number; offset: number }) {
    return this.resourcesService.findResources({ userId, includeAllStatuses: true }, pagination);
  }

  getMyMarketplaceListings(userId: number, pagination: { limit: number; offset: number }) {
    return this.marketplaceListingsService.findListings({ userId, includeAllStatuses: true }, pagination);
  }

  getRecentlyAccessedResources(userId: number, pagination: { limit: number; offset: number }) {
    return this.meRepository.findRecentResources(userId, pagination);
  }

  getBookmarkedResources(userId: number, pagination: { limit: number; offset: number }) {
    return this.meRepository.findBookmarkedResources(userId, pagination);
  }

  getBookmarkedResourceIds(userId: number) {
    return this.meRepository.findBookmarkedResourceIds(userId);
  }

  getWeeklySummary(userId: number) {
    const since = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
    return this.meRepository.getWeeklySummary(userId, since);
  }

  /** Same visibility rule as ResourcesService.findResourceById - APPROVED, or the viewer
   * is the uploader/a moderator/admin. Anything else 404s, so a pending/rejected/removed
   * resource's existence can't be probed for via the recent/bookmark endpoints either. */
  private async assertResourceVisible(viewer: AuthenticatedUser, resourceId: number): Promise<void> {
    const resource = await this.resourcesRepository.findOwnership(resourceId);

    const isVisible =
      resource &&
      (resource.status === "APPROVED" ||
        resource.uploadedBy === viewer.id ||
        viewer.role === "MODERATOR" ||
        viewer.role === "ADMIN");

    if (!isVisible) {
      throw new NotFoundException("Resource not found");
    }
  }

  async markResourceAsRecentlyAccessed(viewer: AuthenticatedUser, resourceId: number): Promise<void> {
    await this.assertResourceVisible(viewer, resourceId);
    await this.meRepository.markRecentlyAccessed(viewer.id, resourceId);
  }

  async markResourceAsBookmarked(viewer: AuthenticatedUser, resourceId: number): Promise<void> {
    await this.assertResourceVisible(viewer, resourceId);
    await this.meRepository.markBookmarked(viewer.id, resourceId);
  }

  async unmarkResourceAsBookmarked(userId: number, resourceId: number): Promise<void> {
    await this.meRepository.unmarkBookmarked(userId, resourceId);
  }

  getVoteValues(userId: number) {
    return this.meRepository.findVoteValues(userId);
  }

  async setResourceVote(userId: number, resourceId: number, value: number): Promise<void> {
    await this.assertVotable(userId, resourceId);
    await this.meRepository.setVote(userId, resourceId, value);
  }

  async clearResourceVote(userId: number, resourceId: number): Promise<void> {
    await this.assertVotable(userId, resourceId);
    await this.meRepository.clearVote(userId, resourceId);
  }

  private async assertVotable(userId: number, resourceId: number): Promise<void> {
    const resource = await this.resourcesRepository.findOwnership(resourceId);

    if (!resource) {
      throw new NotFoundException("Resource not found");
    }

    if (resource.uploadedBy === userId) {
      throw new ForbiddenException("You can't vote on your own resource");
    }

    if (resource.status !== "APPROVED") {
      throw new BadRequestException("Only approved resources can be voted on");
    }
  }
}
