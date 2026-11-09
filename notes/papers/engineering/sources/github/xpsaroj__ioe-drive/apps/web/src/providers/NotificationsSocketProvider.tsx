"use client";
import { useEffect, useRef, useState } from "react";
import { useAuth } from "@clerk/nextjs";
import { io, type Socket } from "socket.io-client";
import { useQueryClient } from "@tanstack/react-query";

import { NotificationSocketContext } from "@/hooks/use-notifications-socket";
import { notificationsKeys } from "@/hooks/queries/use-notifications";

// The gateway is mounted on the same NestJS process/port as the REST API (see apps/server/src/main.ts) -
// derived from NEXT_PUBLIC_API_BASE_URL rather than its own env var, so the two can never point at
// different backends by accident.
const WS_BASE_URL = (process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:4000/api").replace(/\/api\/?$/, "");

// Separate connection/namespace from MessagingSocketProvider - notifications are a distinct
// domain (moderation events, not DMs) kept fully independent, same as the "Messages" nav
// badge staying untouched. Connects once at app-shell level and stays alive while signed in.
export function NotificationsSocketProvider({ children }: { children: React.ReactNode }) {
    const { isSignedIn, getToken } = useAuth();
    const queryClient = useQueryClient();
    const [socket, setSocket] = useState<Socket | null>(null);
    const socketRef = useRef<Socket | null>(null);

    useEffect(() => {
        if (!isSignedIn) {
            socketRef.current?.disconnect();
            socketRef.current = null;
            setSocket(null);
            return;
        }

        const instance = io(`${WS_BASE_URL}/notifications`, {
            auth: (cb) => {
                getToken().then((token) => cb({ token }));
            },
        });

        socketRef.current = instance;
        setSocket(instance);

        return () => {
            instance.disconnect();
            socketRef.current = null;
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isSignedIn]);

    useEffect(() => {
        if (!socket) return;

        // A newly-created notification is always unread by definition, so this just bumps
        // the count by 1 (unlike messaging's unreadDelta, there's no "delta" to read off the payload).
        const handleNotificationCreated = () => {
            queryClient.setQueryData(
                notificationsKeys.unreadCount,
                (old?: { unreadCount: number }) => (old ? { unreadCount: old.unreadCount + 1 } : old),
            );
            queryClient.invalidateQueries({ queryKey: notificationsKeys.all });
        };

        socket.on("notification_created", handleNotificationCreated);

        return () => {
            socket.off("notification_created", handleNotificationCreated);
        };
    }, [socket, queryClient]);

    return (
        <NotificationSocketContext.Provider value={socket}>
            {children}
        </NotificationSocketContext.Provider>
    );
}
