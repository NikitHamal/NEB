CREATE TABLE "resource_votes" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "resource_votes_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"resource_id" integer NOT NULL,
	"user_id" integer NOT NULL,
	"value" integer NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "unique_user_resource_vote" UNIQUE("user_id","resource_id")
);
--> statement-breakpoint
ALTER TABLE "resources" ADD COLUMN "upvote_count" integer DEFAULT 0 NOT NULL;--> statement-breakpoint
ALTER TABLE "resources" ADD COLUMN "downvote_count" integer DEFAULT 0 NOT NULL;--> statement-breakpoint
ALTER TABLE "resources" ADD COLUMN "download_count" integer DEFAULT 0 NOT NULL;--> statement-breakpoint
ALTER TABLE "resource_votes" ADD CONSTRAINT "resource_votes_resource_id_resources_id_fk" FOREIGN KEY ("resource_id") REFERENCES "public"."resources"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "resource_votes" ADD CONSTRAINT "resource_votes_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "idx_resource_votes_resource_id" ON "resource_votes" USING btree ("resource_id");--> statement-breakpoint
CREATE INDEX "idx_resource_votes_user_id" ON "resource_votes" USING btree ("user_id");