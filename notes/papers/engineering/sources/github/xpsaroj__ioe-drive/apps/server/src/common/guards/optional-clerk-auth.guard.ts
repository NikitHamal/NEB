import { CanActivate, ExecutionContext, Injectable } from "@nestjs/common";

import { ClerkIdentityResolver } from "../../clerk/clerk-identity.resolver";
import { toFetchRequest } from "../utils/fetch-request";
import type { RequestWithAuthUser } from "./clerk-auth.guard";

// Same identity resolution as ClerkAuthGuard, but never rejects - populates request.authUser if present, undefined otherwise.
@Injectable()
export class OptionalClerkAuthGuard implements CanActivate {
  constructor(private readonly clerkIdentityResolver: ClerkIdentityResolver) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest<RequestWithAuthUser>();

    request.authUser = await this.clerkIdentityResolver.resolve(toFetchRequest(request));
    return true;
  }
}
