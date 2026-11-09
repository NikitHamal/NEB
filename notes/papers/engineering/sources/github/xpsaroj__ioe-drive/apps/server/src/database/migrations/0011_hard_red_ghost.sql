CREATE TYPE "public"."moderation_reason_enum" AS ENUM('INAPPROPRIATE_CONTENT', 'WRONG_SUBJECT', 'SPAM_OR_LOW_QUALITY', 'COPYRIGHT', 'OTHER');--> statement-breakpoint
CREATE TYPE "public"."report_status_enum" AS ENUM('OPEN', 'RESOLVED');--> statement-breakpoint
CREATE TYPE "public"."resource_status_enum" AS ENUM('PENDING', 'APPROVED', 'REJECTED', 'REMOVED');--> statement-breakpoint
CREATE TYPE "public"."user_role_enum" AS ENUM('USER', 'MODERATOR');--> statement-breakpoint
CREATE TABLE "reports" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "reports_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"resource_id" integer NOT NULL,
	"reported_by" integer NOT NULL,
	"reason" "moderation_reason_enum" NOT NULL,
	"note" text,
	"status" "report_status_enum" DEFAULT 'OPEN' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"resolved_at" timestamp,
	CONSTRAINT "unique_report_per_user_resource" UNIQUE("resource_id","reported_by")
);
--> statement-breakpoint
ALTER TABLE "users" ADD COLUMN "role" "user_role_enum" DEFAULT 'USER' NOT NULL;--> statement-breakpoint
ALTER TABLE "resources" ADD COLUMN "status" "resource_status_enum" DEFAULT 'APPROVED' NOT NULL;--> statement-breakpoint
ALTER TABLE "resources" ADD COLUMN "moderated_by" integer;--> statement-breakpoint
ALTER TABLE "resources" ADD COLUMN "moderation_reason" "moderation_reason_enum";--> statement-breakpoint
ALTER TABLE "resources" ADD COLUMN "moderation_note" text;--> statement-breakpoint
ALTER TABLE "resources" ADD COLUMN "moderated_at" timestamp;--> statement-breakpoint
ALTER TABLE "reports" ADD CONSTRAINT "reports_resource_id_resources_id_fk" FOREIGN KEY ("resource_id") REFERENCES "public"."resources"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "reports" ADD CONSTRAINT "reports_reported_by_users_id_fk" FOREIGN KEY ("reported_by") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "idx_reports_resource_id" ON "reports" USING btree ("resource_id");--> statement-breakpoint
CREATE INDEX "idx_reports_status" ON "reports" USING btree ("status");--> statement-breakpoint
ALTER TABLE "resources" ADD CONSTRAINT "resources_moderated_by_users_id_fk" FOREIGN KEY ("moderated_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "idx_resources_status" ON "resources" USING btree ("status");