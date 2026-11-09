import { useQuery, useMutation, useQueryClient, keepPreviousData } from '@tanstack/react-query';
import { resourcesApi } from '@/lib/api/resources-api';
import { meKeys } from './use-me';
import { moderationKeys } from './use-moderation';
import type { ModerationReasonInput, UpdateResourceInput } from '@/lib/validators/resources';
import type { ResourceLinkInput } from '@/lib/validators/resource-links';

export const resourcesKeys = {
    all: ['resources'] as const,
    byId: (id: number) => ['resources', id] as const,
    // Called with no `page` to get a stable prefix for invalidating every page at once.
    bySubjectOfferingId: (offeringId?: number, page?: number) => page === undefined
        ? ['resources', 'subject-offering', offeringId] as const
        : ['resources', 'subject-offering', offeringId, page] as const,
    byUploaderId: (uploaderId?: number, page?: number) => page === undefined
        ? ['resources', 'uploader', uploaderId] as const
        : ['resources', 'uploader', uploaderId, page] as const,
    fileDownloadUrl: (resourceId: number, fileId: number) => ['resources', resourceId, 'files', fileId, 'download-url'] as const,
    search: (q: string, page?: number) => page === undefined
        ? ['resources', 'search', q] as const
        : ['resources', 'search', q, page] as const,
    searchSuggestions: (q: string, limit?: number) => ['resources', 'search-suggestions', q, limit] as const,
    similar: (resourceId: number, limit?: number) => ['resources', resourceId, 'similar', limit] as const,
};

export function useResource(resourceId: number) {
    return useQuery({
        queryKey: resourcesKeys.byId(resourceId),
        queryFn: async () => {
            const response = await resourcesApi.getResourceById(resourceId);
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch resource');
            }
            return response.data;
        },
    });
}

export function useResourcesBySubjectOfferingId(offeringId?: number, page: number = 1) {
    return useQuery({
        queryKey: resourcesKeys.bySubjectOfferingId(offeringId, page),
        queryFn: async () => {
            if (!offeringId) {
                throw new Error('Subject Offering ID is required to fetch resources');
            }
            const response = await resourcesApi.getResourcesBySubjectOffering(offeringId, { page });
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch resources for subject');
            }

            return { items: response.data, meta: response.meta };
        },
        enabled: !!offeringId,
        staleTime: 10 * 60 * 1000,
        placeholderData: keepPreviousData,
    });
}

export function useCreateResource() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (formData: FormData) => {
            const response = await resourcesApi.createResource(formData);
            if (!response.success) {
                throw new Error(response.error || 'Failed to create resource');
            }
            return response;
        },
        onSuccess: (response) => {
            queryClient.invalidateQueries({ queryKey: resourcesKeys.all });
            queryClient.invalidateQueries({
                queryKey: resourcesKeys.bySubjectOfferingId(response.data.offeringId)
            });
        },
    });
}

export function useUpdateResource(resourceId: number) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (resourceData: UpdateResourceInput) =>
            resourcesApi.updateResource(resourceId, resourceData),
        onSuccess: (response) => {
            if (!response.success) {
                throw new Error(response.error || 'Failed to update resource');
            }
            // PATCH response is the bare row only (no files/uploader) - invalidate rather than write it into the full-detail cache slot.
            queryClient.invalidateQueries({ queryKey: resourcesKeys.byId(resourceId) });
            queryClient.invalidateQueries({ queryKey: resourcesKeys.all });
            // The edited resource may show up in the current user's uploads list too
            queryClient.invalidateQueries({ queryKey: meKeys.uploadedResources() });
        },
    });
}

export function useDeleteResource() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (resourceId: number) => {
            const response = await resourcesApi.deleteResource(resourceId);
            if (!response.success) {
                throw new Error(response.error || 'Failed to delete resource');
            }
            return response;
        },
        onSuccess: (_response, resourceId) => {
            queryClient.removeQueries({ queryKey: resourcesKeys.byId(resourceId) });
            queryClient.invalidateQueries({ queryKey: resourcesKeys.all });
            queryClient.invalidateQueries({ queryKey: meKeys.uploadedResources() });
        },
    });
}

export function useAddResourceFiles(resourceId: number) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (formData: FormData) => {
            const response = await resourcesApi.addResourceFiles(resourceId, formData);
            if (!response.success) {
                throw new Error(response.error || 'Failed to add files');
            }
            return response;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: resourcesKeys.byId(resourceId) });
        },
    });
}

export function useRemoveResourceFile(resourceId: number) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (fileId: number) => {
            const response = await resourcesApi.removeResourceFile(resourceId, fileId);
            if (!response.success) {
                throw new Error(response.error || 'Failed to remove file');
            }
            return response;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: resourcesKeys.byId(resourceId) });
        },
    });
}

export function useAddResourceLinks(resourceId: number) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (links: ResourceLinkInput[]) => {
            const response = await resourcesApi.addResourceLinks(resourceId, links);
            if (!response.success) {
                throw new Error(response.error || 'Failed to add links');
            }
            return response;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: resourcesKeys.byId(resourceId) });
        },
    });
}

export function useRemoveResourceLink(resourceId: number) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (linkId: number) => {
            const response = await resourcesApi.removeResourceLink(resourceId, linkId);
            if (!response.success) {
                throw new Error(response.error || 'Failed to remove link');
            }
            return response;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: resourcesKeys.byId(resourceId) });
        },
    });
}

// A few minutes of safety margin below the server's actual SAS expiry.
const FILE_DOWNLOAD_URL_STALE_TIME = 13 * 60 * 1000;
const FILE_DOWNLOAD_URL_GC_TIME = 14 * 60 * 1000;

// staleTime keeps a revisited file's cached URL usable instead of refetching every time.
export function useFileDownloadUrl(resourceId: number, fileId?: number) {
    return useQuery({
        queryKey: resourcesKeys.fileDownloadUrl(resourceId, fileId ?? -1),
        queryFn: async () => {
            if (!fileId) {
                throw new Error('File ID is required to fetch a download URL');
            }
            const response = await resourcesApi.getFileDownloadUrl(resourceId, fileId);
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch download URL');
            }
            return response.data;
        },
        enabled: !!resourceId && !!fileId,
        staleTime: FILE_DOWNLOAD_URL_STALE_TIME,
        gcTime: FILE_DOWNLOAD_URL_GC_TIME,
    });
}

// Only called on an explicit "Download" click, not generated eagerly alongside the inline preview URL.
export function useDownloadFile(resourceId: number) {
    return useMutation({
        mutationFn: async (fileId: number) => {
            const response = await resourcesApi.getFileDownloadUrl(resourceId, fileId, true);
            if (!response.success) {
                throw new Error(response.error || 'Failed to get download link');
            }
            return response.data.url;
        },
    });
}

export function useResourcesByUploaderId(uploaderId?: number, page: number = 1) {
    return useQuery({
        queryKey: resourcesKeys.byUploaderId(uploaderId, page),
        queryFn: async () => {
            if (!uploaderId) {
                throw new Error('Uploader ID is required to fetch resources');
            }
            const response = await resourcesApi.getResourcesByUploader(uploaderId, { page });
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch resources for uploader');
            }

            return { items: response.data, meta: response.meta };
        },
        enabled: !!uploaderId,
        staleTime: 10 * 60 * 1000,
        placeholderData: keepPreviousData,
    });
}

export const MIN_SEARCH_QUERY_LENGTH = 2;

export function useSearchResources(q: string, page: number = 1, limit?: number) {
    const trimmed = q.trim();

    return useQuery({
        queryKey: resourcesKeys.search(trimmed, page),
        queryFn: async () => {
            const response = await resourcesApi.searchResources(trimmed, { page, limit });
            if (!response.success) {
                throw new Error(response.error || 'Failed to search resources');
            }

            return { items: response.data, meta: response.meta };
        },
        enabled: trimmed.length >= MIN_SEARCH_QUERY_LENGTH,
        placeholderData: keepPreviousData,
    });
}

// Lean, capped-list variant of useSearchResources for the live-typing search palette.
export function useSearchSuggestions(q: string, limit?: number) {
    const trimmed = q.trim();

    return useQuery({
        queryKey: resourcesKeys.searchSuggestions(trimmed, limit),
        queryFn: async () => {
            const response = await resourcesApi.searchSuggestions(trimmed, limit);
            if (!response.success) {
                throw new Error(response.error || 'Failed to search resources');
            }
            return response.data;
        },
        enabled: trimmed.length >= MIN_SEARCH_QUERY_LENGTH,
        placeholderData: keepPreviousData,
    });
}

// Shared invalidation after any moderator action or a report.
function invalidateAfterModeration(queryClient: ReturnType<typeof useQueryClient>, resourceId: number) {
    queryClient.invalidateQueries({ queryKey: resourcesKeys.byId(resourceId) });
    queryClient.invalidateQueries({ queryKey: resourcesKeys.all });
    queryClient.invalidateQueries({ queryKey: meKeys.uploadedResources() });
    queryClient.invalidateQueries({ queryKey: moderationKeys.pendingResources() });
    queryClient.invalidateQueries({ queryKey: moderationKeys.resourceReports() });
}

/** Approves a pending resource, making it publicly visible (moderator-only). */
export function useApproveResource(resourceId: number) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async () => {
            const response = await resourcesApi.approveResource(resourceId);
            if (!response.success) {
                throw new Error(response.error || 'Failed to approve resource');
            }
            return response;
        },
        onSuccess: () => invalidateAfterModeration(queryClient, resourceId),
    });
}

// Resubmittable - the uploader editing it resets the resource back to pending.
export function useRejectResource(resourceId: number) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (data: ModerationReasonInput) => {
            const response = await resourcesApi.rejectResource(resourceId, data);
            if (!response.success) {
                throw new Error(response.error || 'Failed to reject resource');
            }
            return response;
        },
        onSuccess: () => invalidateAfterModeration(queryClient, resourceId),
    });
}

// Purges the resource's files and marks it permanently removed.
export function useRemoveResource(resourceId: number) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (data: ModerationReasonInput) => {
            const response = await resourcesApi.removeResource(resourceId, data);
            if (!response.success) {
                throw new Error(response.error || 'Failed to remove resource');
            }
            return response;
        },
        onSuccess: () => invalidateAfterModeration(queryClient, resourceId),
    });
}

// Stays live until a moderator reviews the report.
export function useReportResource(resourceId: number) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (data: ModerationReasonInput) => {
            const response = await resourcesApi.reportResource(resourceId, data);
            if (!response.success) {
                throw new Error(response.error || 'Failed to report resource');
            }
            return response;
        },
        onSuccess: () => queryClient.invalidateQueries({ queryKey: moderationKeys.resourceReports() }),
    });
}

// Backs the resource detail page's "Similar Resources" panel.
export function useSimilarResources(resourceId: number, limit?: number) {
    return useQuery({
        queryKey: resourcesKeys.similar(resourceId, limit),
        queryFn: async () => {
            const response = await resourcesApi.getSimilarResources(resourceId, limit);
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch similar resources');
            }
            return response.data;
        },
        enabled: !!resourceId,
    });
}
