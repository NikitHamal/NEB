CREATE TYPE "public"."subject_hardness_level_enum" AS ENUM('EASY', 'MEDIUM', 'HARD', 'VERY_HARD');--> statement-breakpoint
CREATE TABLE "subject_marks" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "subject_marks_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"subject_id" integer NOT NULL,
	"theory_assessment" integer DEFAULT 0 NOT NULL,
	"theory_final" integer DEFAULT 0 NOT NULL,
	"practical_assessment" integer DEFAULT 0 NOT NULL,
	"practical_final" integer DEFAULT 0 NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "unique_subject_marks" UNIQUE("subject_id")
);
--> statement-breakpoint
ALTER TABLE "subjects" ADD COLUMN "hardness_level" "subject_hardness_level_enum" NOT NULL;--> statement-breakpoint
ALTER TABLE "subjects" ADD COLUMN "description" text;--> statement-breakpoint
ALTER TABLE "subject_marks" ADD CONSTRAINT "subject_marks_subject_id_subjects_id_fk" FOREIGN KEY ("subject_id") REFERENCES "public"."subjects"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "idx_subject_marks_subject_id" ON "subject_marks" USING btree ("subject_id");