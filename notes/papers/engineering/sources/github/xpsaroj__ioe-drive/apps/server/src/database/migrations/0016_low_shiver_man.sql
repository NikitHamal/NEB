CREATE TYPE "public"."marketplace_category_enum" AS ENUM('TEXTBOOKS_AND_NOTES', 'DRAFTING_AND_STATIONERY', 'CALCULATORS_AND_ELECTRONICS', 'LAB_AND_WORKSHOP_EQUIPMENT', 'FURNITURE_AND_HOSTEL_ITEMS', 'OTHER');--> statement-breakpoint
CREATE TYPE "public"."marketplace_listing_status_enum" AS ENUM('ACTIVE', 'FULFILLED', 'REMOVED');--> statement-breakpoint
CREATE TYPE "public"."marketplace_listing_type_enum" AS ENUM('SELLING', 'WANTED');--> statement-breakpoint
CREATE TYPE "public"."marketplace_report_reason_enum" AS ENUM('SCAM_OR_FRAUD', 'PROHIBITED_ITEM', 'INAPPROPRIATE_CONTENT', 'SPAM_OR_MISLEADING', 'ALREADY_SOLD_OR_UNAVAILABLE', 'OTHER');--> statement-breakpoint
CREATE TABLE "marketplace_conversations" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "marketplace_conversations_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"listing_id" integer NOT NULL,
	"poster_id" integer NOT NULL,
	"initiator_id" integer NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "unique_marketplace_conversation_per_listing_initiator" UNIQUE("listing_id","initiator_id")
);
--> statement-breakpoint
CREATE TABLE "marketplace_listing_photos" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "marketplace_listing_photos_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"listing_id" integer NOT NULL,
	"photo_url" text NOT NULL,
	"file_size" integer NOT NULL,
	"original_file_name" text NOT NULL,
	"blob_name" text NOT NULL,
	"mime_type" varchar(100) NOT NULL,
	"sort_order" integer DEFAULT 0 NOT NULL,
	"uploaded_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "marketplace_listings" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "marketplace_listings_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"title" text NOT NULL,
	"description" text NOT NULL,
	"type" "marketplace_listing_type_enum" NOT NULL,
	"category" "marketplace_category_enum" NOT NULL,
	"price" integer,
	"offering_id" integer,
	"posted_by" integer,
	"status" "marketplace_listing_status_enum" NOT NULL,
	"moderated_by" integer,
	"moderation_reason" "marketplace_report_reason_enum",
	"moderation_note" text,
	"moderated_at" timestamp,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "marketplace_messages" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "marketplace_messages_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"conversation_id" integer NOT NULL,
	"sender_id" integer,
	"body" text NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"read_at" timestamp
);
--> statement-breakpoint
CREATE TABLE "marketplace_reports" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "marketplace_reports_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"listing_id" integer NOT NULL,
	"reported_by" integer NOT NULL,
	"reason" "marketplace_report_reason_enum" NOT NULL,
	"note" text,
	"status" "report_status_enum" DEFAULT 'OPEN' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"resolved_at" timestamp,
	"resolved_by" integer,
	CONSTRAINT "unique_marketplace_report_per_user_listing" UNIQUE("listing_id","reported_by")
);
--> statement-breakpoint
ALTER TABLE "marketplace_conversations" ADD CONSTRAINT "marketplace_conversations_listing_id_marketplace_listings_id_fk" FOREIGN KEY ("listing_id") REFERENCES "public"."marketplace_listings"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "marketplace_conversations" ADD CONSTRAINT "marketplace_conversations_poster_id_users_id_fk" FOREIGN KEY ("poster_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "marketplace_conversations" ADD CONSTRAINT "marketplace_conversations_initiator_id_users_id_fk" FOREIGN KEY ("initiator_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "marketplace_listing_photos" ADD CONSTRAINT "marketplace_listing_photos_listing_id_marketplace_listings_id_fk" FOREIGN KEY ("listing_id") REFERENCES "public"."marketplace_listings"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "marketplace_listings" ADD CONSTRAINT "marketplace_listings_offering_id_subject_offerings_id_fk" FOREIGN KEY ("offering_id") REFERENCES "public"."subject_offerings"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "marketplace_listings" ADD CONSTRAINT "marketplace_listings_posted_by_users_id_fk" FOREIGN KEY ("posted_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "marketplace_listings" ADD CONSTRAINT "marketplace_listings_moderated_by_users_id_fk" FOREIGN KEY ("moderated_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "marketplace_messages" ADD CONSTRAINT "marketplace_messages_conversation_id_marketplace_conversations_id_fk" FOREIGN KEY ("conversation_id") REFERENCES "public"."marketplace_conversations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "marketplace_messages" ADD CONSTRAINT "marketplace_messages_sender_id_users_id_fk" FOREIGN KEY ("sender_id") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "marketplace_reports" ADD CONSTRAINT "marketplace_reports_listing_id_marketplace_listings_id_fk" FOREIGN KEY ("listing_id") REFERENCES "public"."marketplace_listings"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "marketplace_reports" ADD CONSTRAINT "marketplace_reports_reported_by_users_id_fk" FOREIGN KEY ("reported_by") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "marketplace_reports" ADD CONSTRAINT "marketplace_reports_resolved_by_users_id_fk" FOREIGN KEY ("resolved_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "idx_marketplace_conversations_listing_id" ON "marketplace_conversations" USING btree ("listing_id");--> statement-breakpoint
CREATE INDEX "idx_marketplace_conversations_poster_id" ON "marketplace_conversations" USING btree ("poster_id");--> statement-breakpoint
CREATE INDEX "idx_marketplace_conversations_initiator_id" ON "marketplace_conversations" USING btree ("initiator_id");--> statement-breakpoint
CREATE INDEX "idx_marketplace_listing_photos_listing_id" ON "marketplace_listing_photos" USING btree ("listing_id");--> statement-breakpoint
CREATE INDEX "idx_marketplace_listings_posted_by" ON "marketplace_listings" USING btree ("posted_by");--> statement-breakpoint
CREATE INDEX "idx_marketplace_listings_status" ON "marketplace_listings" USING btree ("status");--> statement-breakpoint
CREATE INDEX "idx_marketplace_listings_type" ON "marketplace_listings" USING btree ("type");--> statement-breakpoint
CREATE INDEX "idx_marketplace_listings_category" ON "marketplace_listings" USING btree ("category");--> statement-breakpoint
CREATE INDEX "idx_marketplace_listings_offering_id" ON "marketplace_listings" USING btree ("offering_id");--> statement-breakpoint
CREATE INDEX "idx_marketplace_messages_conversation_id_created_at" ON "marketplace_messages" USING btree ("conversation_id","created_at");--> statement-breakpoint
CREATE INDEX "idx_marketplace_reports_listing_id" ON "marketplace_reports" USING btree ("listing_id");--> statement-breakpoint
CREATE INDEX "idx_marketplace_reports_status" ON "marketplace_reports" USING btree ("status");