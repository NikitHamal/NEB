import { useQuery, useMutation, useQueryClient, keepPreviousData } from '@tanstack/react-query';

import { moderationApi } from '@/lib/api/moderation-api';

export const moderationKeys = {
    all: ['moderation'] as const,
    // Called with no `page` to get a stable prefix for invalidating every page at once.
    pendingResources: (page?: number) => page === undefined
        ? ['moderation', 'pending-resources'] as const
        : ['moderation', 'pending-resources', page] as const,
    pendingListings: (page?: number) => page === undefined
        ? ['moderation', 'pending-listings'] as const
        : ['moderation', 'pending-listings', page] as const,
    resourceReports: (page?: number) => page === undefined
        ? ['moderation', 'resource-reports'] as const
        : ['moderation', 'resource-reports', page] as const,
    listingReports: (page?: number) => page === undefined
        ? ['moderation', 'listing-reports'] as const
        : ['moderation', 'listing-reports', page] as const,
};

/** The review queue: resources awaiting a moderator's decision, oldest first. */
export function usePendingResources(page: number = 1) {
    return useQuery({
        queryKey: moderationKeys.pendingResources(page),
        queryFn: async () => {
            const response = await moderationApi.getPendingResources({ page });
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch pending resources');
            }
            return { items: response.data, meta: response.meta };
        },
        placeholderData: keepPreviousData,
    });
}

/** The review queue: marketplace listings awaiting a moderator's decision, oldest first. */
export function usePendingListings(page: number = 1) {
    return useQuery({
        queryKey: moderationKeys.pendingListings(page),
        queryFn: async () => {
            const response = await moderationApi.getPendingListings({ page });
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch pending listings');
            }
            return { items: response.data, meta: response.meta };
        },
        placeholderData: keepPreviousData,
    });
}

/** Open reports against already-approved resources. */
export function useResourceReports(page: number = 1) {
    return useQuery({
        queryKey: moderationKeys.resourceReports(page),
        queryFn: async () => {
            const response = await moderationApi.getResourceReports({ page });
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch reports');
            }
            return { items: response.data, meta: response.meta };
        },
        placeholderData: keepPreviousData,
    });
}

/** Closes a report with no change to the resource - the "unfounded report" case. */
export function useDismissResourceReport() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (reportId: number) => {
            const response = await moderationApi.dismissResourceReport(reportId);
            if (!response.success) {
                throw new Error(response.error || 'Failed to dismiss report');
            }
            return response;
        },
        onSuccess: () => queryClient.invalidateQueries({ queryKey: moderationKeys.resourceReports() }),
    });
}

/** Open reports against marketplace listings. */
export function useListingReports(page: number = 1) {
    return useQuery({
        queryKey: moderationKeys.listingReports(page),
        queryFn: async () => {
            const response = await moderationApi.getListingReports({ page });
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch listing reports');
            }
            return { items: response.data, meta: response.meta };
        },
        placeholderData: keepPreviousData,
    });
}

/** Closes a listing report with no change to the listing - the "unfounded report" case. */
export function useDismissListingReport() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (reportId: number) => {
            const response = await moderationApi.dismissListingReport(reportId);
            if (!response.success) {
                throw new Error(response.error || 'Failed to dismiss report');
            }
            return response;
        },
        onSuccess: () => queryClient.invalidateQueries({ queryKey: moderationKeys.listingReports() }),
    });
}
