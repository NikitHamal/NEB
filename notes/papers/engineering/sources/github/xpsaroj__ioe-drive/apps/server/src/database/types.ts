import * as schemas from "./schema";

export type User = typeof schemas.usersTable.$inferSelect;
export type UserInsert = typeof schemas.usersTable.$inferInsert;
export type UserUpdate = Partial<UserInsert>;

export type Profile = typeof schemas.profilesTable.$inferSelect;
export type ProfileInsert = typeof schemas.profilesTable.$inferInsert;
export type ProfileUpdate = Partial<ProfileInsert>;

export type Notification = typeof schemas.notificationsTable.$inferSelect;
export type NotificationInsert = typeof schemas.notificationsTable.$inferInsert;

export type Message = typeof schemas.marketplaceMessagesTable.$inferSelect;
