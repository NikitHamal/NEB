import { UploaderSummary } from "./user.responses";
import { SubjectSummary, SubjectOfferingSummary } from "./academics.responses";
import { ModerationReason, ResourceStatus, ResourceType } from "../entities";

export interface ResourceFileSummary {
    id: number;
    resourceId: number;
    fileUrl: string;
    fileSize: number;
    originalFileName: string;
    mimeType: string;
}

export interface ResourceLinkSummary {
    id: number;
    resourceId: number;
    url: string;
    label: string;
}

export interface ResourceSummary {
    id: number;
    title: string;
    description: string;
    type: ResourceType;
    createdAt: string;
    updatedAt: string;

    offeringId: number;
    uploadedBy?: number;
    status: ResourceStatus;
    moderatedBy?: number;
    moderationReason?: ModerationReason;
    moderationNote?: string;
    moderatedAt?: string;

    upvoteCount: number;
    downvoteCount: number;
    downloadCount: number;

    subjectOffering: SubjectOfferingSummary & {
        subject: SubjectSummary;
    }

    uploader?: UploaderSummary;
    files: ResourceFileSummary[];
    links: ResourceLinkSummary[];
}

// Lean resource preview row - no description, uploader, or files, unlike ResourceSummary.
export interface ResourceSuggestion {
    id: number;
    title: string;
    type: ResourceType;
    subjectCode: string;
}

export interface RecentResourceItem {
    id: number;
    userId: number;
    resourceId: number;
    accessedAt: string;

    resource: ResourceSummary;
}

export interface BookmarkedResourceItem {
    id: number;
    userId: number;
    resourceId: number;
    bookmarkedAt: string;

    resource: ResourceSummary;
}

// Counts over the last 7 days.
export interface WeeklySummary {
    resourcesShared: number;
    resourcesViewed: number;
    resourcesBookmarked: number;
}
