import {
    integer,
    pgTable,
    varchar,
    timestamp,
    text,
    pgEnum,
    unique,
    index,
    boolean,
} from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

// Enums
export const SemesterEnum = pgEnum("semester_enum", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]);
export const YearEnum = pgEnum("year_enum", ["1", "2", "3", "4", "5"]);
export const SubjectHardnessLevelEnum = pgEnum("subject_hardness_level_enum", ["EASY", "MEDIUM", "HARD", "VERY_HARD"]);
export const ResourceTypeEnum = pgEnum("resource_type_enum", ["NOTE", "PAST_QUESTION", "ASSESSMENT", "LAB_SHEET", "BOOK", "OTHER"]);
// Granting/revoking ADMIN itself is never done through the app - only ever a direct database change.
export const UserRoleEnum = pgEnum("user_role_enum", ["USER", "MODERATOR", "ADMIN"]);
// REJECTED is resubmittable (edit -> back to PENDING); REMOVED is terminal (files deleted, row kept).
export const ResourceStatusEnum = pgEnum("resource_status_enum", ["PENDING", "APPROVED", "REJECTED", "REMOVED"]);
export const ModerationReasonEnum = pgEnum("moderation_reason_enum", [
    "INAPPROPRIATE_CONTENT",
    "WRONG_SUBJECT",
    "SPAM_OR_LOW_QUALITY",
    "COPYRIGHT",
    "MISLEADING_OR_BROKEN_LINK",
    "OTHER",
]);
export const ReportStatusEnum = pgEnum("report_status_enum", ["OPEN", "RESOLVED"]);
export const ModerationActionEnum = pgEnum("moderation_action_enum", ["APPROVE", "REJECT", "REMOVE"]);
export const NotificationTypeEnum = pgEnum("notification_type_enum", [
    "RESOURCE_APPROVED",
    "RESOURCE_REJECTED",
    "RESOURCE_REMOVED",
    "LISTING_APPROVED",
    "LISTING_REJECTED",
    "LISTING_REMOVED",
]);

export const MarketplaceListingTypeEnum = pgEnum("marketplace_listing_type_enum", ["SELLING", "WANTED"]);
export const MarketplaceCategoryEnum = pgEnum("marketplace_category_enum", [
    "TEXTBOOKS_AND_NOTES",
    "DRAFTING_AND_STATIONERY",
    "CALCULATORS_AND_ELECTRONICS",
    "LAB_AND_WORKSHOP_EQUIPMENT",
    "FURNITURE_AND_HOSTEL_ITEMS",
    "OTHER",
]);
// PENDING is pre-review (new listing, invisible except to poster/moderators); REJECTED is resubmittable
// (edit -> back to PENDING); FULFILLED is owner-driven and reversible (reactivate); REMOVED is
// moderator-driven and terminal, photos purged.
export const MarketplaceListingStatusEnum = pgEnum("marketplace_listing_status_enum", [
    "PENDING",
    "ACTIVE",
    "FULFILLED",
    "REJECTED",
    "REMOVED",
]);
export const MarketplaceReportReasonEnum = pgEnum("marketplace_report_reason_enum", [
    "SCAM_OR_FRAUD",
    "PROHIBITED_ITEM",
    "INAPPROPRIATE_CONTENT",
    "SPAM_OR_MISLEADING",
    "ALREADY_SOLD_OR_UNAVAILABLE",
    "OTHER",
]);

export type Semester = (typeof SemesterEnum.enumValues)[number];
export type Year = (typeof YearEnum.enumValues)[number];
export type SubjectHardnessLevel = (typeof SubjectHardnessLevelEnum.enumValues)[number];
export type ResourceType = (typeof ResourceTypeEnum.enumValues)[number];
export type UserRole = (typeof UserRoleEnum.enumValues)[number];
export type ResourceStatus = (typeof ResourceStatusEnum.enumValues)[number];
export type ModerationReason = (typeof ModerationReasonEnum.enumValues)[number];
export type ReportStatus = (typeof ReportStatusEnum.enumValues)[number];
export type ModerationAction = (typeof ModerationActionEnum.enumValues)[number];
export type NotificationType = (typeof NotificationTypeEnum.enumValues)[number];
export type MarketplaceListingType = (typeof MarketplaceListingTypeEnum.enumValues)[number];
export type MarketplaceCategory = (typeof MarketplaceCategoryEnum.enumValues)[number];
export type MarketplaceListingStatus = (typeof MarketplaceListingStatusEnum.enumValues)[number];
export type MarketplaceReportReason = (typeof MarketplaceReportReasonEnum.enumValues)[number];

// Tables
export const webhookEventsTable = pgTable("webhook_events", {
    svixId: text("svix_id").primaryKey(),
    eventType: varchar("event_type", { length: 255 }).notNull(),
    receivedAt: timestamp("received_at").defaultNow(),
});

export const programsTable = pgTable("programs", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    code: varchar("code", { length: 10 }).notNull().unique(),
    name: varchar("name", { length: 255 }).notNull(),
    totalYears: integer("total_years").default(4).notNull(),
    syllabusUrl: varchar("syllabus_url", { length: 255 }),
});

export const subjectsTable = pgTable("subjects", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    code: varchar("code", { length: 15 }).notNull().unique(),
    name: varchar("name", { length: 255 }).notNull(),
    programId: integer("program_id")
        .references(() => programsTable.id)
        .notNull(),
    hardnessLevel: SubjectHardnessLevelEnum("hardness_level").notNull(),
    description: text("description"),
    syllabusUrl: varchar("syllabus_url", { length: 255 }),
});

export const marksTable = pgTable("subject_marks", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    subjectId: integer("subject_id")
        .references(() => subjectsTable.id, { onDelete: "cascade" })
        .notNull(),
    theoryAssessment: integer("theory_assessment").notNull().default(0),
    theoryFinal: integer("theory_final").notNull().default(0),
    practicalAssessment: integer("practical_assessment").notNull().default(0),
    practicalFinal: integer("practical_final").notNull().default(0),
},
    (table) => [
        unique("unique_subject_marks").on(table.subjectId),
        index("idx_subject_marks_subject_id").on(table.subjectId),
    ]
);

export const subjectOfferingsTable = pgTable("subject_offerings", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    subjectId: integer("subject_id")
        .references(() => subjectsTable.id)
        .notNull(),
    semester: SemesterEnum("semester").notNull(),
    programId: integer("program_id")
        .references(() => programsTable.id)
        .notNull(),
    year: YearEnum("year").notNull(),
    isElective: boolean("is_elective").default(false).notNull(),
},
    (table) => [
        unique("unique_subject_offering").on(
            table.subjectId,
            table.semester,
            table.programId,
            table.year
        ),
        index("idx_subject_offerings_semester_program").on(table.semester, table.programId),
        index("idx_subject_offerings_program").on(table.programId),
        index("idx_subject_offerings_subject").on(table.subjectId),
    ]
);

export const usersTable = pgTable("users", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    clerkUserId: varchar("clerk_user_id", { length: 255 }).notNull().unique(),
    fullName: varchar("full_name", { length: 255 }).notNull(),
    email: varchar("email", { length: 255 }).unique(),
    role: UserRoleEnum("role").notNull().default("USER"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
});

export const profilesTable = pgTable("profiles", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    userId: integer("user_id")
        .references(() => usersTable.id, { onDelete: "cascade" })
        .notNull()
        .unique(),
    bio: text("bio"),
    programId: integer("program_id").references(() => programsTable.id),
    semester: SemesterEnum("semester"),
    college: text("college"),
    profilePictureUrl: text("profile_picture_url"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
});

export const resourcesTable = pgTable("resources", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    title: text("title").notNull(),
    description: text("description").notNull(),
    type: ResourceTypeEnum("type").notNull(),
    offeringId: integer("offering_id")
        .references(() => subjectOfferingsTable.id)
        .notNull(),
    uploadedBy: integer("uploaded_by")
        .references(() => usersTable.id, { onDelete: "set null" }),
    // No schema-level default - the application always sets this explicitly.
    status: ResourceStatusEnum("status").notNull(),
    moderatedBy: integer("moderated_by")
        .references(() => usersTable.id, { onDelete: "set null" }),
    moderationReason: ModerationReasonEnum("moderation_reason"),
    moderationNote: text("moderation_note"),
    moderatedAt: timestamp("moderated_at"),
    // Denormalized counters, updated on vote/download rather than COUNT()'d per row.
    upvoteCount: integer("upvote_count").notNull().default(0),
    downvoteCount: integer("downvote_count").notNull().default(0),
    downloadCount: integer("download_count").notNull().default(0),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
},
    (table) => [
        index("idx_resources_offering_id").on(table.offeringId),
        index("idx_resources_uploaded_by").on(table.uploadedBy),
        index("idx_resources_status").on(table.status),
    ]
);

export const resourceFilesTable = pgTable("resource_files", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    resourceId: integer("resource_id")
        .references(() => resourcesTable.id, { onDelete: "cascade" })
        .notNull(),
    fileUrl: text("file_url").notNull(),
    fileSize: integer("file_size").notNull(),
    originalFileName: text("original_file_name").notNull(),
    blobName: text("blob_name").notNull(),
    compressedSize: integer("compressed_size"),
    compressionMethod: varchar("compression_method", { length: 100 }),
    mimeType: varchar("mime_type", { length: 100 }).notNull(),
    uploadedAt: timestamp("uploaded_at").defaultNow().notNull(),
},
    (table) => [
        index("idx_resource_files_resource_id").on(table.resourceId),
    ]
);

export const resourceLinksTable = pgTable("resource_links", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    resourceId: integer("resource_id")
        .references(() => resourcesTable.id, { onDelete: "cascade" })
        .notNull(),
    url: text("url").notNull(),
    label: varchar("label", { length: 100 }).notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
},
    (table) => [
        unique("unique_resource_link").on(table.resourceId, table.url),
        index("idx_resource_links_resource_id").on(table.resourceId),
    ]
);

export const userRecentResourcesTable = pgTable("user_recent_resources", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    userId: integer("user_id")
        .references(() => usersTable.id, { onDelete: "cascade" })
        .notNull(),
    resourceId: integer("resource_id")
        .references(() => resourcesTable.id, { onDelete: "cascade" })
        .notNull(),
    accessedAt: timestamp("accessed_at").defaultNow().notNull(),
},
    (table) => [
        unique("unique_user_recent_resource").on(
            table.userId,
            table.resourceId
        ),
        index("idx_user_recent_resources_user_id").on(table.userId),
    ]
);

export const userBookmarkedResourcesTable = pgTable("user_bookmarked_resources", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    userId: integer("user_id")
        .references(() => usersTable.id, { onDelete: "cascade" })
        .notNull(),
    resourceId: integer("resource_id")
        .references(() => resourcesTable.id, { onDelete: "cascade" })
        .notNull(),
    bookmarkedAt: timestamp("bookmarked_at").defaultNow().notNull(),
},
    (table) => [
        unique("unique_user_bookmarked_resource").on(
            table.userId,
            table.resourceId
        ),
        index("idx_user_bookmarked_resources_user_id").on(table.userId),
    ]
);

// One row per user's current vote; aggregates live on resourcesTable, not here.
export const resourceVotesTable = pgTable("resource_votes", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    resourceId: integer("resource_id")
        .references(() => resourcesTable.id, { onDelete: "cascade" })
        .notNull(),
    userId: integer("user_id")
        .references(() => usersTable.id, { onDelete: "cascade" })
        .notNull(),
    value: integer("value").notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
},
    (table) => [
        unique("unique_user_resource_vote").on(
            table.userId,
            table.resourceId
        ),
        index("idx_resource_votes_resource_id").on(table.resourceId),
        index("idx_resource_votes_user_id").on(table.userId),
    ]
);

export const resourceReportsTable = pgTable("resource_reports", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    resourceId: integer("resource_id")
        .references(() => resourcesTable.id, { onDelete: "cascade" })
        .notNull(),
    reportedBy: integer("reported_by")
        .references(() => usersTable.id, { onDelete: "cascade" })
        .notNull(),
    reason: ModerationReasonEnum("reason").notNull(),
    note: text("note"),
    status: ReportStatusEnum("status").notNull().default("OPEN"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    resolvedAt: timestamp("resolved_at"),
    resolvedBy: integer("resolved_by")
        .references(() => usersTable.id, { onDelete: "set null" }),
},
    (table) => [
        unique("unique_resource_report_per_user_resource").on(table.resourceId, table.reportedBy),
        index("idx_resource_reports_resource_id").on(table.resourceId),
        index("idx_resource_reports_status").on(table.status),
    ]
);

// Append-only history; resourcesTable.moderatedBy/moderationReason/etc. only ever hold the latest one.
export const resourceModerationActionsTable = pgTable("resource_moderation_actions", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    resourceId: integer("resource_id")
        .references(() => resourcesTable.id, { onDelete: "cascade" })
        .notNull(),
    actorId: integer("actor_id")
        .references(() => usersTable.id, { onDelete: "set null" }),
    action: ModerationActionEnum("action").notNull(),
    reason: ModerationReasonEnum("reason"),
    note: text("note"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
},
    (table) => [
        index("idx_resource_moderation_actions_resource_id").on(table.resourceId),
    ]
);

// Granting/revoking ADMIN never goes through the admin endpoint, so it never shows up here.
export const roleChangesTable = pgTable("role_changes", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    userId: integer("user_id")
        .references(() => usersTable.id, { onDelete: "cascade" })
        .notNull(),
    changedBy: integer("changed_by")
        .references(() => usersTable.id, { onDelete: "set null" }),
    previousRole: UserRoleEnum("previous_role").notNull(),
    newRole: UserRoleEnum("new_role").notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
},
    (table) => [
        index("idx_role_changes_user_id").on(table.userId),
    ]
);

export const marketplaceListingsTable = pgTable("marketplace_listings", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    title: text("title").notNull(),
    description: text("description").notNull(),
    type: MarketplaceListingTypeEnum("type").notNull(),
    category: MarketplaceCategoryEnum("category").notNull(),
    // Whole-rupee integer; null = "contact for price" (common for WANTED listings).
    price: integer("price"),
    // Only meaningful for notes/books-type listings - not every listing has a course.
    offeringId: integer("offering_id").references(() => subjectOfferingsTable.id),
    postedBy: integer("posted_by")
        .references(() => usersTable.id, { onDelete: "set null" }),
    // No schema-level default - the application always sets this explicitly.
    status: MarketplaceListingStatusEnum("status").notNull(),
    moderatedBy: integer("moderated_by")
        .references(() => usersTable.id, { onDelete: "set null" }),
    moderationReason: MarketplaceReportReasonEnum("moderation_reason"),
    moderationNote: text("moderation_note"),
    moderatedAt: timestamp("moderated_at"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
},
    (table) => [
        index("idx_marketplace_listings_posted_by").on(table.postedBy),
        index("idx_marketplace_listings_status").on(table.status),
        index("idx_marketplace_listings_type").on(table.type),
        index("idx_marketplace_listings_category").on(table.category),
        index("idx_marketplace_listings_offering_id").on(table.offeringId),
    ]
);

export const marketplaceListingPhotosTable = pgTable("marketplace_listing_photos", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    listingId: integer("listing_id")
        .references(() => marketplaceListingsTable.id, { onDelete: "cascade" })
        .notNull(),
    photoUrl: text("photo_url").notNull(),
    fileSize: integer("file_size").notNull(),
    originalFileName: text("original_file_name").notNull(),
    blobName: text("blob_name").notNull(),
    mimeType: varchar("mime_type", { length: 100 }).notNull(),
    // Lowest sortOrder is the cover photo.
    sortOrder: integer("sort_order").notNull().default(0),
    uploadedAt: timestamp("uploaded_at").defaultNow().notNull(),
},
    (table) => [
        index("idx_marketplace_listing_photos_listing_id").on(table.listingId),
    ]
);

export const marketplaceReportsTable = pgTable("marketplace_reports", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    listingId: integer("listing_id")
        .references(() => marketplaceListingsTable.id, { onDelete: "cascade" })
        .notNull(),
    reportedBy: integer("reported_by")
        .references(() => usersTable.id, { onDelete: "cascade" })
        .notNull(),
    reason: MarketplaceReportReasonEnum("reason").notNull(),
    note: text("note"),
    status: ReportStatusEnum("status").notNull().default("OPEN"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    resolvedAt: timestamp("resolved_at"),
    resolvedBy: integer("resolved_by")
        .references(() => usersTable.id, { onDelete: "set null" }),
},
    (table) => [
        unique("unique_marketplace_report_per_user_listing").on(table.listingId, table.reportedBy),
        index("idx_marketplace_reports_listing_id").on(table.listingId),
        index("idx_marketplace_reports_status").on(table.status),
    ]
);

// Append-only history; marketplaceListingsTable.moderatedBy/moderationReason/etc. only ever hold the latest one.
export const marketplaceModerationActionsTable = pgTable("marketplace_moderation_actions", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    listingId: integer("listing_id")
        .references(() => marketplaceListingsTable.id, { onDelete: "cascade" })
        .notNull(),
    actorId: integer("actor_id")
        .references(() => usersTable.id, { onDelete: "set null" }),
    action: ModerationActionEnum("action").notNull(),
    reason: MarketplaceReportReasonEnum("reason"),
    note: text("note"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
},
    (table) => [
        index("idx_marketplace_moderation_actions_listing_id").on(table.listingId),
    ]
);

// One thread per (listing, initiator) pair - re-contacting reuses it instead of duplicating.
export const marketplaceConversationsTable = pgTable("marketplace_conversations", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    listingId: integer("listing_id")
        .references(() => marketplaceListingsTable.id, { onDelete: "cascade" })
        .notNull(),
    posterId: integer("poster_id")
        .references(() => usersTable.id, { onDelete: "cascade" })
        .notNull(),
    initiatorId: integer("initiator_id")
        .references(() => usersTable.id, { onDelete: "cascade" })
        .notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    // Bumped explicitly alongside each new message insert - $onUpdate only fires on an UPDATE to this row itself.
    updatedAt: timestamp("updated_at").defaultNow().notNull(),
},
    (table) => [
        unique("unique_marketplace_conversation_per_listing_initiator").on(table.listingId, table.initiatorId),
        index("idx_marketplace_conversations_listing_id").on(table.listingId),
        index("idx_marketplace_conversations_poster_id").on(table.posterId),
        index("idx_marketplace_conversations_initiator_id").on(table.initiatorId),
    ]
);

export const marketplaceMessagesTable = pgTable("marketplace_messages", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    conversationId: integer("conversation_id")
        .references(() => marketplaceConversationsTable.id, { onDelete: "cascade" })
        .notNull(),
    senderId: integer("sender_id")
        .references(() => usersTable.id, { onDelete: "set null" }),
    body: text("body").notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    readAt: timestamp("read_at"),
},
    (table) => [
        // Message history is always "this conversation, ordered by time" - a composite index serves that directly.
        index("idx_marketplace_messages_conversation_id_created_at").on(table.conversationId, table.createdAt),
    ]
);

// `link` is a self-contained relative URL (e.g. "/resources/r/42") rather than a FK to
// resourcesTable/marketplaceListingsTable, so deleting the underlying resource/listing
// doesn't silently wipe notification history.
export const notificationsTable = pgTable("notifications", {
    id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
    userId: integer("user_id")
        .references(() => usersTable.id, { onDelete: "cascade" })
        .notNull(),
    type: NotificationTypeEnum("type").notNull(),
    message: text("message").notNull(),
    link: text("link"),
    readAt: timestamp("read_at"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
},
    (table) => [
        index("idx_notifications_user_id").on(table.userId),
    ]
);


// Relations
export const programRelations = relations(programsTable, ({ many }) => ({
    subjects: many(subjectsTable),
    subjectOfferings: many(subjectOfferingsTable),
}))

export const subjectRelations = relations(subjectsTable, ({ many, one }) => ({
    program: one(programsTable, {
        fields: [subjectsTable.programId],
        references: [programsTable.id]
    }),
    subjectOfferings: many(subjectOfferingsTable),
    marks: one(marksTable, {
        fields: [subjectsTable.id],
        references: [marksTable.subjectId]
    }),
    resources: many(resourcesTable),
}));

export const subjectOfferingRelations = relations(subjectOfferingsTable, ({ one }) => ({
    subject: one(subjectsTable, {
        fields: [subjectOfferingsTable.subjectId],
        references: [subjectsTable.id]
    }),
    program: one(programsTable, {
        fields: [subjectOfferingsTable.programId],
        references: [programsTable.id]
    }),
}));

export const userRelations = relations(usersTable, ({ one, many }) => ({
    profile: one(profilesTable),
    // relationName pairs disambiguate tables with two FKs to usersTable (uploadedBy/moderatedBy, etc.).
    resources: many(resourcesTable, { relationName: "uploadedResources" }),
    moderatedResources: many(resourcesTable, { relationName: "moderatedResources" }),
    recentResources: many(userRecentResourcesTable),
    bookmarkedResources: many(userBookmarkedResourcesTable),
    votes: many(resourceVotesTable),
    resourceReportsFiled: many(resourceReportsTable, { relationName: "resourceReportsFiled" }),
    resourceReportsResolved: many(resourceReportsTable, { relationName: "resourceReportsResolved" }),
    resourceModerationActions: many(resourceModerationActionsTable),
    marketplaceModerationActions: many(marketplaceModerationActionsTable),
    roleChangesReceived: many(roleChangesTable, { relationName: "roleChangeSubject" }),
    roleChangesPerformed: many(roleChangesTable, { relationName: "roleChangeActor" }),
    postedMarketplaceListings: many(marketplaceListingsTable, { relationName: "postedListings" }),
    moderatedMarketplaceListings: many(marketplaceListingsTable, { relationName: "moderatedListings" }),
    marketplaceReportsFiled: many(marketplaceReportsTable, { relationName: "marketplaceReportsFiled" }),
    marketplaceReportsResolved: many(marketplaceReportsTable, { relationName: "marketplaceReportsResolved" }),
    marketplaceConversationsAsPoster: many(marketplaceConversationsTable, { relationName: "conversationsAsPoster" }),
    marketplaceConversationsAsInitiator: many(marketplaceConversationsTable, { relationName: "conversationsAsInitiator" }),
    marketplaceMessagesSent: many(marketplaceMessagesTable),
    notifications: many(notificationsTable),
}));

export const profileRelations = relations(profilesTable, ({ one }) => ({
    program: one(programsTable, {
        fields: [profilesTable.programId],
        references: [programsTable.id]
    }),
    user: one(usersTable, {
        fields: [profilesTable.userId],
        references: [usersTable.id]
    }),
}));

export const resourceRelations = relations(resourcesTable, ({ one, many }) => ({
    subjectOffering: one(subjectOfferingsTable, {
        fields: [resourcesTable.offeringId],
        references: [subjectOfferingsTable.id]
    }),
    uploader: one(usersTable, {
        fields: [resourcesTable.uploadedBy],
        references: [usersTable.id],
        relationName: "uploadedResources",
    }),
    moderator: one(usersTable, {
        fields: [resourcesTable.moderatedBy],
        references: [usersTable.id],
        relationName: "moderatedResources",
    }),
    files: many(resourceFilesTable),
    links: many(resourceLinksTable),
    reports: many(resourceReportsTable),
    moderationActions: many(resourceModerationActionsTable),
    votes: many(resourceVotesTable),
}));

export const resourceFileRelations = relations(resourceFilesTable, ({ one }) => ({
    resource: one(resourcesTable, {
        fields: [resourceFilesTable.resourceId],
        references: [resourcesTable.id]
    }),
}));

export const resourceLinkRelations = relations(resourceLinksTable, ({ one }) => ({
    resource: one(resourcesTable, {
        fields: [resourceLinksTable.resourceId],
        references: [resourcesTable.id]
    }),
}));

export const userRecentResourceRelations = relations(userRecentResourcesTable, ({ one }) => ({
    user: one(usersTable, {
        fields: [userRecentResourcesTable.userId],
        references: [usersTable.id]
    }),
    resource: one(resourcesTable, {
        fields: [userRecentResourcesTable.resourceId],
        references: [resourcesTable.id]
    }),
}));

export const userBookmarkedResourceRelations = relations(userBookmarkedResourcesTable, ({ one }) => ({
    user: one(usersTable, {
        fields: [userBookmarkedResourcesTable.userId],
        references: [usersTable.id]
    }),
    resource: one(resourcesTable, {
        fields: [userBookmarkedResourcesTable.resourceId],
        references: [resourcesTable.id]
    }),
}));

export const resourceVoteRelations = relations(resourceVotesTable, ({ one }) => ({
    resource: one(resourcesTable, {
        fields: [resourceVotesTable.resourceId],
        references: [resourcesTable.id]
    }),
    user: one(usersTable, {
        fields: [resourceVotesTable.userId],
        references: [usersTable.id]
    }),
}));

export const resourceReportRelations = relations(resourceReportsTable, ({ one }) => ({
    resource: one(resourcesTable, {
        fields: [resourceReportsTable.resourceId],
        references: [resourcesTable.id]
    }),
    reporter: one(usersTable, {
        fields: [resourceReportsTable.reportedBy],
        references: [usersTable.id],
        relationName: "resourceReportsFiled",
    }),
    resolver: one(usersTable, {
        fields: [resourceReportsTable.resolvedBy],
        references: [usersTable.id],
        relationName: "resourceReportsResolved",
    }),
}));

export const resourceModerationActionRelations = relations(resourceModerationActionsTable, ({ one }) => ({
    resource: one(resourcesTable, {
        fields: [resourceModerationActionsTable.resourceId],
        references: [resourcesTable.id]
    }),
    actor: one(usersTable, {
        fields: [resourceModerationActionsTable.actorId],
        references: [usersTable.id]
    }),
}));

export const roleChangeRelations = relations(roleChangesTable, ({ one }) => ({
    user: one(usersTable, {
        fields: [roleChangesTable.userId],
        references: [usersTable.id],
        relationName: "roleChangeSubject",
    }),
    changedByUser: one(usersTable, {
        fields: [roleChangesTable.changedBy],
        references: [usersTable.id],
        relationName: "roleChangeActor",
    }),
}));

export const marketplaceListingRelations = relations(marketplaceListingsTable, ({ one, many }) => ({
    subjectOffering: one(subjectOfferingsTable, {
        fields: [marketplaceListingsTable.offeringId],
        references: [subjectOfferingsTable.id]
    }),
    poster: one(usersTable, {
        fields: [marketplaceListingsTable.postedBy],
        references: [usersTable.id],
        relationName: "postedListings",
    }),
    moderator: one(usersTable, {
        fields: [marketplaceListingsTable.moderatedBy],
        references: [usersTable.id],
        relationName: "moderatedListings",
    }),
    photos: many(marketplaceListingPhotosTable),
    reports: many(marketplaceReportsTable),
    moderationActions: many(marketplaceModerationActionsTable),
    conversations: many(marketplaceConversationsTable),
}));

export const marketplaceListingPhotoRelations = relations(marketplaceListingPhotosTable, ({ one }) => ({
    listing: one(marketplaceListingsTable, {
        fields: [marketplaceListingPhotosTable.listingId],
        references: [marketplaceListingsTable.id]
    }),
}));

export const marketplaceReportRelations = relations(marketplaceReportsTable, ({ one }) => ({
    listing: one(marketplaceListingsTable, {
        fields: [marketplaceReportsTable.listingId],
        references: [marketplaceListingsTable.id]
    }),
    reporter: one(usersTable, {
        fields: [marketplaceReportsTable.reportedBy],
        references: [usersTable.id],
        relationName: "marketplaceReportsFiled",
    }),
    resolver: one(usersTable, {
        fields: [marketplaceReportsTable.resolvedBy],
        references: [usersTable.id],
        relationName: "marketplaceReportsResolved",
    }),
}));

export const marketplaceModerationActionRelations = relations(marketplaceModerationActionsTable, ({ one }) => ({
    listing: one(marketplaceListingsTable, {
        fields: [marketplaceModerationActionsTable.listingId],
        references: [marketplaceListingsTable.id]
    }),
    actor: one(usersTable, {
        fields: [marketplaceModerationActionsTable.actorId],
        references: [usersTable.id]
    }),
}));

export const marketplaceConversationRelations = relations(marketplaceConversationsTable, ({ one, many }) => ({
    listing: one(marketplaceListingsTable, {
        fields: [marketplaceConversationsTable.listingId],
        references: [marketplaceListingsTable.id]
    }),
    poster: one(usersTable, {
        fields: [marketplaceConversationsTable.posterId],
        references: [usersTable.id],
        relationName: "conversationsAsPoster",
    }),
    initiator: one(usersTable, {
        fields: [marketplaceConversationsTable.initiatorId],
        references: [usersTable.id],
        relationName: "conversationsAsInitiator",
    }),
    messages: many(marketplaceMessagesTable),
}));

export const marketplaceMessageRelations = relations(marketplaceMessagesTable, ({ one }) => ({
    conversation: one(marketplaceConversationsTable, {
        fields: [marketplaceMessagesTable.conversationId],
        references: [marketplaceConversationsTable.id]
    }),
    sender: one(usersTable, {
        fields: [marketplaceMessagesTable.senderId],
        references: [usersTable.id]
    }),
}));

export const notificationRelations = relations(notificationsTable, ({ one }) => ({
    user: one(usersTable, {
        fields: [notificationsTable.userId],
        references: [usersTable.id]
    }),
}));
