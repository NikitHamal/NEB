import { createParamDecorator, ExecutionContext } from "@nestjs/common";

import type { RequestWithAuthUser, AuthenticatedUser } from "../guards/clerk-auth.guard";

// Only valid on routes guarded by @UseGuards(ClerkAuthGuard) - `authUser` is guaranteed set there.
export const CurrentUser = createParamDecorator((_data: unknown, ctx: ExecutionContext): AuthenticatedUser => {
  const request = ctx.switchToHttp().getRequest<RequestWithAuthUser>();
  return request.authUser!;
});

// Same as CurrentUser, but for @UseGuards(OptionalClerkAuthGuard) - `authUser` may be undefined.
export const OptionalCurrentUser = createParamDecorator(
  (_data: unknown, ctx: ExecutionContext): AuthenticatedUser | undefined => {
    const request = ctx.switchToHttp().getRequest<RequestWithAuthUser>();
    return request.authUser;
  },
);
