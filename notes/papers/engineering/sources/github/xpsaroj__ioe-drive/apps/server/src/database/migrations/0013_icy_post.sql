CREATE TYPE "public"."moderation_action_enum" AS ENUM('APPROVE', 'REJECT', 'REMOVE');--> statement-breakpoint
ALTER TYPE "public"."user_role_enum" ADD VALUE 'ADMIN';--> statement-breakpoint
CREATE TABLE "moderation_actions" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "moderation_actions_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"resource_id" integer NOT NULL,
	"actor_id" integer,
	"action" "moderation_action_enum" NOT NULL,
	"reason" "moderation_reason_enum",
	"note" text,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "role_changes" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "role_changes_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"user_id" integer NOT NULL,
	"changed_by" integer NOT NULL,
	"previous_role" "user_role_enum" NOT NULL,
	"new_role" "user_role_enum" NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
ALTER TABLE "reports" ADD COLUMN "resolved_by" integer;--> statement-breakpoint
ALTER TABLE "moderation_actions" ADD CONSTRAINT "moderation_actions_resource_id_resources_id_fk" FOREIGN KEY ("resource_id") REFERENCES "public"."resources"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "moderation_actions" ADD CONSTRAINT "moderation_actions_actor_id_users_id_fk" FOREIGN KEY ("actor_id") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "role_changes" ADD CONSTRAINT "role_changes_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "role_changes" ADD CONSTRAINT "role_changes_changed_by_users_id_fk" FOREIGN KEY ("changed_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "idx_moderation_actions_resource_id" ON "moderation_actions" USING btree ("resource_id");--> statement-breakpoint
CREATE INDEX "idx_role_changes_user_id" ON "role_changes" USING btree ("user_id");--> statement-breakpoint
ALTER TABLE "reports" ADD CONSTRAINT "reports_resolved_by_users_id_fk" FOREIGN KEY ("resolved_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;