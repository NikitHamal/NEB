import { UploaderSummary } from "./user.responses";
import { SubjectSummary, SubjectOfferingSummary } from "./academics.responses";
import { MarketplaceCategory, MarketplaceListingStatus, MarketplaceListingType, MarketplaceReportReason } from "../entities";

export interface ListingPhotoSummary {
    id: number;
    listingId: number;
    photoUrl: string;
    fileSize: number;
    originalFileName: string;
    mimeType: string;
    sortOrder: number;
}

export interface ListingSummary {
    id: number;
    title: string;
    description: string;
    type: MarketplaceListingType;
    category: MarketplaceCategory;
    price: number | null;
    createdAt: string;
    updatedAt: string;

    offeringId?: number;
    postedBy?: number;
    status: MarketplaceListingStatus;
    moderatedBy?: number;
    moderationReason?: MarketplaceReportReason;
    moderationNote?: string;
    moderatedAt?: string;

    subjectOffering?: SubjectOfferingSummary & {
        subject: SubjectSummary;
    };

    poster?: UploaderSummary;
    photos: ListingPhotoSummary[];
}

// Lean listing preview row - no description, poster, or subject, unlike ListingSummary.
export interface ListingSuggestion {
    id: number;
    title: string;
    price: number | null;
    category: MarketplaceCategory;
    photoUrl?: string;
}

export interface ListingReportPreview {
    id: number;
    title: string;
    type: MarketplaceListingType;
    category: MarketplaceCategory;
}

// Reporter's identity is only ever exposed here, never on any poster- or public-facing response.
export interface ListingReportItem {
    id: number;
    listingId: number;
    reportedBy: number;
    reason: MarketplaceReportReason;
    note: string | null;
    status: "OPEN" | "RESOLVED";
    createdAt: string;
    resolvedAt: string | null;
    listing: ListingReportPreview;
    reporter: { id: number; fullName: string };
}
