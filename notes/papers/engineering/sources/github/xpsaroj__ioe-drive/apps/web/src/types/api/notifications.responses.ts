export type NotificationType =
    | "RESOURCE_APPROVED"
    | "RESOURCE_REJECTED"
    | "RESOURCE_REMOVED"
    | "LISTING_APPROVED"
    | "LISTING_REJECTED"
    | "LISTING_REMOVED";

export interface NotificationSummary {
    id: number;
    type: NotificationType;
    message: string;
    link: string | null;
    isRead: boolean;
    createdAt: string;
}
