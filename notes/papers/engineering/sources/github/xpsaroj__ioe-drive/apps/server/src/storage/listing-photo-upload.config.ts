import { FileTypeValidator, MaxFileSizeValidator, ParseFilePipe } from "@nestjs/common";
import type { MulterModuleOptions } from "@nestjs/platform-express";
import { memoryStorage } from "multer";

export const LISTING_PHOTO_FIELD = "listingPhoto";
export const MAX_LISTING_PHOTOS = 6;

const MAX_PHOTO_SIZE_BYTES = 10 * 1024 * 1024; // 10 MB

const ALLOWED_PHOTO_MIME_TYPES = /^(image\/jpeg|image\/png|image\/webp)$/;

// In-memory storage - photos stream straight to Azure Blob Storage, never written to disk.
export const listingPhotoMulterOptions: MulterModuleOptions = {
  storage: memoryStorage(),
  limits: {
    fileSize: MAX_PHOTO_SIZE_BYTES,
  },
};

// Only validates size/type of whatever was provided - "at least one photo" is enforced explicitly
// in the service, since ParseFilePipe's fileIsRequired doesn't reliably guard array length for @UploadedFiles.
export const createListingPhotoValidationPipe = (): ParseFilePipe =>
  new ParseFilePipe({
    fileIsRequired: false,
    validators: [
      new MaxFileSizeValidator({ maxSize: MAX_PHOTO_SIZE_BYTES }),
      new FileTypeValidator({ fileType: ALLOWED_PHOTO_MIME_TYPES }),
    ],
  });
