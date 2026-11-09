import { apiClient } from "./api-client";
import { appendPaginationParams, type PaginationParams } from "./pagination";
import type { UserProfile, Profile } from "@/types/entities";
import type { ApiResponse, EmptyApiResponse, PaginatedApiResponse, ResourceSummary, RecentResourceItem, BookmarkedResourceItem, WeeklySummary } from "@/types/api";

const ME_API_BASE_URL = "/me";

export const meApi = {
    async getMyProfile(): Promise<ApiResponse<UserProfile>> {
        return apiClient.get<ApiResponse<UserProfile>>(`${ME_API_BASE_URL}`);
    },

    async updateMyProfile(profileData: Partial<Omit<Profile, "id" | "userId">>): Promise<EmptyApiResponse> {
        return apiClient.patch<EmptyApiResponse>(`${ME_API_BASE_URL}`, profileData);
    },

    async getWeeklySummary(): Promise<ApiResponse<WeeklySummary>> {
        return apiClient.get<ApiResponse<WeeklySummary>>(`${ME_API_BASE_URL}/weekly-summary`);
    },

    async getUploadedResources(pagination?: PaginationParams): Promise<PaginatedApiResponse<ResourceSummary>> {
        const params = appendPaginationParams(new URLSearchParams(), pagination).toString();
        return apiClient.get<PaginatedApiResponse<ResourceSummary>>(`${ME_API_BASE_URL}/resources${params ? `?${params}` : ""}`);
    },

    async getRecentResources(pagination?: PaginationParams): Promise<PaginatedApiResponse<RecentResourceItem>> {
        const params = appendPaginationParams(new URLSearchParams(), pagination).toString();
        return apiClient.get<PaginatedApiResponse<RecentResourceItem>>(`${ME_API_BASE_URL}/recent-resources${params ? `?${params}` : ""}`);
    },

    async getBookmarkedResources(pagination?: PaginationParams): Promise<PaginatedApiResponse<BookmarkedResourceItem>> {
        const params = appendPaginationParams(new URLSearchParams(), pagination).toString();
        return apiClient.get<PaginatedApiResponse<BookmarkedResourceItem>>(`${ME_API_BASE_URL}/bookmarked-resources${params ? `?${params}` : ""}`);
    },

    /** Every resource ID the current user has bookmarked, uncapped - for checking status across a list, not display. */
    async getBookmarkedResourceIds(): Promise<ApiResponse<number[]>> {
        return apiClient.get<ApiResponse<number[]>>(`${ME_API_BASE_URL}/bookmarked-resource-ids`);
    },

    async markResourceAsRecentlyAccessed(resourceId: string): Promise<EmptyApiResponse> {
        return apiClient.post<EmptyApiResponse>(`${ME_API_BASE_URL}/resources/${resourceId}/recent`);
    },

    async markResourceAsBookmarked(resourceId: string): Promise<EmptyApiResponse> {
        return apiClient.post<EmptyApiResponse>(`${ME_API_BASE_URL}/resources/${resourceId}/bookmark`);
    },

    async unmarkResourceAsBookmarked(resourceId: string): Promise<EmptyApiResponse> {
        return apiClient.delete<EmptyApiResponse>(`${ME_API_BASE_URL}/resources/${resourceId}/bookmark`);
    },

    /** Every resource the current user has voted on, mapped to their vote (1 or -1). */
    async getResourceVoteValues(): Promise<ApiResponse<Record<number, 1 | -1>>> {
        return apiClient.get<ApiResponse<Record<number, 1 | -1>>>(`${ME_API_BASE_URL}/resources/vote-values`);
    },

    async setResourceVote(resourceId: string, value: 1 | -1): Promise<EmptyApiResponse> {
        return apiClient.put<EmptyApiResponse>(`${ME_API_BASE_URL}/resources/${resourceId}/vote`, { value });
    },

    async clearResourceVote(resourceId: string): Promise<EmptyApiResponse> {
        return apiClient.delete<EmptyApiResponse>(`${ME_API_BASE_URL}/resources/${resourceId}/vote`);
    },
}
