import { createClerkClient } from "@clerk/backend";

// Shared by ClerkModule's Nest provider and the standalone sync-clerk-users seeder (outside Nest's DI).
export function buildClerkClient(secretKey: string, publishableKey: string) {
  return createClerkClient({ secretKey, publishableKey });
}
