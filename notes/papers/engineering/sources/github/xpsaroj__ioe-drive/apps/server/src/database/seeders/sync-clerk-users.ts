import { eq } from "drizzle-orm";

import { buildClerkClient } from "../../clerk/clerk-client.factory";
import { profilesTable, usersTable } from "../schema";
import { db } from "../seed-db";

// Restricted to Clerk development instances (sk_test_ keys) only.
async function syncUsers() {
  const secretKey = process.env.CLERK_SECRET_KEY;
  const publishableKey = process.env.CLERK_PUBLISHABLE_KEY;

  if (!secretKey?.startsWith("sk_test_")) {
    console.error("Error: CLERK_SECRET_KEY must be a development instance key (sk_test_) for syncing users.");
    process.exit(1);
  }

  const clerkClient = buildClerkClient(secretKey, publishableKey ?? "");

  let offset = 0;
  const limit = 100;

  while (true) {
    const { data: clerkUsers } = await clerkClient.users.getUserList({
      limit,
      offset,
      orderBy: "+created_at",
    });

    if (clerkUsers.length === 0) {
      break;
    }

    for (const clerkUser of clerkUsers) {
      await db.transaction(async (tx) => {
        const email = clerkUser.primaryEmailAddress?.emailAddress ?? null;
        const fullName =
          [clerkUser.firstName, clerkUser.lastName].filter(Boolean).join(" ").trim() || "Unknown User";

        const existingUser = await tx.query.usersTable.findFirst({
          where: eq(usersTable.clerkUserId, clerkUser.id),
        });

        let userId: number;

        if (!existingUser) {
          const [user] = await tx
            .insert(usersTable)
            .values({ clerkUserId: clerkUser.id, fullName, email })
            .returning();

          userId = user!.id;
          console.log(`Created user: ${email ?? clerkUser.id}`);
        } else {
          const [user] = await tx
            .update(usersTable)
            .set({ fullName, email })
            .where(eq(usersTable.id, existingUser.id))
            .returning();

          userId = user!.id;
          console.log(`Updated user: ${email ?? clerkUser.id}`);
        }

        const existingProfile = await tx.query.profilesTable.findFirst({
          where: eq(profilesTable.userId, userId),
        });

        if (!existingProfile) {
          await tx.insert(profilesTable).values({ userId, profilePictureUrl: clerkUser.imageUrl });
          console.log(`Created profile: ${email ?? clerkUser.id}`);
        } else {
          await tx
            .update(profilesTable)
            .set({ profilePictureUrl: clerkUser.imageUrl })
            .where(eq(profilesTable.userId, userId));
          console.log(`Updated profile: ${email ?? clerkUser.id}`);
        }
      });
    }

    offset += limit;
  }

  console.log("Finished syncing Clerk users.");
}

syncUsers()
  .then(() => {
    console.log("User sync completed successfully.");
    process.exit(0);
  })
  .catch((error) => {
    console.error("User sync failed:", error);
    process.exit(1);
  });
