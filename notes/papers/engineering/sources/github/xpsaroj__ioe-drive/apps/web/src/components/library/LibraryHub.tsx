"use client";
import Link from "next/link";
import { Bookmark, ChevronRight, File, History, ShoppingBag, UploadCloud } from "lucide-react";

import StatStrip from "@/components/ui/StatStrip";
import Button from "@/components/ui/Button";
import { JumpBackIn, ResourcePreviewTile } from "@/components/common/resources";
import { PreviewPanel } from "@/components/common/list";
import { BookSpines, DEFAULT_SHELF_SPINES } from "@/components/decor";
import { useRecentResources, useBookmarkedResources, useUploadedResources, useMyMarketplaceListings } from "@/hooks/queries/use-me";
import { getRelativeTime } from "@/utils/time";
import type { BookmarkedResourceItem } from "@/types/api";

// Trades ResourcePreviewTile's icon/bookmark/uploader detail for density in the narrow sidebar column.
const BookmarkListRow = ({ resourceId, title, subjectCode }: { resourceId: number; title: string; subjectCode?: string }) => (
    <Link
        href={`/resources/r/${resourceId}`}
        className="flex items-center gap-3 px-4 py-3 transition-colors hover:bg-background-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-inset"
    >
        <span className="flex size-8 shrink-0 items-center justify-center rounded-md bg-background-tertiary">
            <File className="size-3.5 text-foreground-secondary" />
        </span>
        <div className="min-w-0">
            <p className="text-sm font-medium text-foreground truncate">{title}</p>
            {subjectCode && <p className="text-xs text-foreground-secondary truncate">{subjectCode}</p>}
        </div>
    </Link>
);

const RecentlyBookmarkedPanel = ({ items }: { items: BookmarkedResourceItem[] }) => (
    <div>
        <div className="flex items-center justify-between gap-4 mb-6">
            <h3 className="text-lg font-semibold text-foreground">Recently Bookmarked</h3>
            <Button
                href="/library/bookmarks"
                variant="ghost"
                size="xs"
                icon={<ChevronRight className="size-3.5" />}
                iconPosition="right"
                className="text-foreground-secondary hover:text-foreground shrink-0"
            >
                View all
            </Button>
        </div>

        {items.length > 0 ? (
            <div className="rounded-lg border border-border bg-background-secondary divide-y divide-border">
                {items.map((item) => (
                    <BookmarkListRow
                        key={item.resourceId}
                        resourceId={item.resourceId}
                        title={item.resource.title}
                        subjectCode={item.resource.subjectOffering?.subject?.code}
                    />
                ))}
            </div>
        ) : (
            <div className="flex flex-col items-center justify-center gap-3 rounded-lg border border-dashed border-border py-10 text-center">
                <span className="flex size-10 items-center justify-center rounded-full bg-accent-soft text-accent">
                    <Bookmark className="size-5" />
                </span>
                <div>
                    <p className="text-sm font-medium text-foreground">Nothing bookmarked yet</p>
                    <p className="text-sm text-foreground-secondary mt-1">Save resources here to find them again quickly.</p>
                </div>
                <Button href="/resources" size="sm" variant="secondary">Browse resources</Button>
            </div>
        )}
    </div>
);

const LibraryHub = () => {
    const { data: recentResourcesData } = useRecentResources();
    const { data: bookmarkedResourcesData } = useBookmarkedResources();
    const { data: uploadedResourcesData } = useUploadedResources();
    const { data: myListingsData } = useMyMarketplaceListings();

    return (
        <div className="space-y-8">
            <div className="relative overflow-hidden rounded-lg border border-border bg-background-secondary p-6 sm:p-8">
                <BookSpines spines={DEFAULT_SHELF_SPINES} />

                <div className="relative z-10 space-y-2 max-w-md">
                    <p className="font-display text-xs tracking-[0.2em] uppercase text-foreground-tertiary">
                        Library
                    </p>
                    <h1 className="text-2xl md:text-3xl font-bold text-foreground">
                        My Library
                    </h1>
                    <p className="text-foreground-secondary text-base leading-relaxed">
                        Everything tied to you: recently viewed, bookmarked, and uploaded resources.
                    </p>
                </div>
            </div>

            <div className="pb-8 border-b border-border">
                <StatStrip
                    variant="cards"
                    className="sm:grid-cols-4"
                    items={[
                        { href: "/library/recent", label: "Recently viewed", value: recentResourcesData?.meta?.total, icon: History },
                        { href: "/library/bookmarks", label: "Bookmarked", value: bookmarkedResourcesData?.meta?.total, icon: Bookmark },
                        { href: "/library/uploads", label: "Uploaded", value: uploadedResourcesData?.meta?.total, icon: UploadCloud },
                        { href: "/library/marketplace", label: "Listings", value: myListingsData?.meta?.total, icon: ShoppingBag },
                    ]}
                />
            </div>

            {/* Stacked so a shorter Recently Bookmarked column never leaves a gap. */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 flex flex-col gap-8">
                    <JumpBackIn />

                    <PreviewPanel
                        title="My Uploads"
                        viewAllHref="/library/uploads"
                        emptyText="Nothing shared yet"
                        emptyDescription="Upload notes, past questions, or study guides for others to find."
                        emptyIcon={UploadCloud}
                        emptyAction={<Button href="/resources/share" size="sm" variant="secondary">Upload a resource</Button>}
                        columns={2}
                        tiles={(uploadedResourcesData?.items ?? []).slice(0, 2).map((item) => (
                            <ResourcePreviewTile
                                key={item.id}
                                resourceId={item.id}
                                title={item.title}
                                subjectCode={item.subjectOffering?.subject?.code}
                                type={item.type}
                                timeLabel={`Uploaded ${getRelativeTime(item.createdAt)}`}
                            />
                        ))}
                    />
                </div>

                <RecentlyBookmarkedPanel items={(bookmarkedResourcesData?.items ?? []).slice(0, 5)} />
            </div>
        </div>
    );
};

export default LibraryHub;
