"use client";
import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { Bell, CheckCheck } from "lucide-react";

import Button from "@/components/ui/Button";
import {
    useNotifications,
    useUnreadNotificationsCount,
    useMarkNotificationRead,
    useMarkAllNotificationsRead,
} from "@/hooks/queries/use-notifications";
import { getRelativeTime } from "@/utils/time";
import { cn } from "@/utils/cn";
import type { NotificationSummary } from "@/types/api";

interface PanelPosition {
    top: number;
    left: number;
}

// Matches the panel's own `w-80` class below.
const PANEL_WIDTH = 320;
const VIEWPORT_MARGIN = 12;

const NotificationsBell = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [panelPosition, setPanelPosition] = useState<PanelPosition | null>(null);
    const containerRef = useRef<HTMLDivElement>(null);

    const { data: unreadData } = useUnreadNotificationsCount();
    const { data, isPending } = useNotifications(1, isOpen);
    const { mutate: markRead } = useMarkNotificationRead();
    const { mutate: markAllRead, isPending: isMarkingAllRead } = useMarkAllNotificationsRead();

    const unreadCount = unreadData?.unreadCount ?? 0;
    const notifications = data?.items ?? [];

    const handleToggle = () => {
        if (!isOpen && containerRef.current) {
            const rect = containerRef.current.getBoundingClientRect();

            const left = Math.min(
                Math.max(rect.left, VIEWPORT_MARGIN),
                window.innerWidth - PANEL_WIDTH - VIEWPORT_MARGIN,
            );
            setPanelPosition({ top: rect.bottom + 8, left });
        }
        setIsOpen((open) => !open);
    };

    useEffect(() => {
        if (!isOpen) return;

        const handleClickOutside = (event: MouseEvent) => {
            if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };

        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, [isOpen]);

    const handleItemClick = (notification: NotificationSummary) => {
        if (!notification.isRead) markRead(notification.id);
        setIsOpen(false);
    };

    return (
        <div ref={containerRef} className="relative">
            <Button
                variant={ isOpen ? "secondary" : "ghost"}
                size="sm"
                iconOnly
                aria-label="Notifications"
                onClick={handleToggle}
                icon={<Bell className="size-5" />}
            />
            {!!unreadCount && (
                <span className="pointer-events-none absolute -top-1 -right-1 flex min-w-5 items-center justify-center rounded-full bg-accent px-1.5 py-0.5 text-[11px] font-semibold text-accent-foreground">
                    {unreadCount}
                </span>
            )}

            {isOpen && panelPosition && (
                <div
                    style={{ top: panelPosition.top, left: panelPosition.left }}
                    className="fixed z-50 w-80 rounded-lg border border-border bg-card-background shadow-xl animate-scale-in"
                >
                    <div className="flex items-center justify-between border-b border-border px-4 py-3">
                        <p className="text-sm font-semibold text-foreground">Notifications</p>
                        {unreadCount > 0 && (
                            <Button
                                variant="ghost"
                                size="xs"
                                icon={<CheckCheck className="size-3.5" />}
                                onClick={() => markAllRead()}
                                disabled={isMarkingAllRead}
                            >
                                Mark all read
                            </Button>
                        )}
                    </div>

                    <div className="max-h-96 overflow-y-auto">
                        {isPending ? (
                            <div className="flex items-center justify-center py-8">
                                <div className="size-5 animate-spin rounded-full border-2 border-foreground-secondary border-t-foreground" />
                            </div>
                        ) : notifications.length === 0 ? (
                            <div className="flex flex-col items-center justify-center gap-2 px-4 py-10 text-center">
                                <Bell className="size-5 text-foreground-tertiary" />
                                <p className="text-sm text-foreground-tertiary">No notifications yet.</p>
                            </div>
                        ) : (
                            <div className="divide-y divide-border">
                                {notifications.map((notification) => (
                                    <Link
                                        key={notification.id}
                                        href={notification.link ?? "#"}
                                        onClick={() => handleItemClick(notification)}
                                        className={cn(
                                            "block px-4 py-3 text-sm transition-colors hover:bg-background-hover",
                                            !notification.isRead && "bg-accent-soft"
                                        )}
                                    >
                                        <p className={cn("text-foreground", !notification.isRead && "font-medium")}>
                                            {notification.message}
                                        </p>
                                        <p className="mt-1 text-xs text-foreground-tertiary">
                                            {getRelativeTime(notification.createdAt)}
                                        </p>
                                    </Link>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default NotificationsBell;
