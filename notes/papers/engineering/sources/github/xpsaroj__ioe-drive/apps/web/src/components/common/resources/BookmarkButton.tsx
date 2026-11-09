"use client";
import { Bookmark } from "lucide-react";
import { toast } from "sonner";

import Button from "@/components/ui/Button";
import { useMe, useBookmarkedResourceIds, useBookmarkResource, useUnbookmarkResource } from "@/hooks/queries/use-me";
import { getErrorMessage } from "@/lib/errors";

interface BookmarkButtonProps {
    resourceId: number;
    /** Labeled "Save"/"Saved" button instead of icon-only, for prominent placements. */
    showLabel?: boolean;
}

const BookmarkButton = ({ resourceId, showLabel = false }: BookmarkButtonProps) => {
    const { data: userData } = useMe();
    const { data: bookmarkedIds } = useBookmarkedResourceIds();
    const { mutate: bookmark, isPending: isBookmarking } = useBookmarkResource();
    const { mutate: unbookmark, isPending: isUnbookmarking } = useUnbookmarkResource();

    // Guests never see the button at all, rather than a disabled/dead one.
    if (!userData) return null;

    const isBookmarked = !!bookmarkedIds?.includes(resourceId);

    const handleToggle = () => {
        const idAsString = String(resourceId);

        if (isBookmarked) {
            unbookmark(idAsString, {
                onSuccess: () => {
                    toast.success("Bookmark removed.");
                },
                onError: (error) => {
                    toast.error(getErrorMessage(error, "Couldn't remove the bookmark. Please try again."));
                },
            });
        } else {
            bookmark(idAsString, {
                onSuccess: () => {
                    toast.success("Resource bookmarked.");
                },
                onError: (error) => {
                    toast.error(getErrorMessage(error, "Couldn't bookmark the resource. Please try again."));
                },
            });
        }
    };

    if (showLabel) {
        return (
            <Button
                variant="secondary"
                size="md"
                icon={<Bookmark className="size-4" fill={isBookmarked ? "currentColor" : "none"} />}
                onClick={handleToggle}
                disabled={isBookmarking || isUnbookmarking}
                className={isBookmarked ? "text-info border-info/40 hover:text-info" : ""}
            >
                {isBookmarked ? "Saved" : "Save"}
            </Button>
        );
    }

    return (
        <Button
            variant="ghost"
            size="xs"
            iconOnly
            icon={<Bookmark className="size-4" fill={isBookmarked ? "currentColor" : "none"} />}
            onClick={handleToggle}
            disabled={isBookmarking || isUnbookmarking}
            className={isBookmarked ? "text-info hover:text-info hover:bg-info/10" : "text-foreground-secondary hover:text-info hover:bg-info/10"}
            aria-label={isBookmarked ? "Remove bookmark" : "Bookmark resource"}
        />
    );
};

export default BookmarkButton;
