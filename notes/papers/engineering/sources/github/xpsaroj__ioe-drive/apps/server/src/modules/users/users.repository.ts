import { Inject, Injectable } from "@nestjs/common";
import { eq } from "drizzle-orm";

import { DRIZZLE } from "../../database/database.constants";
import type { DrizzleDb } from "../../database/database.types";
import { profilesTable, usersTable, type Semester } from "../../database/schema";

export interface WebhookUserData {
  clerkUserId: string;
  fullName: string;
  email: string | null;
}

export interface WebhookProfileData {
  profilePictureUrl: string | null;
}

export interface ProfileUpdateData {
  bio?: string;
  programId?: number;
  semester?: Semester;
  college?: string;
}

// Shared users/profiles table access, reused by the users, me, and webhooks modules.
@Injectable()
export class UsersRepository {
  constructor(@Inject(DRIZZLE) private readonly db: DrizzleDb) {}

  // Deliberately omits clerkUserId/email, unlike findOwnProfileById below.
  findPublicProfileById(userId: number) {
    return this.db.query.usersTable.findFirst({
      where: eq(usersTable.id, userId),
      columns: { id: true, fullName: true, createdAt: true },
      with: {
        profile: {
          columns: {
            id: true,
            userId: true,
            bio: true,
            programId: true,
            semester: true,
            college: true,
            profilePictureUrl: true,
          },
          with: {
            program: { columns: { id: true, name: true, code: true } },
          },
        },
      },
    });
  }

  /** The signed-in user's own profile (GET /api/me) - full user row + profile + program. */
  findOwnProfileById(userId: number) {
    return this.db.query.usersTable.findFirst({
      where: eq(usersTable.id, userId),
      with: {
        profile: {
          with: { program: true },
        },
      },
    });
  }

  findProfileByUserId(userId: number) {
    return this.db.query.profilesTable.findFirst({
      where: eq(profilesTable.userId, userId),
    });
  }

  async updateProfile(userId: number, data: ProfileUpdateData): Promise<void> {
    if (Object.keys(data).length === 0) return;

    await this.db.update(profilesTable).set(data).where(eq(profilesTable.userId, userId));
  }

  /** Upserts a user + profile from a Clerk `user.created` webhook. */
  async createFromWebhook(userData: WebhookUserData, profileData: WebhookProfileData): Promise<void> {
    await this.db.transaction(async (tx) => {
      const [user] = await tx.insert(usersTable).values(userData).onConflictDoNothing().returning();

      if (!user) {
        throw new Error("Failed to create user");
      }

      await tx
        .insert(profilesTable)
        .values({ userId: user.id, profilePictureUrl: profileData.profilePictureUrl })
        .onConflictDoUpdate({
          target: profilesTable.userId,
          set: { profilePictureUrl: profileData.profilePictureUrl },
        });
    });
  }

  // Returns null if no matching local user exists yet (caller falls back to creating one).
  async updateFromWebhook(userData: WebhookUserData, profileData: WebhookProfileData) {
    return this.db.transaction(async (tx) => {
      const [user] = await tx
        .update(usersTable)
        .set({ fullName: userData.fullName, email: userData.email })
        .where(eq(usersTable.clerkUserId, userData.clerkUserId))
        .returning();

      if (!user) {
        return null;
      }

      await tx
        .update(profilesTable)
        .set({ profilePictureUrl: profileData.profilePictureUrl })
        .where(eq(profilesTable.userId, user.id));

      return user;
    });
  }

  async deleteByClerkUserId(clerkUserId: string): Promise<void> {
    await this.db.delete(usersTable).where(eq(usersTable.clerkUserId, clerkUserId));
  }
}
