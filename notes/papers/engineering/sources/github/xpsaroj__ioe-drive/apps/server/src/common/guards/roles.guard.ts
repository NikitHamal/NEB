import { CanActivate, ExecutionContext, ForbiddenException, Injectable } from "@nestjs/common";
import { Reflector } from "@nestjs/core";

import type { UserRole } from "../../database/schema";
import { ROLES_KEY } from "../decorators/roles.decorator";
import type { RequestWithAuthUser } from "./clerk-auth.guard";

// Runs after ClerkAuthGuard in @UseGuards(...) - relies on `request.authUser` being set.
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<UserRole[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!requiredRoles || requiredRoles.length === 0) {
      return true;
    }

    const request = context.switchToHttp().getRequest<RequestWithAuthUser>();
    const user = request.authUser;

    if (!user || !requiredRoles.includes(user.role)) {
      throw new ForbiddenException("You don't have permission to perform this action");
    }

    return true;
  }
}
