import { apiClient } from "./api-client";
import { appendPaginationParams, type PaginationParams } from "./pagination";
import type { MarketplaceListing } from "@/types/entities";
import type { ApiResponse, EmptyApiResponse, PaginatedApiResponse, ListingSummary, ListingSuggestion } from "@/types/api";
import type { MarketplaceReportReasonInput, UpdateListingInput } from "../validators/marketplace";

const MARKETPLACE_API_BASE_URL = "/marketplace/listings";

export interface GetListingsFilters extends PaginationParams {
    type?: string;
    category?: string;
    offeringId?: number;
    userId?: number;
    minPrice?: number;
    maxPrice?: number;
    q?: string;
}

export const marketplaceApi = {
    async createListing(formData: FormData): Promise<ApiResponse<MarketplaceListing>> {
        return apiClient.postForm<ApiResponse<MarketplaceListing>>(`${MARKETPLACE_API_BASE_URL}`, formData);
    },

    async updateListing(listingId: number, data: UpdateListingInput): Promise<ApiResponse<MarketplaceListing>> {
        return apiClient.patch<ApiResponse<MarketplaceListing>>(`${MARKETPLACE_API_BASE_URL}/${listingId}`, data);
    },

    async deleteListing(listingId: number): Promise<EmptyApiResponse> {
        return apiClient.delete<EmptyApiResponse>(`${MARKETPLACE_API_BASE_URL}/${listingId}`);
    },

    async markFulfilled(listingId: number): Promise<ApiResponse<MarketplaceListing>> {
        return apiClient.post<ApiResponse<MarketplaceListing>>(`${MARKETPLACE_API_BASE_URL}/${listingId}/mark-fulfilled`);
    },

    async reactivateListing(listingId: number): Promise<ApiResponse<MarketplaceListing>> {
        return apiClient.post<ApiResponse<MarketplaceListing>>(`${MARKETPLACE_API_BASE_URL}/${listingId}/reactivate`);
    },

    async addListingPhotos(listingId: number, formData: FormData): Promise<EmptyApiResponse> {
        return apiClient.postForm<EmptyApiResponse>(`${MARKETPLACE_API_BASE_URL}/${listingId}/photos`, formData);
    },

    async removeListingPhoto(listingId: number, photoId: number): Promise<EmptyApiResponse> {
        return apiClient.delete<EmptyApiResponse>(`${MARKETPLACE_API_BASE_URL}/${listingId}/photos/${photoId}`);
    },

    async approveListing(listingId: number): Promise<ApiResponse<MarketplaceListing>> {
        return apiClient.post<ApiResponse<MarketplaceListing>>(`${MARKETPLACE_API_BASE_URL}/${listingId}/approve`);
    },

    async rejectListing(listingId: number, data: MarketplaceReportReasonInput): Promise<ApiResponse<MarketplaceListing>> {
        return apiClient.post<ApiResponse<MarketplaceListing>>(`${MARKETPLACE_API_BASE_URL}/${listingId}/reject`, data);
    },

    async reportListing(listingId: number, data: MarketplaceReportReasonInput): Promise<EmptyApiResponse> {
        return apiClient.post<EmptyApiResponse>(`${MARKETPLACE_API_BASE_URL}/${listingId}/report`, data);
    },

    async removeListingAsModerator(listingId: number, data: MarketplaceReportReasonInput): Promise<ApiResponse<MarketplaceListing>> {
        return apiClient.post<ApiResponse<MarketplaceListing>>(`${MARKETPLACE_API_BASE_URL}/${listingId}/remove`, data);
    },

    async getListingById(listingId: number): Promise<ApiResponse<ListingSummary>> {
        return apiClient.get<ApiResponse<ListingSummary>>(`${MARKETPLACE_API_BASE_URL}/${listingId}`);
    },

    async getListings(filters?: GetListingsFilters): Promise<PaginatedApiResponse<ListingSummary>> {
        const params = new URLSearchParams();
        if (filters?.type) params.set("type", filters.type);
        if (filters?.category) params.set("category", filters.category);
        if (filters?.offeringId) params.set("offeringId", String(filters.offeringId));
        if (filters?.userId) params.set("userId", String(filters.userId));
        if (filters?.minPrice !== undefined) params.set("minPrice", String(filters.minPrice));
        if (filters?.maxPrice !== undefined) params.set("maxPrice", String(filters.maxPrice));
        if (filters?.q) params.set("q", filters.q);
        appendPaginationParams(params, filters);

        const query = params.toString();
        return apiClient.get<PaginatedApiResponse<ListingSummary>>(`${MARKETPLACE_API_BASE_URL}${query ? `?${query}` : ""}`);
    },

    async getMyListings(pagination?: PaginationParams): Promise<PaginatedApiResponse<ListingSummary>> {
        const params = new URLSearchParams();
        appendPaginationParams(params, pagination);
        return apiClient.get<PaginatedApiResponse<ListingSummary>>(`/me/marketplace/listings?${params.toString()}`);
    },

    async searchSuggestions(q: string, limit?: number): Promise<ApiResponse<ListingSuggestion[]>> {
        const params = new URLSearchParams({ q });
        if (limit) params.set("limit", String(limit));
        return apiClient.get<ApiResponse<ListingSuggestion[]>>(`${MARKETPLACE_API_BASE_URL}/search-suggestions?${params.toString()}`);
    },
};
