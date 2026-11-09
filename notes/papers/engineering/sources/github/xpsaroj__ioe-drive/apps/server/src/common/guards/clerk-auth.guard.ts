import { CanActivate, ExecutionContext, Injectable, UnauthorizedException } from "@nestjs/common";
import type { Request } from "express";

import { ClerkIdentityResolver } from "../../clerk/clerk-identity.resolver";
import type { UserRole } from "../../database/schema";
import { toFetchRequest } from "../utils/fetch-request";

export interface AuthenticatedUser {
  id: number;
  clerkUserId: string;
  role: UserRole;
}

export type RequestWithAuthUser = Request & { authUser?: AuthenticatedUser };

// Also requires a matching local `users` row - rejects even if Clerk itself considers the request signed in.
@Injectable()
export class ClerkAuthGuard implements CanActivate {
  constructor(private readonly clerkIdentityResolver: ClerkIdentityResolver) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest<RequestWithAuthUser>();

    const user = await this.clerkIdentityResolver.resolve(toFetchRequest(request));

    if (!user) {
      throw new UnauthorizedException("User not authenticated");
    }

    request.authUser = user;
    return true;
  }
}
