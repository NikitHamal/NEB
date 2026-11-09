import { Body, Controller, Patch, UseGuards } from "@nestjs/common";

import { CurrentUser } from "../../common/decorators/current-user.decorator";
import { Roles } from "../../common/decorators/roles.decorator";
import { ApiResponse } from "../../common/dto/api-response";
import { ClerkAuthGuard, type AuthenticatedUser } from "../../common/guards/clerk-auth.guard";
import { RolesGuard } from "../../common/guards/roles.guard";
import { AdminService } from "./admin.service";
import { ChangeUserRoleDto } from "./dto/change-user-role.dto";

/** Every route here is ADMIN-only, enforced by the @Roles("ADMIN") guard below. */
@Controller("admin")
@UseGuards(ClerkAuthGuard, RolesGuard)
@Roles("ADMIN")
export class AdminController {
  constructor(private readonly adminService: AdminService) {}

  // Can't grant/revoke ADMIN, and refuses to touch any user who is currently an admin.
  @Patch("users/role")
  async changeUserRole(@CurrentUser() admin: AuthenticatedUser, @Body() dto: ChangeUserRoleDto) {
    const user = await this.adminService.changeUserRole(admin.id, dto.email, dto.role);
    return ApiResponse.of(user, "Role updated successfully");
  }
}
