ALTER TABLE "departments" RENAME TO "programs";--> statement-breakpoint
ALTER TABLE "programs" DROP CONSTRAINT "departments_code_unique";--> statement-breakpoint
ALTER TABLE "profiles" DROP CONSTRAINT "profiles_program_id_departments_id_fk";
--> statement-breakpoint
ALTER TABLE "subject_offerings" DROP CONSTRAINT "subject_offerings_program_id_departments_id_fk";
--> statement-breakpoint
ALTER TABLE "subjects" DROP CONSTRAINT "subjects_program_id_departments_id_fk";
--> statement-breakpoint
ALTER TABLE "profiles" ADD CONSTRAINT "profiles_program_id_programs_id_fk" FOREIGN KEY ("program_id") REFERENCES "public"."programs"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "subject_offerings" ADD CONSTRAINT "subject_offerings_program_id_programs_id_fk" FOREIGN KEY ("program_id") REFERENCES "public"."programs"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "subjects" ADD CONSTRAINT "subjects_program_id_programs_id_fk" FOREIGN KEY ("program_id") REFERENCES "public"."programs"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "programs" ADD CONSTRAINT "programs_code_unique" UNIQUE("code");