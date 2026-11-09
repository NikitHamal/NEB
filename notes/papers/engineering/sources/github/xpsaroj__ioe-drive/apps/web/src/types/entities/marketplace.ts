export enum MarketplaceListingType {
    SELLING = "SELLING",
    WANTED = "WANTED",
}

export const MarketplaceListingTypeLabel: Record<MarketplaceListingType, string> = {
    [MarketplaceListingType.SELLING]: "Selling",
    [MarketplaceListingType.WANTED]: "Wanted",
};

export enum MarketplaceCategory {
    TEXTBOOKS_AND_NOTES = "TEXTBOOKS_AND_NOTES",
    DRAFTING_AND_STATIONERY = "DRAFTING_AND_STATIONERY",
    CALCULATORS_AND_ELECTRONICS = "CALCULATORS_AND_ELECTRONICS",
    LAB_AND_WORKSHOP_EQUIPMENT = "LAB_AND_WORKSHOP_EQUIPMENT",
    FURNITURE_AND_HOSTEL_ITEMS = "FURNITURE_AND_HOSTEL_ITEMS",
    OTHER = "OTHER",
}

export const MarketplaceCategoryLabel: Record<MarketplaceCategory, string> = {
    [MarketplaceCategory.TEXTBOOKS_AND_NOTES]: "Textbooks & Notes",
    [MarketplaceCategory.DRAFTING_AND_STATIONERY]: "Drafting & Stationery",
    [MarketplaceCategory.CALCULATORS_AND_ELECTRONICS]: "Calculators & Electronics",
    [MarketplaceCategory.LAB_AND_WORKSHOP_EQUIPMENT]: "Lab & Workshop Equipment",
    [MarketplaceCategory.FURNITURE_AND_HOSTEL_ITEMS]: "Furniture & Hostel Items",
    [MarketplaceCategory.OTHER]: "Other",
};

// PENDING: awaiting moderator review, invisible except to poster/moderators. ACTIVE: live.
// FULFILLED: owner marked sold/found, hidden from default browse, reversible. REJECTED: moderator
// sent it back with a reason, resubmittable (edit -> back to PENDING). REMOVED: moderator took it
// down, terminal.
export enum MarketplaceListingStatus {
    PENDING = "PENDING",
    ACTIVE = "ACTIVE",
    FULFILLED = "FULFILLED",
    REJECTED = "REJECTED",
    REMOVED = "REMOVED",
}

export const MarketplaceListingStatusLabel: Record<MarketplaceListingStatus, string> = {
    [MarketplaceListingStatus.PENDING]: "Pending Review",
    [MarketplaceListingStatus.ACTIVE]: "Active",
    [MarketplaceListingStatus.FULFILLED]: "Fulfilled",
    [MarketplaceListingStatus.REJECTED]: "Rejected",
    [MarketplaceListingStatus.REMOVED]: "Removed",
};

export enum MarketplaceReportReason {
    SCAM_OR_FRAUD = "SCAM_OR_FRAUD",
    PROHIBITED_ITEM = "PROHIBITED_ITEM",
    INAPPROPRIATE_CONTENT = "INAPPROPRIATE_CONTENT",
    SPAM_OR_MISLEADING = "SPAM_OR_MISLEADING",
    ALREADY_SOLD_OR_UNAVAILABLE = "ALREADY_SOLD_OR_UNAVAILABLE",
    OTHER = "OTHER",
}

export const MarketplaceReportReasonLabel: Record<MarketplaceReportReason, string> = {
    [MarketplaceReportReason.SCAM_OR_FRAUD]: "Scam or fraud",
    [MarketplaceReportReason.PROHIBITED_ITEM]: "Prohibited item",
    [MarketplaceReportReason.INAPPROPRIATE_CONTENT]: "Inappropriate content",
    [MarketplaceReportReason.SPAM_OR_MISLEADING]: "Spam or misleading",
    [MarketplaceReportReason.ALREADY_SOLD_OR_UNAVAILABLE]: "Already sold / unavailable",
    [MarketplaceReportReason.OTHER]: "Other",
};

export interface MarketplaceListing {
    id: number;
    title: string;
    description: string;
    type: MarketplaceListingType;
    category: MarketplaceCategory;
    price: number | null;
    offeringId?: number;
    postedBy?: number;
    status: MarketplaceListingStatus;
    moderatedBy?: number;
    moderationReason?: MarketplaceReportReason;
    moderationNote?: string;
    moderatedAt?: string;
    createdAt: string;
    updatedAt: string;
}

export interface MarketplaceListingPhoto {
    id: number;
    listingId: number;
    photoUrl: string;
    fileSize: number;
    originalFileName: string;
    mimeType: string;
    sortOrder: number;
    uploadedAt: string;
}
