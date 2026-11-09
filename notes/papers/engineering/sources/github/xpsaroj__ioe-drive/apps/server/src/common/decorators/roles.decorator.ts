import { SetMetadata } from "@nestjs/common";

import type { UserRole } from "../../database/schema";

export const ROLES_KEY = "roles";

// Must be paired with @UseGuards(ClerkAuthGuard, RolesGuard), in that order - RolesGuard needs request.authUser already attached.
export const Roles = (...roles: UserRole[]) => SetMetadata(ROLES_KEY, roles);
