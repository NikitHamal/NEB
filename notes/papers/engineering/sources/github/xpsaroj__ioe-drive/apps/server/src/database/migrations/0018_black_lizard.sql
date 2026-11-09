ALTER TYPE "public"."marketplace_listing_status_enum" ADD VALUE 'PENDING' BEFORE 'ACTIVE';--> statement-breakpoint
ALTER TYPE "public"."marketplace_listing_status_enum" ADD VALUE 'REJECTED' BEFORE 'REMOVED';--> statement-breakpoint
ALTER TYPE "public"."notification_type_enum" ADD VALUE 'LISTING_APPROVED' BEFORE 'LISTING_REMOVED';--> statement-breakpoint
ALTER TYPE "public"."notification_type_enum" ADD VALUE 'LISTING_REJECTED' BEFORE 'LISTING_REMOVED';--> statement-breakpoint
CREATE TABLE "marketplace_moderation_actions" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "marketplace_moderation_actions_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"listing_id" integer NOT NULL,
	"actor_id" integer,
	"action" "moderation_action_enum" NOT NULL,
	"reason" "marketplace_report_reason_enum",
	"note" text,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
ALTER TABLE "marketplace_moderation_actions" ADD CONSTRAINT "marketplace_moderation_actions_listing_id_marketplace_listings_id_fk" FOREIGN KEY ("listing_id") REFERENCES "public"."marketplace_listings"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "marketplace_moderation_actions" ADD CONSTRAINT "marketplace_moderation_actions_actor_id_users_id_fk" FOREIGN KEY ("actor_id") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "idx_marketplace_moderation_actions_listing_id" ON "marketplace_moderation_actions" USING btree ("listing_id");