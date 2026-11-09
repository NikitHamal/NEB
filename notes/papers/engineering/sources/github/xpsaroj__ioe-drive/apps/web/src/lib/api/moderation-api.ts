import { apiClient } from "./api-client";
import { appendPaginationParams, type PaginationParams } from "./pagination";
import type { EmptyApiResponse, PaginatedApiResponse, ListingSummary, ListingReportItem, ReportItem, ResourceSummary } from "@/types/api";

const MODERATION_API_BASE_URL = "/moderation";

export const moderationApi = {
    async getPendingResources(pagination?: PaginationParams): Promise<PaginatedApiResponse<ResourceSummary>> {
        const params = new URLSearchParams();
        appendPaginationParams(params, pagination);
        return apiClient.get<PaginatedApiResponse<ResourceSummary>>(`${MODERATION_API_BASE_URL}/resources/pending?${params.toString()}`);
    },

    async getPendingListings(pagination?: PaginationParams): Promise<PaginatedApiResponse<ListingSummary>> {
        const params = new URLSearchParams();
        appendPaginationParams(params, pagination);
        return apiClient.get<PaginatedApiResponse<ListingSummary>>(`${MODERATION_API_BASE_URL}/listings/pending?${params.toString()}`);
    },

    async getResourceReports(pagination?: PaginationParams): Promise<PaginatedApiResponse<ReportItem>> {
        const params = new URLSearchParams();
        appendPaginationParams(params, pagination);
        return apiClient.get<PaginatedApiResponse<ReportItem>>(`${MODERATION_API_BASE_URL}/resources/reports?${params.toString()}`);
    },

    async dismissResourceReport(reportId: number): Promise<EmptyApiResponse> {
        return apiClient.post<EmptyApiResponse>(`${MODERATION_API_BASE_URL}/resources/reports/${reportId}/dismiss`);
    },

    async getListingReports(pagination?: PaginationParams): Promise<PaginatedApiResponse<ListingReportItem>> {
        const params = new URLSearchParams();
        appendPaginationParams(params, pagination);
        return apiClient.get<PaginatedApiResponse<ListingReportItem>>(`${MODERATION_API_BASE_URL}/listings/reports?${params.toString()}`);
    },

    async dismissListingReport(reportId: number): Promise<EmptyApiResponse> {
        return apiClient.post<EmptyApiResponse>(`${MODERATION_API_BASE_URL}/listings/reports/${reportId}/dismiss`);
    },
}
