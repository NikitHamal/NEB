CREATE TYPE "public"."semester_enum" AS ENUM('1', '2', '3', '4', '5', '6', '7', '8');--> statement-breakpoint
CREATE TABLE "departments" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "departments_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"code" varchar(10) NOT NULL,
	"name" varchar(255) NOT NULL,
	CONSTRAINT "departments_code_unique" UNIQUE("code")
);
--> statement-breakpoint
CREATE TABLE "note_files" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "note_files_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"note_id" integer NOT NULL,
	"file_url" text NOT NULL,
	"file_size" integer NOT NULL,
	"compressed_size" integer NOT NULL,
	"compression_method" varchar(100) NOT NULL,
	"file_type" varchar(100) NOT NULL,
	"uploaded_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "notes" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "notes_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"title" text NOT NULL,
	"description" text NOT NULL,
	"subject_id" integer NOT NULL,
	"uploaded_by" integer,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "profiles" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "profiles_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"user_id" integer NOT NULL,
	"bio" text,
	"department_id" integer,
	"semester" "semester_enum",
	"college" text,
	"profile_picture_url" text,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "profiles_user_id_unique" UNIQUE("user_id")
);
--> statement-breakpoint
CREATE TABLE "subject_offerings" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "subject_offerings_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"subject_id" integer NOT NULL,
	"semester" "semester_enum" NOT NULL,
	"department_id" integer NOT NULL,
	"year" integer NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "unique_subject_offering" UNIQUE("subject_id","semester","department_id","year")
);
--> statement-breakpoint
CREATE TABLE "subjects" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "subjects_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"code" varchar(10) NOT NULL,
	"name" varchar(255) NOT NULL,
	"department_id" integer NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "subjects_code_unique" UNIQUE("code")
);
--> statement-breakpoint
CREATE TABLE "user_archived_notes" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "user_archived_notes_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"user_id" integer NOT NULL,
	"note_id" integer NOT NULL,
	"archived_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "unique_user_archived_note" UNIQUE("user_id","note_id")
);
--> statement-breakpoint
CREATE TABLE "user_recent_notes" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "user_recent_notes_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"user_id" integer NOT NULL,
	"note_id" integer NOT NULL,
	"accessed_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "unique_user_recent_note" UNIQUE("user_id","note_id")
);
--> statement-breakpoint
CREATE TABLE "users" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "users_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"clerk_user_id" varchar(255) NOT NULL,
	"full_name" varchar(255) NOT NULL,
	"email" varchar(255),
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "users_clerk_user_id_unique" UNIQUE("clerk_user_id"),
	CONSTRAINT "users_email_unique" UNIQUE("email")
);
--> statement-breakpoint
CREATE TABLE "webhook_events" (
	"svix_id" text PRIMARY KEY NOT NULL,
	"event_type" varchar(255) NOT NULL,
	"received_at" timestamp DEFAULT now()
);
--> statement-breakpoint
ALTER TABLE "note_files" ADD CONSTRAINT "note_files_note_id_notes_id_fk" FOREIGN KEY ("note_id") REFERENCES "public"."notes"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "notes" ADD CONSTRAINT "notes_subject_id_subjects_id_fk" FOREIGN KEY ("subject_id") REFERENCES "public"."subjects"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "notes" ADD CONSTRAINT "notes_uploaded_by_users_id_fk" FOREIGN KEY ("uploaded_by") REFERENCES "public"."users"("id") ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "profiles" ADD CONSTRAINT "profiles_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "profiles" ADD CONSTRAINT "profiles_department_id_departments_id_fk" FOREIGN KEY ("department_id") REFERENCES "public"."departments"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "subject_offerings" ADD CONSTRAINT "subject_offerings_subject_id_subjects_id_fk" FOREIGN KEY ("subject_id") REFERENCES "public"."subjects"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "subject_offerings" ADD CONSTRAINT "subject_offerings_department_id_departments_id_fk" FOREIGN KEY ("department_id") REFERENCES "public"."departments"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "subjects" ADD CONSTRAINT "subjects_department_id_departments_id_fk" FOREIGN KEY ("department_id") REFERENCES "public"."departments"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_archived_notes" ADD CONSTRAINT "user_archived_notes_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_archived_notes" ADD CONSTRAINT "user_archived_notes_note_id_notes_id_fk" FOREIGN KEY ("note_id") REFERENCES "public"."notes"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_recent_notes" ADD CONSTRAINT "user_recent_notes_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "user_recent_notes" ADD CONSTRAINT "user_recent_notes_note_id_notes_id_fk" FOREIGN KEY ("note_id") REFERENCES "public"."notes"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "idx_note_files_note_id" ON "note_files" USING btree ("note_id");--> statement-breakpoint
CREATE INDEX "idx_notes_subject_id" ON "notes" USING btree ("subject_id");--> statement-breakpoint
CREATE INDEX "idx_notes_uploaded_by" ON "notes" USING btree ("uploaded_by");--> statement-breakpoint
CREATE INDEX "idx_subject_offerings_semester_department" ON "subject_offerings" USING btree ("semester","department_id");--> statement-breakpoint
CREATE INDEX "idx_subject_offerings_department" ON "subject_offerings" USING btree ("department_id");--> statement-breakpoint
CREATE INDEX "idx_subject_offerings_subject" ON "subject_offerings" USING btree ("subject_id");--> statement-breakpoint
CREATE INDEX "idx_user_archived_notes_user_id" ON "user_archived_notes" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "idx_user_recent_notes_user_id" ON "user_recent_notes" USING btree ("user_id");