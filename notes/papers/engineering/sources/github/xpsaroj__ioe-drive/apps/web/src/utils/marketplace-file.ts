// Mirrors apps/server/src/storage/listing-photo-upload.config.ts - kept in sync manually, the two apps don't share a package.
// Deliberately a separate allowlist from utils/file.ts - listing photos are images-only with their own caps, distinct from resource uploads.
export const MAX_LISTING_PHOTO_SIZE_BYTES = 10 * 1024 * 1024;
export const MAX_LISTING_PHOTOS = 6;
export const ALLOWED_LISTING_PHOTO_MIME_TYPES = new Set(["image/jpeg", "image/png", "image/webp"]);
export const ACCEPTED_LISTING_PHOTO_EXTENSIONS = ".jpg,.jpeg,.png,.webp";

// Splits candidates into ones passing the same rules the backend enforces, and human-readable reasons for the rest.
export const partitionUploadablePhotos = (
    incoming: File[],
    alreadyQueued: number,
) => {
    const accepted: File[] = [];
    const rejected: string[] = [];
    let remaining = MAX_LISTING_PHOTOS - alreadyQueued;

    for (const file of incoming) {
        if (remaining <= 0) {
            rejected.push(`${file.name} (max ${MAX_LISTING_PHOTOS} photos)`);
            continue;
        }
        if (!ALLOWED_LISTING_PHOTO_MIME_TYPES.has(file.type)) {
            rejected.push(`${file.name} (unsupported file type)`);
            continue;
        }
        if (file.size > MAX_LISTING_PHOTO_SIZE_BYTES) {
            rejected.push(`${file.name} (over 10 MB)`);
            continue;
        }
        accepted.push(file);
        remaining -= 1;
    }

    return { accepted, rejected };
};
