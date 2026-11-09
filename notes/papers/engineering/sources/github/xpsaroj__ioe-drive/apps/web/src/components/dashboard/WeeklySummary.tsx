"use client";
import { Share2, Eye, Bookmark } from "lucide-react";

import { useWeeklySummary } from "@/hooks/queries/use-me";

const WeeklySummary = () => {
    const { data, isPending } = useWeeklySummary();

    const stats = [
        { icon: Share2, label: "Resources Shared", value: data?.resourcesShared, bg: "bg-tag-blue-bg", text: "text-tag-blue-text" },
        { icon: Eye, label: "Resources Viewed", value: data?.resourcesViewed, bg: "bg-tag-teal-bg", text: "text-tag-teal-text" },
        { icon: Bookmark, label: "Resources Bookmarked", value: data?.resourcesBookmarked, bg: "bg-tag-clay-bg", text: "text-tag-clay-text" },
    ];

    return (
        <div className="h-full flex flex-col">
            <h2 className="text-lg font-semibold text-foreground mb-6">This Week</h2>
            {/* flex-1 matches Jump Back In's card height on desktop; no-op once stacked on mobile. */}
            <div className="flex-1 flex flex-col rounded-lg border border-border bg-background-secondary divide-y divide-border">
                {stats.map(({ icon: Icon, label, value, bg, text }) => (
                    <div key={label} className="flex-1 flex items-center justify-between gap-3 px-4 py-4">
                        <div className="flex items-center gap-3 text-sm text-foreground-secondary">
                            <span className={`flex size-8 shrink-0 items-center justify-center rounded-full ${bg} ${text}`}>
                                <Icon className="size-4" />
                            </span>
                            {label}
                        </div>
                        {isPending ? (
                            <div className="h-5 w-6 animate-pulse rounded bg-skeleton-base" />
                        ) : (
                            <span className="text-base font-semibold text-foreground">{value ?? 0}</span>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default WeeklySummary;
