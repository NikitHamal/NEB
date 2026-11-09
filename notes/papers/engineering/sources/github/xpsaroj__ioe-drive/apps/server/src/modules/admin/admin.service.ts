import { BadRequestException, Injectable, NotFoundException } from "@nestjs/common";

import { AdminRepository } from "./admin.repository";

@Injectable()
export class AdminService {
  constructor(private readonly adminRepository: AdminRepository) {}

  // Only ever moves a user between USER and MODERATOR - refusing any current ADMIN keeps that guarantee real.
  async changeUserRole(actingAdminId: number, email: string, newRole: "USER" | "MODERATOR") {
    const targetUser = await this.adminRepository.findUserByEmail(email);

    if (!targetUser) {
      throw new NotFoundException("User not found");
    }

    if (targetUser.id === actingAdminId) {
      throw new BadRequestException("You can't change your own role");
    }

    if (targetUser.role === "ADMIN") {
      throw new BadRequestException("Admin roles can't be changed through this action");
    }

    if (targetUser.role === newRole) {
      throw new BadRequestException(`This user already has the ${newRole} role`);
    }

    return this.adminRepository.changeUserRole(targetUser.id, actingAdminId, targetUser.role, newRole);
  }
}
