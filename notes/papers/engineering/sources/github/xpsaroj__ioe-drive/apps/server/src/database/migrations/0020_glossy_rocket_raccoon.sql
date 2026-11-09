ALTER TYPE "public"."moderation_reason_enum" ADD VALUE 'MISLEADING_OR_BROKEN_LINK' BEFORE 'OTHER';--> statement-breakpoint
CREATE TABLE "resource_links" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "resource_links_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"resource_id" integer NOT NULL,
	"url" text NOT NULL,
	"label" varchar(100) NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "unique_resource_link" UNIQUE("resource_id","url")
);
--> statement-breakpoint
ALTER TABLE "resource_links" ADD CONSTRAINT "resource_links_resource_id_resources_id_fk" FOREIGN KEY ("resource_id") REFERENCES "public"."resources"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "idx_resource_links_resource_id" ON "resource_links" USING btree ("resource_id");