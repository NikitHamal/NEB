import { ChevronLeft, ChevronRight } from "lucide-react";

import Button from "@/components/ui/Button";
import { cn } from "@/utils/cn";

interface PaginationProps {
    page: number;
    totalPages: number;
    onPageChange: (page: number) => void;
    /** Disable page-change controls, e.g. while TanStack Query's isPlaceholderData is true. */
    disabled?: boolean;
    className?: string;
}

const ELLIPSIS = "ellipsis" as const;

// E.g. page=5, totalPages=10 -> [1, ellipsis, 4, 5, 6, ellipsis, 10].
const getPageNumbers = (page: number, totalPages: number): (number | typeof ELLIPSIS)[] => {
    const pages: (number | typeof ELLIPSIS)[] = [];
    const windowStart = Math.max(2, page - 1);
    const windowEnd = Math.min(totalPages - 1, page + 1);

    pages.push(1);
    if (windowStart > 2) pages.push(ELLIPSIS);
    for (let p = windowStart; p <= windowEnd; p++) pages.push(p);
    if (windowEnd < totalPages - 1) pages.push(ELLIPSIS);
    if (totalPages > 1) pages.push(totalPages);

    return pages;
};

// Shared across every paginated list page.
const Pagination = ({ page, totalPages, onPageChange, disabled, className }: PaginationProps) => {
    if (totalPages <= 1) return null;

    const pageNumbers = getPageNumbers(page, totalPages);

    return (
        <nav
            aria-label="Pagination"
            className={cn("flex items-center justify-center gap-1", className)}
        >
            <Button
                variant="ghost"
                size="sm"
                iconOnly
                aria-label="Previous page"
                icon={<ChevronLeft className="size-4" />}
                disabled={disabled || page <= 1}
                onClick={() => onPageChange(page - 1)}
            />

            {pageNumbers.map((entry, index) =>
                entry === ELLIPSIS ? (
                    <span
                        key={`ellipsis-${index}`}
                        className="px-1.5 text-sm text-foreground-tertiary select-none"
                    >
                        &hellip;
                    </span>
                ) : (
                    <Button
                        key={entry}
                        variant={entry === page ? "primary" : "ghost"}
                        size="sm"
                        aria-label={`Page ${entry}`}
                        aria-current={entry === page ? "page" : undefined}
                        disabled={disabled}
                        onClick={() => onPageChange(entry)}
                    >
                        {entry}
                    </Button>
                )
            )}

            <Button
                variant="ghost"
                size="sm"
                iconOnly
                aria-label="Next page"
                icon={<ChevronRight className="size-4" />}
                disabled={disabled || page >= totalPages}
                onClick={() => onPageChange(page + 1)}
            />
        </nav>
    );
};

export default Pagination;
