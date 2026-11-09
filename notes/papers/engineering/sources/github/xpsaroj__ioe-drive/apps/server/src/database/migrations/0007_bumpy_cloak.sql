ALTER TABLE "subject_offerings" ADD COLUMN "is_elective" boolean DEFAULT false NOT NULL;--> statement-breakpoint
ALTER TABLE "subjects" ADD COLUMN "syllabus_url" varchar(255);