ALTER TABLE "note_files" RENAME COLUMN "file_type" TO "mime_type";--> statement-breakpoint
ALTER TABLE "note_files" ALTER COLUMN "compressed_size" DROP NOT NULL;--> statement-breakpoint
ALTER TABLE "note_files" ALTER COLUMN "compression_method" DROP NOT NULL;--> statement-breakpoint
ALTER TABLE "note_files" ADD COLUMN "original_file_name" text NOT NULL;--> statement-breakpoint
ALTER TABLE "note_files" ADD COLUMN "blob_name" text NOT NULL;