"use client";
import { useEffect, useRef, useState } from "react";
import { useAuth } from "@clerk/nextjs";
import { io, type Socket } from "socket.io-client";
import { useQueryClient } from "@tanstack/react-query";

import { MarketplaceSocketContext } from "@/hooks/use-marketplace-socket";
import { messagingKeys } from "@/hooks/queries/use-messaging";

// The gateway is mounted on the same NestJS process/port as the REST API (see apps/server/src/main.ts) -
// derived from NEXT_PUBLIC_API_BASE_URL rather than its own env var, so the two can never point at
// different backends by accident.
const WS_BASE_URL = (process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:4000/api").replace(/\/api\/?$/, "");

interface ConversationUpdatedPayload {
    conversationId: number;
    unreadDelta: number;
}

// Connects once at app-shell level. Only handles connection lifecycle plus the always-on
// conversation_updated stream (nav badge + inbox list) - a joined conversation's own
// new_message stream is handled by the thread page itself, only while that thread is open.
export function MessagingSocketProvider({ children }: { children: React.ReactNode }) {
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

        const instance = io(`${WS_BASE_URL}/marketplace-messaging`, {
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

        const handleConversationUpdated = (payload: ConversationUpdatedPayload) => {
            queryClient.setQueryData(
                messagingKeys.unreadCount,
                (old?: { unreadCount: number }) =>
                    old ? { unreadCount: Math.max(0, old.unreadCount + payload.unreadDelta) } : old,
            );
            queryClient.invalidateQueries({ queryKey: messagingKeys.all });
        };

        socket.on("conversation_updated", handleConversationUpdated);

        return () => {
            socket.off("conversation_updated", handleConversationUpdated);
        };
    }, [socket, queryClient]);

    return (
        <MarketplaceSocketContext.Provider value={socket}>
            {children}
        </MarketplaceSocketContext.Provider>
    );
}
