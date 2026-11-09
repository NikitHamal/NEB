import type { ReactNode } from "react";
import { Inbox, AlertCircle } from "lucide-react";

const DefaultSkeleton = () => (
    <div className="h-24 animate-pulse rounded-lg border border-border bg-background-tertiary" />
);

interface ItemListProps<T> {
    items: T[];
    loading?: boolean;
    error?: string | null;
    renderItem: (item: T) => ReactNode;
    emptyMessage?: string;
    /** Overrides the default icon+message empty state, e.g. to add a CTA. */
    emptyState?: ReactNode;
    /** A single loading-state placeholder, repeated `skeletonCount` times. Defaults to a plain neutral shimmer block. */
    renderSkeleton?: () => ReactNode;
    skeletonCount?: number;
}

// Generic loading/error/empty/list handling for any paginated collection of cards -
// shared across resources, marketplace listings, and moderation queues. Domain-specific
// callers that want their own loading placeholder shape pass `renderSkeleton`.
const ItemList = <T,>({
    items,
    loading,
    error,
    renderItem,
    emptyMessage = "No items found.",
    emptyState,
    renderSkeleton,
    skeletonCount = 3,
}: ItemListProps<T>) => {
    if (loading) {
        const skeleton = renderSkeleton ?? (() => <DefaultSkeleton />);

        return (
            <div className="flex flex-col gap-4">
                {Array.from({ length: skeletonCount }).map((_, index) => (
                    <div key={index}>{skeleton()}</div>
                ))}
            </div>
        )
    }

    if (error) {
        return (
            <div className="flex flex-col items-center gap-2 rounded-lg border border-border py-16">
                <AlertCircle className="size-5 text-error" />
                <p className="text-error text-sm">{error}</p>
            </div>
        )
    }

    if (!items || items.length === 0) {
        return (
            <div className="flex flex-col items-center gap-2 rounded-lg border border-border py-16">
                {emptyState ?? (
                    <>
                        <Inbox className="size-5 text-foreground-tertiary" />
                        <p className="text-sm text-foreground-tertiary">{emptyMessage}</p>
                    </>
                )}
            </div>
        )
    }

    return (
        <div className="flex flex-col gap-4">
            {items.map((item, index) => (
                <div key={index}>
                    {renderItem(item)}
                </div>
            ))}
        </div>
    )
}

export default ItemList;
