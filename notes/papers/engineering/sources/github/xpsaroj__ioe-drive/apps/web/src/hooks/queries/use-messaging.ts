import { useQuery, useMutation, useQueryClient, keepPreviousData } from '@tanstack/react-query';

import { messagingApi } from '@/lib/api/messaging-api';

export const messagingKeys = {
    all: ['messaging-conversations'] as const,
    byId: (conversationId: number) => ['messaging-conversations', conversationId] as const,
    // Called with no `page` to get a stable prefix for invalidating every page at once.
    conversations: (page?: number) => page === undefined
        ? ['messaging-conversations', 'list'] as const
        : ['messaging-conversations', 'list', page] as const,
    messages: (conversationId: number, page?: number) => page === undefined
        ? ['messaging-conversations', conversationId, 'messages'] as const
        : ['messaging-conversations', conversationId, 'messages', page] as const,
    unreadCount: ['messaging-conversations', 'unread-count'] as const,
};

/** Thread header detail (listing + both participants) - the inbox list's shape, minus preview-only fields. */
export function useConversation(conversationId: number) {
    return useQuery({
        queryKey: messagingKeys.byId(conversationId),
        queryFn: async () => {
            const response = await messagingApi.getConversation(conversationId);
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch conversation');
            }
            return response.data;
        },
        enabled: !!conversationId,
    });
}

/** This user's inbox, paginated, most recently active thread first. */
export function useConversations(page: number = 1) {
    return useQuery({
        queryKey: messagingKeys.conversations(page),
        queryFn: async () => {
            const response = await messagingApi.getConversations({ page });
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch conversations');
            }
            return { items: response.data, meta: response.meta };
        },
        placeholderData: keepPreviousData,
    });
}

// Chunk size for both the initial load and each "load older" fetch.
export const MESSAGE_PAGE_SIZE = 50;

/** First (most recent) page only - ConversationThread drives further pages itself via
 * useLoadOlderMessages, merging into its own local message list rather than a cached query. */
export function useConversationMessages(conversationId: number) {
    return useQuery({
        queryKey: messagingKeys.messages(conversationId),
        queryFn: async () => {
            const response = await messagingApi.getMessages(conversationId, { page: 1, limit: MESSAGE_PAGE_SIZE });
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch messages');
            }
            return { items: response.data, meta: response.meta };
        },
        enabled: !!conversationId,
    });
}

/** Fetches one older page of a conversation's thread on demand ("Load older messages").
 * A one-shot mutation rather than a cached query - the thread keeps its own merged,
 * append/prepend-friendly message list in local state (see ConversationThread). */
export function useLoadOlderMessages(conversationId: number) {
    return useMutation({
        mutationFn: async (page: number) => {
            const response = await messagingApi.getMessages(conversationId, { page, limit: MESSAGE_PAGE_SIZE });
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch messages');
            }
            return { items: response.data, meta: response.meta };
        },
    });
}

/** Starts (or reuses) a thread with a listing's poster and sends the first message. */
export function useStartConversation() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async ({ listingId, message }: { listingId: number; message: string }) => {
            const response = await messagingApi.startConversation(listingId, message);
            if (!response.success) {
                throw new Error(response.error || 'Failed to send message');
            }
            return response.data;
        },
        onSuccess: () => {
            // Just the inbox list, not messagingKeys.all - that prefix also matches
            // messagingKeys.messages(conversationId), and an open thread's messages are
            // deliberately not query-driven (see useConversationMessages) - invalidating them
            // here would refetch page 1 and stomp the thread's local state/scroll position.
            queryClient.invalidateQueries({ queryKey: messagingKeys.conversations() });
        },
    });
}

export function useMarkConversationRead(conversationId: number) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async () => {
            const response = await messagingApi.markConversationRead(conversationId);
            if (!response.success) {
                throw new Error(response.error || 'Failed to mark conversation as read');
            }
            return response;
        },
        onSuccess: () => {
            // Same reasoning as useStartConversation above - avoid messagingKeys.all.
            queryClient.invalidateQueries({ queryKey: messagingKeys.conversations() });
            queryClient.invalidateQueries({ queryKey: messagingKeys.unreadCount });
        },
    });
}

/** Cold-start value for the nav badge, before the socket's live conversation_updated events take over. */
export function useUnreadCount() {
    return useQuery({
        queryKey: messagingKeys.unreadCount,
        queryFn: async () => {
            const response = await messagingApi.getUnreadCount();
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch unread count');
            }
            return response.data;
        },
    });
}
