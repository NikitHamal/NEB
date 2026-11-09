-- Rename tables (data-preserving)
ALTER TABLE "notes" RENAME TO "resources";--> statement-breakpoint
ALTER TABLE "note_files" RENAME TO "resource_files";--> statement-breakpoint
ALTER TABLE "user_archived_notes" RENAME TO "user_bookmarked_resources";--> statement-breakpoint
ALTER TABLE "user_recent_notes" RENAME TO "user_recent_resources";--> statement-breakpoint

-- Rename columns
ALTER TABLE "resource_files" RENAME COLUMN "note_id" TO "resource_id";--> statement-breakpoint
ALTER TABLE "user_bookmarked_resources" RENAME COLUMN "note_id" TO "resource_id";--> statement-breakpoint
ALTER TABLE "user_bookmarked_resources" RENAME COLUMN "archived_at" TO "bookmarked_at";--> statement-breakpoint
ALTER TABLE "user_recent_resources" RENAME COLUMN "note_id" TO "resource_id";--> statement-breakpoint

-- Rename indexes to match the new table/column names
ALTER INDEX "idx_notes_subject_id" RENAME TO "idx_resources_offering_id";--> statement-breakpoint
ALTER INDEX "idx_notes_uploaded_by" RENAME TO "idx_resources_uploaded_by";--> statement-breakpoint
ALTER INDEX "idx_note_files_note_id" RENAME TO "idx_resource_files_resource_id";--> statement-breakpoint
ALTER INDEX "idx_user_archived_notes_user_id" RENAME TO "idx_user_bookmarked_resources_user_id";--> statement-breakpoint
ALTER INDEX "idx_user_recent_notes_user_id" RENAME TO "idx_user_recent_resources_user_id";--> statement-breakpoint

-- Rename constraints to match the new table/column names
ALTER TABLE "resources" RENAME CONSTRAINT "notes_offering_id_subject_offerings_id_fk" TO "resources_offering_id_subject_offerings_id_fk";--> statement-breakpoint
ALTER TABLE "resources" RENAME CONSTRAINT "notes_uploaded_by_users_id_fk" TO "resources_uploaded_by_users_id_fk";--> statement-breakpoint
ALTER TABLE "resource_files" RENAME CONSTRAINT "note_files_note_id_notes_id_fk" TO "resource_files_resource_id_resources_id_fk";--> statement-breakpoint
ALTER TABLE "user_bookmarked_resources" RENAME CONSTRAINT "user_archived_notes_user_id_users_id_fk" TO "user_bookmarked_resources_user_id_users_id_fk";--> statement-breakpoint
ALTER TABLE "user_bookmarked_resources" RENAME CONSTRAINT "user_archived_notes_note_id_notes_id_fk" TO "user_bookmarked_resources_resource_id_resources_id_fk";--> statement-breakpoint
ALTER TABLE "user_bookmarked_resources" RENAME CONSTRAINT "unique_user_archived_note" TO "unique_user_bookmarked_resource";--> statement-breakpoint
ALTER TABLE "user_recent_resources" RENAME CONSTRAINT "user_recent_notes_user_id_users_id_fk" TO "user_recent_resources_user_id_users_id_fk";--> statement-breakpoint
ALTER TABLE "user_recent_resources" RENAME CONSTRAINT "user_recent_notes_note_id_notes_id_fk" TO "user_recent_resources_resource_id_resources_id_fk";--> statement-breakpoint
ALTER TABLE "user_recent_resources" RENAME CONSTRAINT "unique_user_recent_note" TO "unique_user_recent_resource";--> statement-breakpoint

-- Rename identity sequences to match the new table names
ALTER SEQUENCE "notes_id_seq" RENAME TO "resources_id_seq";--> statement-breakpoint
ALTER SEQUENCE "note_files_id_seq" RENAME TO "resource_files_id_seq";--> statement-breakpoint
ALTER SEQUENCE "user_archived_notes_id_seq" RENAME TO "user_bookmarked_resources_id_seq";--> statement-breakpoint
ALTER SEQUENCE "user_recent_notes_id_seq" RENAME TO "user_recent_resources_id_seq";--> statement-breakpoint

-- New resource type enum
CREATE TYPE "public"."resource_type_enum" AS ENUM('NOTE', 'PAST_QUESTION', 'ASSESSMENT', 'LAB_SHEET', 'BOOK', 'OTHER');--> statement-breakpoint

-- Add the type column. Every existing row predates this rename and was, by definition,
-- a plain note, so backfill with 'NOTE' via a temporary default, then drop the default
-- so future inserts must specify a type explicitly.
ALTER TABLE "resources" ADD COLUMN "type" "resource_type_enum" DEFAULT 'NOTE' NOT NULL;--> statement-breakpoint
ALTER TABLE "resources" ALTER COLUMN "type" DROP DEFAULT;
