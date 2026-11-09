import { Injectable, NotFoundException } from "@nestjs/common";

import { ResourcesRepository } from "../resources/resources.repository";
import { UsersRepository } from "./users.repository";

@Injectable()
export class UsersService {
  constructor(
    private readonly usersRepository: UsersRepository,
    private readonly resourcesRepository: ResourcesRepository,
  ) {}

  async findPublicProfileById(userId: number) {
    const profile = await this.usersRepository.findPublicProfileById(userId);

    if (!profile) {
      throw new NotFoundException("User not found");
    }

    const upvoteCount = await this.resourcesRepository.sumUpvotesByUploader(userId);

    return { ...profile, upvoteCount };
  }
}
