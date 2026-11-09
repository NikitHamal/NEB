import { ChevronRight, Inbox, type LucideIcon } from "lucide-react";

import Button from "@/components/ui/Button";

interface PreviewPanelProps {
    title: string;
    viewAllHref: string;
    tiles: React.ReactNode[];
    emptyText: string;
    emptyDescription?: string;
    emptyIcon?: LucideIcon;
    emptyAction?: React.ReactNode;
    /** Grid columns at the sm breakpoint - 2 for the narrower column, 3 for full-width. */
    columns?: 2 | 3;
}

// Generic "title + View all link + a small grid of preview tiles" panel - shared across
// hub-style pages (LibraryHub, a user's profile) that preview a few items from a larger
// list living on its own dedicated page, rather than embedding the full paginated list.
const PreviewPanel = ({ title, viewAllHref, tiles, emptyText, emptyDescription, emptyIcon: EmptyIcon = Inbox, emptyAction, columns = 3 }: PreviewPanelProps) => (
    <div>
        <div className="flex items-center justify-between gap-4 mb-6">
            <h3 className="text-lg font-semibold text-foreground">{title}</h3>
            <Button
                href={viewAllHref}
                variant="ghost"
                size="xs"
                icon={<ChevronRight className="size-3.5" />}
                iconPosition="right"
                className="text-foreground-secondary hover:text-foreground shrink-0"
            >
                View all
            </Button>
        </div>

        {tiles.length > 0 ? (
            <div className={columns === 2 ? "grid grid-cols-1 sm:grid-cols-2 gap-4" : "grid grid-cols-1 sm:grid-cols-3 gap-4"}>
                {tiles}
            </div>
        ) : (
            <div className="flex flex-col items-center justify-center gap-3 rounded-lg border border-dashed border-border py-10 text-center">
                <span className="flex size-10 items-center justify-center rounded-full bg-accent-soft text-accent">
                    <EmptyIcon className="size-5" />
                </span>
                <div>
                    <p className="text-sm font-medium text-foreground">{emptyText}</p>
                    {emptyDescription && <p className="text-sm text-foreground-secondary mt-1">{emptyDescription}</p>}
                </div>
                {emptyAction}
            </div>
        )}
    </div>
);

export default PreviewPanel;
