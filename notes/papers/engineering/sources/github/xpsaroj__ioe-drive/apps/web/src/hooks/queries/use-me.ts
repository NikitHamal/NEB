import { useAuth } from '@clerk/nextjs';
import { useQuery, useMutation, useQueryClient, keepPreviousData } from '@tanstack/react-query';

import { meApi } from '@/lib/api/me-api';
import { marketplaceApi } from '@/lib/api/marketplace-api';
import { academicsKeys } from './use-academics';
import { resourcesKeys } from './use-resources';
import type { Profile, UserProfile } from '@/types/entities';
import type { ResourceSummary } from '@/types/api';

export const meKeys = {
    all: ['me'] as const,
    user: ['me', 'user'] as const,
    weeklySummary: ['me', 'weekly-summary'] as const,
    // Called with no `page` to get a stable prefix for invalidating every page at once.
    uploadedResources: (page?: number) => page === undefined
        ? ['me', 'uploaded-resources'] as const
        : ['me', 'uploaded-resources', page] as const,
    recentResources: (page?: number) => page === undefined
        ? ['me', 'recent-resources'] as const
        : ['me', 'recent-resources', page] as const,
    bookmarkedResources: (page?: number) => page === undefined
        ? ['me', 'bookmarked-resources'] as const
        : ['me', 'bookmarked-resources', page] as const,
    bookmarkedResourceIds: ['me', 'bookmarked-resource-ids'] as const,
    resourceVoteValues: ['me', 'resource-vote-values'] as const,
    myMarketplaceListings: (page?: number) => page === undefined
        ? ['me', 'marketplace-listings'] as const
        : ['me', 'marketplace-listings', page] as const,
};

/** Adjusts a cached resource's counts to reflect a vote changing from oldValue to newValue (either can be 0 for "no vote"). */
function applyVoteDelta(resource: ResourceSummary, oldValue: number, newValue: number): ResourceSummary {
    return {
        ...resource,
        upvoteCount: resource.upvoteCount + (newValue === 1 ? 1 : 0) - (oldValue === 1 ? 1 : 0),
        downvoteCount: resource.downvoteCount + (newValue === -1 ? 1 : 0) - (oldValue === -1 ? 1 : 0),
    };
}

export function useMe() {
    const { isSignedIn } = useAuth();

    return useQuery({
        queryKey: meKeys.user,
        queryFn: async () => {
            const response = await meApi.getMyProfile();
            if (!response.success) {
                throw new Error(response.error ?? 'Failed to fetch user data.');
            }
            return response.data;
        },
        enabled: isSignedIn,
        staleTime: 20 * 60 * 1000,
        gcTime: 30 * 60 * 1000,
    });
}

export function useUpdateProfile() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (profileData: Partial<Omit<Profile, "id" | "userId">>) => meApi.updateMyProfile(profileData),

        onMutate: async (newProfile) => {
            await queryClient.cancelQueries({ queryKey: meKeys.user });

            const previousProfile = queryClient.getQueryData<UserProfile>(meKeys.user);

            queryClient.setQueryData<UserProfile>(meKeys.user, (old) =>
                old ? { ...old, profile: { ...old.profile, ...newProfile } } : old
            );

            return { previousProfile };
        },

        onError: (_err, _newProfile, context) => {
            if (context?.previousProfile) {
                queryClient.setQueryData(meKeys.user, context.previousProfile);
            }
        },

        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: meKeys.user });
            queryClient.invalidateQueries({
                queryKey: [...academicsKeys.all, "subject-offerings"],
            });
        },
    });
}

export function useWeeklySummary() {
    const { isSignedIn } = useAuth();

    return useQuery({
        queryKey: meKeys.weeklySummary,
        queryFn: async () => {
            const response = await meApi.getWeeklySummary();
            if (!response.success) {
                throw new Error(response.error ?? 'Failed to fetch weekly summary.');
            }
            return response.data;
        },
        enabled: isSignedIn,
    });
}

export function useUploadedResources(page: number = 1) {
    const { isSignedIn } = useAuth();

    return useQuery({
        queryKey: meKeys.uploadedResources(page),
        queryFn: async () => {
            const response = await meApi.getUploadedResources({ page });
            if (!response.success) {
                throw new Error(response.error ?? 'Failed to fetch uploaded resources.');
            }
            return { items: response.data, meta: response.meta };
        },
        enabled: isSignedIn,
        placeholderData: keepPreviousData,
    });
}

/** Marketplace listings the current user has posted, any status - backs the "My Listings" view. */
export function useMyMarketplaceListings(page: number = 1) {
    const { isSignedIn } = useAuth();

    return useQuery({
        queryKey: meKeys.myMarketplaceListings(page),
        queryFn: async () => {
            const response = await marketplaceApi.getMyListings({ page });
            if (!response.success) {
                throw new Error(response.error ?? 'Failed to fetch your listings.');
            }
            return { items: response.data, meta: response.meta };
        },
        enabled: isSignedIn,
        placeholderData: keepPreviousData,
    });
}

export function useRecentResources(page: number = 1) {
    const { isSignedIn } = useAuth();

    return useQuery({
        queryKey: meKeys.recentResources(page),
        queryFn: async () => {
            const response = await meApi.getRecentResources({ page });
            if (!response.success) {
                throw new Error(response.error ?? 'Failed to fetch recent resources.');
            }
            return { items: response.data, meta: response.meta };
        },
        enabled: isSignedIn,
        placeholderData: keepPreviousData,
    });
}

export function useBookmarkedResources(page: number = 1) {
    const { isSignedIn } = useAuth();

    return useQuery({
        queryKey: meKeys.bookmarkedResources(page),
        queryFn: async () => {
            const response = await meApi.getBookmarkedResources({ page });
            if (!response.success) {
                throw new Error(response.error ?? 'Failed to fetch bookmarked resources.');
            }
            return { items: response.data, meta: response.meta };
        },
        enabled: isSignedIn,
        placeholderData: keepPreviousData,
    });
}

/**
 * Fetches every resource ID the current user has bookmarked, for cheap "is this
 * bookmarked" membership checks across many resources at once (e.g. a bookmark icon on
 * every ResourceCard) - see useBookmarkResource/useUnbookmarkResource below for how
 * this cache gets kept in sync with actual bookmark/unbookmark actions.
 */
export function useBookmarkedResourceIds() {
    const { isSignedIn } = useAuth();

    return useQuery({
        queryKey: meKeys.bookmarkedResourceIds,
        queryFn: async () => {
            const response = await meApi.getBookmarkedResourceIds();
            if (!response.success) {
                throw new Error(response.error ?? 'Failed to fetch bookmarked resource IDs.');
            }
            return response.data;
        },
        enabled: isSignedIn,
        // Bookmarks change far less often than resources get browsed, and the mutations
        // below explicitly invalidate this on any bookmark/unbookmark, so correctness
        // for our own actions doesn't depend on staleTime.
        staleTime: 30 * 60 * 1000,
        gcTime: 40 * 60 * 1000,
    });
}

export function useMarkResourceAsRecentlyAccessed() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (resourceId: string) => meApi.markResourceAsRecentlyAccessed(resourceId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: meKeys.recentResources() });
        },
    });
}

export function useBookmarkResource() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (resourceId: string) => meApi.markResourceAsBookmarked(resourceId),

        // Optimistically add to the ID set so a card's bookmark icon flips instantly,
        // instead of waiting on a round-trip + refetch.
        onMutate: async (resourceId) => {
            await queryClient.cancelQueries({ queryKey: meKeys.bookmarkedResourceIds });

            const previousIds = queryClient.getQueryData<number[]>(meKeys.bookmarkedResourceIds);

            queryClient.setQueryData<number[]>(meKeys.bookmarkedResourceIds, (old) =>
                old ? [...old, Number(resourceId)] : old
            );

            return { previousIds };
        },

        onError: (_err, _resourceId, context) => {
            if (context?.previousIds) {
                queryClient.setQueryData(meKeys.bookmarkedResourceIds, context.previousIds);
            }
        },

        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: meKeys.bookmarkedResourceIds });
            queryClient.invalidateQueries({ queryKey: meKeys.bookmarkedResources() });
        },
    });
}

/** Every resource the current user has voted on, mapped to their vote (1 or -1) - backs the up/downvote buttons' highlighted state on every ResourceCard. */
export function useResourceVoteValues() {
    const { isSignedIn } = useAuth();

    return useQuery({
        queryKey: meKeys.resourceVoteValues,
        queryFn: async () => {
            const response = await meApi.getResourceVoteValues();
            if (!response.success) {
                throw new Error(response.error ?? 'Failed to fetch vote values.');
            }
            return response.data;
        },
        enabled: isSignedIn,
        staleTime: 30 * 60 * 1000,
        gcTime: 40 * 60 * 1000,
    });
}

export function useSetResourceVote() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ resourceId, value }: { resourceId: string; value: 1 | -1 }) => meApi.setResourceVote(resourceId, value),

        onMutate: async ({ resourceId, value }) => {
            await queryClient.cancelQueries({ queryKey: meKeys.resourceVoteValues });
            await queryClient.cancelQueries({ queryKey: resourcesKeys.byId(Number(resourceId)) });

            const previousVoteValues = queryClient.getQueryData<Record<number, 1 | -1>>(meKeys.resourceVoteValues);
            const previousResource = queryClient.getQueryData<ResourceSummary>(resourcesKeys.byId(Number(resourceId)));
            const oldValue = previousVoteValues?.[Number(resourceId)] ?? 0;

            queryClient.setQueryData<Record<number, 1 | -1>>(meKeys.resourceVoteValues, (old) =>
                old ? { ...old, [Number(resourceId)]: value } : old
            );
            queryClient.setQueryData<ResourceSummary>(resourcesKeys.byId(Number(resourceId)), (old) =>
                old ? applyVoteDelta(old, oldValue, value) : old
            );

            return { previousVoteValues, previousResource, resourceId };
        },

        onError: (_err, { resourceId }, context) => {
            if (context?.previousVoteValues) {
                queryClient.setQueryData(meKeys.resourceVoteValues, context.previousVoteValues);
            }
            if (context?.previousResource) {
                queryClient.setQueryData(resourcesKeys.byId(Number(resourceId)), context.previousResource);
            }
        },

        onSettled: (_data, _err, { resourceId }) => {
            queryClient.invalidateQueries({ queryKey: meKeys.resourceVoteValues });
            queryClient.invalidateQueries({ queryKey: resourcesKeys.byId(Number(resourceId)) });
        },
    });
}

export function useClearResourceVote() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (resourceId: string) => meApi.clearResourceVote(resourceId),

        onMutate: async (resourceId) => {
            await queryClient.cancelQueries({ queryKey: meKeys.resourceVoteValues });
            await queryClient.cancelQueries({ queryKey: resourcesKeys.byId(Number(resourceId)) });

            const previousVoteValues = queryClient.getQueryData<Record<number, 1 | -1>>(meKeys.resourceVoteValues);
            const previousResource = queryClient.getQueryData<ResourceSummary>(resourcesKeys.byId(Number(resourceId)));
            const oldValue = previousVoteValues?.[Number(resourceId)] ?? 0;

            queryClient.setQueryData<Record<number, 1 | -1>>(meKeys.resourceVoteValues, (old) => {
                if (!old) return old;
                const next = { ...old };
                delete next[Number(resourceId)];
                return next;
            });
            queryClient.setQueryData<ResourceSummary>(resourcesKeys.byId(Number(resourceId)), (old) =>
                old ? applyVoteDelta(old, oldValue, 0) : old
            );

            return { previousVoteValues, previousResource, resourceId };
        },

        onError: (_err, resourceId, context) => {
            if (context?.previousVoteValues) {
                queryClient.setQueryData(meKeys.resourceVoteValues, context.previousVoteValues);
            }
            if (context?.previousResource) {
                queryClient.setQueryData(resourcesKeys.byId(Number(resourceId)), context.previousResource);
            }
        },

        onSettled: (_data, _err, resourceId) => {
            queryClient.invalidateQueries({ queryKey: meKeys.resourceVoteValues });
            queryClient.invalidateQueries({ queryKey: resourcesKeys.byId(Number(resourceId)) });
        },
    });
}

export function useUnbookmarkResource() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (resourceId: string) => meApi.unmarkResourceAsBookmarked(resourceId),

        onMutate: async (resourceId) => {
            await queryClient.cancelQueries({ queryKey: meKeys.bookmarkedResourceIds });

            const previousIds = queryClient.getQueryData<number[]>(meKeys.bookmarkedResourceIds);

            queryClient.setQueryData<number[]>(meKeys.bookmarkedResourceIds, (old) =>
                old ? old.filter((id) => id !== Number(resourceId)) : old
            );

            return { previousIds };
        },

        onError: (_err, _resourceId, context) => {
            if (context?.previousIds) {
                queryClient.setQueryData(meKeys.bookmarkedResourceIds, context.previousIds);
            }
        },

        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: meKeys.bookmarkedResourceIds });
            queryClient.invalidateQueries({ queryKey: meKeys.bookmarkedResources() });
        },
    });
}
