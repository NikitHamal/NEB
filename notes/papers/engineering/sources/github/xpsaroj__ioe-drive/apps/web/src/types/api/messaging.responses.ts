import { UploaderSummary } from "./user.responses";
import { ListingPhotoSummary } from "./marketplace.responses";
import { MarketplaceListingStatus } from "../entities";

export interface ConversationListingPreview {
    id: number;
    title: string;
    status: MarketplaceListingStatus;
    photos: ListingPhotoSummary[];
}

export interface MessageSummary {
    id: number;
    conversationId: number;
    senderId?: number;
    body: string;
    createdAt: string;
    readAt?: string;
}

export interface ConversationDetail {
    id: number;
    listingId: number;
    posterId?: number;
    initiatorId?: number;
    createdAt: string;
    updatedAt: string;
    listing: ConversationListingPreview;
    poster?: UploaderSummary;
    initiator?: UploaderSummary;
}

/** The inbox list's shape - ConversationDetail plus the preview fields only that endpoint computes. */
export interface ConversationSummary extends ConversationDetail {
    lastMessage: MessageSummary | null;
    unreadCount: number;
}

export interface StartConversationResult {
    conversationId: number;
    message: MessageSummary;
}
