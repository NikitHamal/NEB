import { apiClient } from "./api-client";
import { appendPaginationParams, type PaginationParams } from "./pagination";
import type { ApiResponse, EmptyApiResponse, PaginatedApiResponse, NotificationSummary } from "@/types/api";

const NOTIFICATIONS_API_BASE_URL = "/notifications";

export const notificationsApi = {
    async getNotifications(pagination?: PaginationParams): Promise<PaginatedApiResponse<NotificationSummary>> {
        const params = new URLSearchParams();
        appendPaginationParams(params, pagination);
        return apiClient.get<PaginatedApiResponse<NotificationSummary>>(
            `${NOTIFICATIONS_API_BASE_URL}?${params.toString()}`
        );
    },

    async getUnreadCount(): Promise<ApiResponse<{ unreadCount: number }>> {
        return apiClient.get<ApiResponse<{ unreadCount: number }>>(`${NOTIFICATIONS_API_BASE_URL}/unread-count`);
    },

    async markRead(notificationId: number): Promise<EmptyApiResponse> {
        return apiClient.patch<EmptyApiResponse>(`${NOTIFICATIONS_API_BASE_URL}/${notificationId}/read`);
    },

    async markAllRead(): Promise<EmptyApiResponse> {
        return apiClient.patch<EmptyApiResponse>(`${NOTIFICATIONS_API_BASE_URL}/read-all`);
    },
};
