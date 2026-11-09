import { apiClient } from "./api-client";
import { appendPaginationParams, type PaginationParams } from "./pagination";
import type {
    ApiResponse,
    EmptyApiResponse,
    PaginatedApiResponse,
    ConversationDetail,
    ConversationSummary,
    MessageSummary,
    StartConversationResult,
} from "@/types/api";

const MESSAGING_API_BASE_URL = "/messaging";

export const messagingApi = {
    async getConversation(conversationId: number): Promise<ApiResponse<ConversationDetail>> {
        return apiClient.get<ApiResponse<ConversationDetail>>(`${MESSAGING_API_BASE_URL}/conversations/${conversationId}`);
    },

    async getConversations(pagination?: PaginationParams): Promise<PaginatedApiResponse<ConversationSummary>> {
        const params = new URLSearchParams();
        appendPaginationParams(params, pagination);
        return apiClient.get<PaginatedApiResponse<ConversationSummary>>(
            `${MESSAGING_API_BASE_URL}/conversations?${params.toString()}`
        );
    },

    async getMessages(conversationId: number, pagination?: PaginationParams): Promise<PaginatedApiResponse<MessageSummary>> {
        const params = new URLSearchParams();
        appendPaginationParams(params, pagination);
        return apiClient.get<PaginatedApiResponse<MessageSummary>>(
            `${MESSAGING_API_BASE_URL}/conversations/${conversationId}/messages?${params.toString()}`
        );
    },

    async startConversation(listingId: number, message: string): Promise<ApiResponse<StartConversationResult>> {
        return apiClient.post<ApiResponse<StartConversationResult>>(`${MESSAGING_API_BASE_URL}/conversations`, {
            listingId,
            message,
        });
    },

    async markConversationRead(conversationId: number): Promise<EmptyApiResponse> {
        return apiClient.patch<EmptyApiResponse>(`${MESSAGING_API_BASE_URL}/conversations/${conversationId}/read`);
    },

    async getUnreadCount(): Promise<ApiResponse<{ unreadCount: number }>> {
        return apiClient.get<ApiResponse<{ unreadCount: number }>>(`${MESSAGING_API_BASE_URL}/unread-count`);
    },
};
