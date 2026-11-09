import { apiClient } from "./api-client";
import { appendPaginationParams, type PaginationParams } from "./pagination";
import type { Resource } from "@/types/entities";
import type { ApiResponse, EmptyApiResponse, PaginatedApiResponse, ResourceSummary, ResourceSuggestion } from "@/types/api";
import type { ModerationReasonInput, UpdateResourceInput } from "../validators/resources";
import type { ResourceLinkInput } from "../validators/resource-links";

const RESOURCES_API_BASE_URL = "/resources";

export const resourcesApi = {
    async createResource(formData: FormData): Promise<ApiResponse<Resource>> {
        return apiClient.postForm<ApiResponse<Resource>>(`${RESOURCES_API_BASE_URL}`, formData);
    },

    async updateResource(resourceId: number, resourceData: UpdateResourceInput): Promise<ApiResponse<Resource>> {
        return apiClient.patch<ApiResponse<Resource>>(`${RESOURCES_API_BASE_URL}/${resourceId}`, resourceData);
    },

    async deleteResource(resourceId: number): Promise<EmptyApiResponse> {
        return apiClient.delete<EmptyApiResponse>(`${RESOURCES_API_BASE_URL}/${resourceId}`);
    },

    async addResourceFiles(resourceId: number, formData: FormData): Promise<EmptyApiResponse> {
        return apiClient.postForm<EmptyApiResponse>(`${RESOURCES_API_BASE_URL}/${resourceId}/files`, formData);
    },

    async removeResourceFile(resourceId: number, fileId: number): Promise<EmptyApiResponse> {
        return apiClient.delete<EmptyApiResponse>(`${RESOURCES_API_BASE_URL}/${resourceId}/files/${fileId}`);
    },

    async addResourceLinks(resourceId: number, links: ResourceLinkInput[]): Promise<EmptyApiResponse> {
        return apiClient.post<EmptyApiResponse>(`${RESOURCES_API_BASE_URL}/${resourceId}/links`, { links });
    },

    async removeResourceLink(resourceId: number, linkId: number): Promise<EmptyApiResponse> {
        return apiClient.delete<EmptyApiResponse>(`${RESOURCES_API_BASE_URL}/${resourceId}/links/${linkId}`);
    },

    async getFileDownloadUrl(resourceId: number, fileId: number, forceDownload = false): Promise<ApiResponse<{ url: string }>> {
        const query = forceDownload ? "?download=true" : "";
        return apiClient.get<ApiResponse<{ url: string }>>(`${RESOURCES_API_BASE_URL}/${resourceId}/files/${fileId}/download-url${query}`);
    },

    async getResourceById(resourceId: number): Promise<ApiResponse<ResourceSummary>> {
        return apiClient.get<ApiResponse<ResourceSummary>>(`${RESOURCES_API_BASE_URL}/${resourceId}`);
    },

    async getResourcesBySubjectOffering(offeringId: number, pagination?: PaginationParams): Promise<PaginatedApiResponse<ResourceSummary>> {
        const params = new URLSearchParams({
            offeringId: offeringId.toString()
        });
        appendPaginationParams(params, pagination);
        return apiClient.get<PaginatedApiResponse<ResourceSummary>>(`${RESOURCES_API_BASE_URL}?${params.toString()}`);
    },

    async getResourcesByUploader(uploaderId: number, pagination?: PaginationParams): Promise<PaginatedApiResponse<ResourceSummary>> {
        const params = new URLSearchParams({
            userId: uploaderId.toString()
        });
        appendPaginationParams(params, pagination);
        return apiClient.get<PaginatedApiResponse<ResourceSummary>>(`${RESOURCES_API_BASE_URL}?${params.toString()}`);
    },

    async searchResources(q: string, pagination?: PaginationParams): Promise<PaginatedApiResponse<ResourceSummary>> {
        const params = new URLSearchParams({ q });
        appendPaginationParams(params, pagination);
        return apiClient.get<PaginatedApiResponse<ResourceSummary>>(`${RESOURCES_API_BASE_URL}?${params.toString()}`);
    },

    async searchSuggestions(q: string, limit?: number): Promise<ApiResponse<ResourceSuggestion[]>> {
        const params = new URLSearchParams({ q });
        if (limit) params.set("limit", String(limit));
        return apiClient.get<ApiResponse<ResourceSuggestion[]>>(`${RESOURCES_API_BASE_URL}/search-suggestions?${params.toString()}`);
    },

    async getSimilarResources(resourceId: number, limit?: number): Promise<ApiResponse<ResourceSuggestion[]>> {
        const query = limit ? `?limit=${limit}` : "";
        return apiClient.get<ApiResponse<ResourceSuggestion[]>>(`${RESOURCES_API_BASE_URL}/${resourceId}/similar${query}`);
    },

    async approveResource(resourceId: number): Promise<ApiResponse<Resource>> {
        return apiClient.post<ApiResponse<Resource>>(`${RESOURCES_API_BASE_URL}/${resourceId}/approve`);
    },

    async rejectResource(resourceId: number, data: ModerationReasonInput): Promise<ApiResponse<Resource>> {
        return apiClient.post<ApiResponse<Resource>>(`${RESOURCES_API_BASE_URL}/${resourceId}/reject`, data);
    },

    async removeResource(resourceId: number, data: ModerationReasonInput): Promise<ApiResponse<Resource>> {
        return apiClient.post<ApiResponse<Resource>>(`${RESOURCES_API_BASE_URL}/${resourceId}/remove`, data);
    },

    async reportResource(resourceId: number, data: ModerationReasonInput): Promise<EmptyApiResponse> {
        return apiClient.post<EmptyApiResponse>(`${RESOURCES_API_BASE_URL}/${resourceId}/report`, data);
    },
}
