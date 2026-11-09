import type { User } from "./user";
import type { Subject, SubjectOffering } from "./academics";

export enum ResourceType {
    NOTE = "NOTE",
    PAST_QUESTION = "PAST_QUESTION",
    ASSESSMENT = "ASSESSMENT",
    LAB_SHEET = "LAB_SHEET",
    BOOK = "BOOK",
    OTHER = "OTHER",
}

export const ResourceTypeLabel: Record<ResourceType, string> = {
    [ResourceType.NOTE]: "Note",
    [ResourceType.PAST_QUESTION]: "Past Question",
    [ResourceType.ASSESSMENT]: "Assessment",
    [ResourceType.LAB_SHEET]: "Lab Sheet",
    [ResourceType.BOOK]: "Book",
    [ResourceType.OTHER]: "Other",
};

export enum ResourceStatus {
    PENDING = "PENDING",
    APPROVED = "APPROVED",
    REJECTED = "REJECTED",
    REMOVED = "REMOVED",
}

export const ResourceStatusLabel: Record<ResourceStatus, string> = {
    [ResourceStatus.PENDING]: "Pending Review",
    [ResourceStatus.APPROVED]: "Approved",
    [ResourceStatus.REJECTED]: "Rejected",
    [ResourceStatus.REMOVED]: "Removed",
};

export enum ModerationReason {
    INAPPROPRIATE_CONTENT = "INAPPROPRIATE_CONTENT",
    WRONG_SUBJECT = "WRONG_SUBJECT",
    SPAM_OR_LOW_QUALITY = "SPAM_OR_LOW_QUALITY",
    COPYRIGHT = "COPYRIGHT",
    MISLEADING_OR_BROKEN_LINK = "MISLEADING_OR_BROKEN_LINK",
    OTHER = "OTHER",
}

export const ModerationReasonLabel: Record<ModerationReason, string> = {
    [ModerationReason.INAPPROPRIATE_CONTENT]: "Inappropriate content",
    [ModerationReason.WRONG_SUBJECT]: "Wrong subject",
    [ModerationReason.SPAM_OR_LOW_QUALITY]: "Spam or low quality",
    [ModerationReason.COPYRIGHT]: "Copyright",
    [ModerationReason.MISLEADING_OR_BROKEN_LINK]: "Misleading or broken link",
    [ModerationReason.OTHER]: "Other",
};

export interface Resource {
    id: number;
    title: string;
    description: string;
    type: ResourceType;
    offeringId: number;
    uploadedBy?: number;
    status: ResourceStatus;
    moderatedBy?: number;
    moderationReason?: ModerationReason;
    moderationNote?: string;
    moderatedAt?: string;
    createdAt: string;
    updatedAt: string;
}

export interface ResourceFile {
    id: number;
    resourceId: number;
    originalFileName: string;
    blobName: string;
    mimeType: string;
    fileUrl: string;
    fileSize: number;
    compressedSize: number | null;
    compressionMethod: string | null;
    uploadedAt: string;
}

export interface ResourceWithFiles extends Resource {
    files: ResourceFile[];
}

export interface UploadedResource extends Resource {
    subjectOffering: SubjectOffering & {
        subject: Subject;
    }

    uploader?: Omit<User, "email" | "clerkUserId">;
    files: ResourceFile[];
}

export interface RecentResource {
    id: number;
    userId: number;
    resourceId: number;
    accessedAt: string;
    resource: UploadedResource;
}

export interface BookmarkedResource {
    id: number;
    userId: number;
    resourceId: number;
    bookmarkedAt: string;
    resource: UploadedResource;
}
