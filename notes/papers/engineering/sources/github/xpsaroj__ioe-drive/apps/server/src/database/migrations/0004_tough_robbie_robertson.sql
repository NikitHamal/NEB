CREATE TYPE "public"."year_enum" AS ENUM('1', '2', '3', '4', '5');--> statement-breakpoint
ALTER TYPE "public"."semester_enum" ADD VALUE '9';--> statement-breakpoint
ALTER TYPE "public"."semester_enum" ADD VALUE '10';--> statement-breakpoint
ALTER TABLE "profiles" RENAME COLUMN "department_id" TO "program_id";--> statement-breakpoint
ALTER TABLE "subject_offerings" RENAME COLUMN "department_id" TO "program_id";--> statement-breakpoint
ALTER TABLE "subjects" RENAME COLUMN "department_id" TO "program_id";--> statement-breakpoint
ALTER TABLE "subject_offerings" DROP CONSTRAINT "unique_subject_offering";--> statement-breakpoint
ALTER TABLE "profiles" DROP CONSTRAINT "profiles_department_id_departments_id_fk";
--> statement-breakpoint
ALTER TABLE "subject_offerings" DROP CONSTRAINT "subject_offerings_department_id_departments_id_fk";
--> statement-breakpoint
ALTER TABLE "subjects" DROP CONSTRAINT "subjects_department_id_departments_id_fk";
--> statement-breakpoint
DROP INDEX "idx_subject_offerings_semester_department";--> statement-breakpoint
DROP INDEX "idx_subject_offerings_department";--> statement-breakpoint
ALTER TABLE "departments" ALTER COLUMN "id" DROP IDENTITY;--> statement-breakpoint
ALTER TABLE "subject_offerings" ALTER COLUMN "year" SET DATA TYPE "public"."year_enum" USING "year"::"text"::"public"."year_enum";--> statement-breakpoint
ALTER TABLE "departments" ADD COLUMN "total_years" integer DEFAULT 4 NOT NULL;--> statement-breakpoint
ALTER TABLE "departments" ADD COLUMN "syllabus_url" varchar(255);--> statement-breakpoint
ALTER TABLE "profiles" ADD CONSTRAINT "profiles_program_id_departments_id_fk" FOREIGN KEY ("program_id") REFERENCES "public"."departments"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "subject_offerings" ADD CONSTRAINT "subject_offerings_program_id_departments_id_fk" FOREIGN KEY ("program_id") REFERENCES "public"."departments"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "subjects" ADD CONSTRAINT "subjects_program_id_departments_id_fk" FOREIGN KEY ("program_id") REFERENCES "public"."departments"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "idx_subject_offerings_semester_program" ON "subject_offerings" USING btree ("semester","program_id");--> statement-breakpoint
CREATE INDEX "idx_subject_offerings_program" ON "subject_offerings" USING btree ("program_id");--> statement-breakpoint
ALTER TABLE "subject_offerings" ADD CONSTRAINT "unique_subject_offering" UNIQUE("subject_id","semester","program_id","year");