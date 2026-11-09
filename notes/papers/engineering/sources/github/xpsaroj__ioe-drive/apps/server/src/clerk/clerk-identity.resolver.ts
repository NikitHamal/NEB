import { Inject, Injectable } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { eq } from "drizzle-orm";

import { CLERK_CLIENT, type ClerkClient } from "./clerk.constants";
import { DRIZZLE } from "../database/database.constants";
import type { DrizzleDb } from "../database/database.types";
import { usersTable } from "../database/schema";
import type { AuthenticatedUser } from "../common/guards/clerk-auth.guard";

// Single source of truth for "who is this Fetch API Request from" - shared by ClerkAuthGuard,
// OptionalClerkAuthGuard, and the WebSocket gateway, so HTTP and socket auth never diverge.
@Injectable()
export class ClerkIdentityResolver {
  constructor(
    @Inject(CLERK_CLIENT) private readonly clerkClient: ClerkClient,
    @Inject(DRIZZLE) private readonly db: DrizzleDb,
    private readonly configService: ConfigService,
  ) {}

  async resolve(fetchRequest: Request): Promise<AuthenticatedUser | undefined> {
    const authorizedParties = this.configService
      .getOrThrow<string>("ALLOWED_ORIGINS")
      .split(",")
      .map((origin) => origin.trim());

    const requestState = await this.clerkClient.authenticateRequest(fetchRequest, {
      authorizedParties,
    });

    if (!requestState.isAuthenticated) return undefined;

    const { userId: clerkUserId } = requestState.toAuth();

    return this.db.query.usersTable.findFirst({
      where: eq(usersTable.clerkUserId, clerkUserId),
      columns: { id: true, clerkUserId: true, role: true },
    });
  }
}
