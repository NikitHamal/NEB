-- Rename tables (data-preserving) - these were resource-specific all along but predate
-- marketplace listings having their own reports/moderation_actions, so they never needed
-- a qualifier until now.
ALTER TABLE "reports" RENAME TO "resource_reports";--> statement-breakpoint
ALTER TABLE "moderation_actions" RENAME TO "resource_moderation_actions";--> statement-breakpoint

-- Rename indexes to match the new table names
ALTER INDEX "idx_reports_resource_id" RENAME TO "idx_resource_reports_resource_id";--> statement-breakpoint
ALTER INDEX "idx_reports_status" RENAME TO "idx_resource_reports_status";--> statement-breakpoint
ALTER INDEX "idx_moderation_actions_resource_id" RENAME TO "idx_resource_moderation_actions_resource_id";--> statement-breakpoint

-- Rename constraints to match the new table names
ALTER TABLE "resource_reports" RENAME CONSTRAINT "reports_resource_id_resources_id_fk" TO "resource_reports_resource_id_resources_id_fk";--> statement-breakpoint
ALTER TABLE "resource_reports" RENAME CONSTRAINT "reports_reported_by_users_id_fk" TO "resource_reports_reported_by_users_id_fk";--> statement-breakpoint
ALTER TABLE "resource_reports" RENAME CONSTRAINT "reports_resolved_by_users_id_fk" TO "resource_reports_resolved_by_users_id_fk";--> statement-breakpoint
ALTER TABLE "resource_reports" RENAME CONSTRAINT "unique_report_per_user_resource" TO "unique_resource_report_per_user_resource";--> statement-breakpoint
ALTER TABLE "resource_moderation_actions" RENAME CONSTRAINT "moderation_actions_resource_id_resources_id_fk" TO "resource_moderation_actions_resource_id_resources_id_fk";--> statement-breakpoint
ALTER TABLE "resource_moderation_actions" RENAME CONSTRAINT "moderation_actions_actor_id_users_id_fk" TO "resource_moderation_actions_actor_id_users_id_fk";--> statement-breakpoint

-- Rename identity sequences to match the new table names
ALTER SEQUENCE "reports_id_seq" RENAME TO "resource_reports_id_seq";--> statement-breakpoint
ALTER SEQUENCE "moderation_actions_id_seq" RENAME TO "resource_moderation_actions_id_seq";
