ALTER TABLE "notes" RENAME COLUMN "subject_id" TO "offering_id";--> statement-breakpoint
ALTER TABLE "notes" DROP CONSTRAINT "notes_subject_id_subjects_id_fk";
--> statement-breakpoint
DROP INDEX "idx_notes_subject_id";--> statement-breakpoint
ALTER TABLE "notes" ADD CONSTRAINT "notes_offering_id_subject_offerings_id_fk" FOREIGN KEY ("offering_id") REFERENCES "public"."subject_offerings"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "idx_notes_subject_id" ON "notes" USING btree ("offering_id");