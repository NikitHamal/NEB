"use client";
import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";
import { ArrowDown, MessageCircle, Send } from "lucide-react";

import Button from "@/components/ui/Button";
import Textarea from "@/components/ui/Textarea";
import Loader from "@/components/ui/Loader";
import { useConversationMessages, useLoadOlderMessages, useMarkConversationRead } from "@/hooks/queries/use-messaging";
import { useMarketplaceSocket } from "@/hooks/use-marketplace-socket";
import { getErrorMessage } from "@/lib/errors";
import { cn } from "@/utils/cn";
import type { MessageSummary } from "@/types/api";

interface ConversationThreadProps {
    conversationId: number;
    currentUserId: number;
}

const NEAR_BOTTOM_THRESHOLD_PX = 120;

const isNearBottom = (container: HTMLDivElement | null): boolean => {
    if (!container) return true;
    return container.scrollHeight - container.scrollTop - container.clientHeight <= NEAR_BOTTOM_THRESHOLD_PX;
};

// Real-time chat is socket-only in v1 (see MessagingModule plan) - messages live in local state
// seeded from the initial fetch, then appended to directly as new_message events arrive, rather
// than fighting TanStack Query cache invalidation timing for a fast-moving list.
const ConversationThread = ({ conversationId, currentUserId }: ConversationThreadProps) => {
    const socket = useMarketplaceSocket();
    const { data, isPending, error } = useConversationMessages(conversationId);
    const { mutate: markRead } = useMarkConversationRead(conversationId);
    const { mutate: loadOlder, isPending: isLoadingOlder } = useLoadOlderMessages(conversationId);

    const [messages, setMessages] = useState<MessageSummary[]>([]);
    const [page, setPage] = useState(1);
    const [hasOlder, setHasOlder] = useState(false);
    const [hasNewMessageBelow, setHasNewMessageBelow] = useState(false);
    const [draft, setDraft] = useState("");
    const containerRef = useRef<HTMLDivElement>(null);
    const bottomRef = useRef<HTMLDivElement>(null);
    // Whether the next `messages` change should scroll to the bottom - true for the initial
    // load and new incoming messages, false while prepending older history (see handleLoadOlder,
    // which repositions the scroll offset itself instead).
    const autoScrollRef = useRef(true);
    // Which conversation's first page has already been seeded into local state - guards the
    // effect below so a background refetch of the same conversation (e.g. on window refocus)
    // can't reset the thread's local state/scroll position from under a live socket session.
    const seededConversationIdRef = useRef<number | null>(null);

    // Newest-first from the API - reverse to display oldest-first, like any chat thread.
    useEffect(() => {
        if (data && seededConversationIdRef.current !== conversationId) {
            seededConversationIdRef.current = conversationId;
            autoScrollRef.current = true;
            setMessages([...data.items].reverse());
            setPage(1);
            setHasOlder(data.meta?.hasNextPage ?? false);
        }
    }, [data, conversationId]);

    const handleLoadOlder = () => {
        const container = containerRef.current;
        const prevScrollHeight = container?.scrollHeight ?? 0;

        loadOlder(page + 1, {
            onSuccess: (older) => {
                autoScrollRef.current = false;
                setMessages((prev) => {
                    const existingIds = new Set(prev.map((m) => m.id));
                    const newlyLoaded = [...older.items].reverse().filter((m) => !existingIds.has(m.id));
                    return [...newlyLoaded, ...prev];
                });
                setPage((p) => p + 1);
                setHasOlder(older.meta?.hasNextPage ?? false);

                // Older messages were prepended above the viewport - keep the same messages in
                // view instead of letting the scroll position jump with the added height.
                requestAnimationFrame(() => {
                    if (container) container.scrollTop += container.scrollHeight - prevScrollHeight;
                });
            },
        });
    };

    useEffect(() => {
        markRead();
        // Only on mount/conversation change - mutate's identity isn't stable input here.
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [conversationId]);

    useEffect(() => {
        if (!socket) return;

        socket.emit("join_conversation", { conversationId });

        const handleNewMessage = (message: MessageSummary) => {
            if (message.conversationId !== conversationId) return;

            const isOwnMessage = message.senderId === currentUserId;
            // Your own messages always take you to the bottom; the other party's only do if
            // you're already there - otherwise you're reading history and shouldn't get yanked.
            const shouldAutoScroll = isOwnMessage || isNearBottom(containerRef.current);
            autoScrollRef.current = shouldAutoScroll;
            setHasNewMessageBelow(!shouldAutoScroll);

            setMessages((prev) => [...prev, message]);
            if (!isOwnMessage) markRead();
        };

        const handleError = (payload: { message?: string }) => {
            toast.error(getErrorMessage(new Error(payload?.message ?? ""), "A messaging error occurred."));
        };

        socket.on("new_message", handleNewMessage);
        socket.on("error", handleError);

        return () => {
            socket.emit("leave_conversation", { conversationId });
            socket.off("new_message", handleNewMessage);
            socket.off("error", handleError);
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [socket, conversationId]);

    useEffect(() => {
        if (autoScrollRef.current) bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages.length]);

    // Clears the "new message" indicator once you scroll down to it yourself, not just via the button.
    const handleScroll = () => {
        if (hasNewMessageBelow && isNearBottom(containerRef.current)) setHasNewMessageBelow(false);
    };

    const handleJumpToNewMessage = () => {
        setHasNewMessageBelow(false);
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    const handleSend = () => {
        const body = draft.trim();
        if (!body) return;

        if (!socket?.connected) {
            toast.error("Not connected. Please wait and try again.");
            return;
        }

        socket.emit("send_message", { conversationId, body });
        setDraft("");
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    if (isPending) {
        return (
            <div className="flex flex-1 min-h-0 items-center justify-center py-16">
                <Loader text="Loading messages. Please wait." />
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex flex-1 min-h-0 items-center justify-center py-16">
                <p className="text-error text-sm">{getErrorMessage(error, "Couldn't load messages. Please try again.")}</p>
            </div>
        );
    }

    return (
        <div className="flex flex-1 min-h-0 flex-col gap-4">
            <div className="relative flex-1 min-h-0">
                <div ref={containerRef} onScroll={handleScroll} className="h-full space-y-3 overflow-y-auto p-4">
                    {hasOlder && (
                        <div className="flex justify-center pb-1">
                            <Button variant="secondary" size="xs" onClick={handleLoadOlder} disabled={isLoadingOlder}>
                                {isLoadingOlder ? "Loading..." : "Load older messages"}
                            </Button>
                        </div>
                    )}
                    {messages.length === 0 ? (
                        <div className="flex flex-col items-center justify-center gap-2 py-8 text-center">
                            <MessageCircle className="size-5 text-foreground-tertiary" />
                            <p className="text-sm text-foreground-tertiary">No messages yet. Say hello!</p>
                        </div>
                    ) : (
                        messages.map((message) => {
                            const isOwn = message.senderId === currentUserId;
                            return (
                                <div key={message.id} className={cn("flex", isOwn ? "justify-end" : "justify-start")}>
                                    <div
                                        className={cn(
                                            "max-w-[75%] rounded-xl px-3.5 py-2 text-sm",
                                            isOwn ? "bg-accent text-accent-foreground" : "bg-background-tertiary text-foreground",
                                        )}
                                    >
                                        <p className="whitespace-pre-wrap break-words">{message.body}</p>
                                        <p className={cn("mt-1 text-[11px]", isOwn ? "text-accent-foreground/70" : "text-foreground-tertiary")}>
                                            {new Date(message.createdAt).toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" })}
                                        </p>
                                    </div>
                                </div>
                            );
                        })
                    )}
                    <div ref={bottomRef} />
                </div>

                {hasNewMessageBelow && (
                    <button
                        type="button"
                        onClick={handleJumpToNewMessage}
                        className="absolute inset-x-0 bottom-3 mx-auto flex w-fit items-center gap-1.5 rounded-full bg-accent px-3 py-1.5 text-xs font-medium text-accent-foreground shadow-md transition-colors hover:bg-accent/90"
                    >
                        <ArrowDown className="size-3.5" />
                        New message
                    </button>
                )}
            </div>

            <div className="flex shrink-0 items-end gap-2">
                <Textarea
                    placeholder="Type a message..."
                    rows={2}
                    maxLength={2000}
                    value={draft}
                    onChange={(e) => setDraft(e.target.value)}
                    onKeyDown={handleKeyDown}
                    className="flex-1 resize-none"
                />
                <Button
                    icon={<Send className="size-4" />}
                    iconOnly
                    onClick={handleSend}
                    disabled={!draft.trim()}
                    aria-label="Send message"
                />
            </div>
        </div>
    );
};

export default ConversationThread;
