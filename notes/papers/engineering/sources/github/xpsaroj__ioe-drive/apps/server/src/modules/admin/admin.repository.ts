import { Inject, Injectable } from "@nestjs/common";
import { eq } from "drizzle-orm";

import { DRIZZLE } from "../../database/database.constants";
import type { DrizzleDb } from "../../database/database.types";
import { roleChangesTable, usersTable, type UserRole } from "../../database/schema";

@Injectable()
export class AdminRepository {
  constructor(@Inject(DRIZZLE) private readonly db: DrizzleDb) {}

  findUserByEmail(email: string) {
    return this.db.query.usersTable.findFirst({
      where: eq(usersTable.email, email),
      columns: { id: true, email: true, fullName: true, role: true },
    });
  }

  // Same transaction as the role_changes insert, mirroring ModerationRepository.recordResourceModerationAction.
  async changeUserRole(userId: number, changedBy: number, previousRole: UserRole, newRole: UserRole) {
    return this.db.transaction(async (tx) => {
      const [updatedUser] = await tx
        .update(usersTable)
        .set({ role: newRole })
        .where(eq(usersTable.id, userId))
        .returning();

      await tx.insert(roleChangesTable).values({ userId, changedBy, previousRole, newRole });

      return updatedUser;
    });
  }
}
