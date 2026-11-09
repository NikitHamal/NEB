import { Controller, Get, Param, ParseIntPipe, UseGuards } from "@nestjs/common";

import { ClerkAuthGuard } from "../../common/guards/clerk-auth.guard";
import { UsersService } from "./users.service";

@Controller("users")
@UseGuards(ClerkAuthGuard)
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  /** GET /api/users/:userId - another user's public-ish profile. */
  @Get(":userId")
  findById(@Param("userId", ParseIntPipe) userId: number) {
    return this.usersService.findPublicProfileById(userId);
  }
}
