import { useQuery, useMutation, useQueryClient, keepPreviousData } from '@tanstack/react-query';

import { notificationsApi } from '@/lib/api/notifications-api';

export const notificationsKeys = {
    all: ['notifications'] as const,
    // Called with no `page` to get a stable prefix for invalidating every page at once.
    list: (page?: number) => page === undefined
        ? ['notifications', 'list'] as const
        : ['notifications', 'list', page] as const,
    unreadCount: ['notifications', 'unread-count'] as const,
};

/** This user's notifications, paginated, newest first. `enabled` lets callers (the bell
 * dropdown) skip the fetch entirely until the panel is actually opened. */
export function useNotifications(page: number = 1, enabled: boolean = true) {
    return useQuery({
        queryKey: notificationsKeys.list(page),
        queryFn: async () => {
            const response = await notificationsApi.getNotifications({ page });
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch notifications');
            }
            return { items: response.data, meta: response.meta };
        },
        placeholderData: keepPreviousData,
        enabled,
    });
}

/** Cold-start value for the bell badge, before the socket's live notification_created events take over. */
export function useUnreadNotificationsCount() {
    return useQuery({
        queryKey: notificationsKeys.unreadCount,
        queryFn: async () => {
            const response = await notificationsApi.getUnreadCount();
            if (!response.success) {
                throw new Error(response.error || 'Failed to fetch unread count');
            }
            return response.data;
        },
    });
}

export function useMarkNotificationRead() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (notificationId: number) => {
            const response = await notificationsApi.markRead(notificationId);
            if (!response.success) {
                throw new Error(response.error || 'Failed to mark notification as read');
            }
            return response;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: notificationsKeys.all });
        },
    });
}

export function useMarkAllNotificationsRead() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async () => {
            const response = await notificationsApi.markAllRead();
            if (!response.success) {
                throw new Error(response.error || 'Failed to mark notifications as read');
            }
            return response;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: notificationsKeys.all });
        },
    });
}
