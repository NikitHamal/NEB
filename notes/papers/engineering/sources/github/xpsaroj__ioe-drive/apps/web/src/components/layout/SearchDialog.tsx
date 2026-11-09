"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Search, FileText, ImageOff, Loader2 } from "lucide-react";

import { useSearchSuggestions } from "@/hooks/queries/use-resources";
import { useSearchSubjects } from "@/hooks/queries/use-academics";
import { useListingSearchSuggestions } from "@/hooks/queries/use-marketplace";
import { useDebouncedValue } from "@/hooks/use-debounced-value";
import { SubjectCodeTile } from "@/components/common/offering";
import { TYPE_BADGE_COLOR } from "@/components/common/resources";
import { cn } from "@/utils/cn";
import { formatListingPrice } from "@/utils/marketplace";
import { ResourceTypeLabel, SemesterLabel, MarketplaceCategoryLabel } from "@/types/entities";

interface SearchDialogProps {
    isOpen: boolean;
    onClose: () => void;
}

const RESULT_LIMITS = { subjects: 5, resources: 8, listings: 5 };

// Lets ↑/↓/Enter move across subjects, resources, and listings as one flat sequence.
interface FlatItem {
    key: string;
    href: string;
}

const SearchDialog = ({ isOpen, onClose }: SearchDialogProps) => {
    const router = useRouter();
    const inputRef = useRef<HTMLInputElement>(null);
    const resultsRef = useRef<HTMLDivElement>(null);

    const [query, setQuery] = useState("");
    const [highlightedIndex, setHighlightedIndex] = useState(-1);
    const debouncedQuery = useDebouncedValue(query, 300);
    const trimmedQuery = debouncedQuery.trim();

    const { data: subjectsData, isFetching: subjectsFetching } = useSearchSubjects(debouncedQuery, 1, RESULT_LIMITS.subjects);
    const { data: resourceSuggestions, isFetching: resourcesFetching } = useSearchSuggestions(debouncedQuery, RESULT_LIMITS.resources);
    const { data: listingSuggestions, isFetching: listingsFetching } = useListingSearchSuggestions(debouncedQuery, RESULT_LIMITS.listings);
    const subjects = subjectsData?.items ?? [];
    const resources = resourceSuggestions ?? [];
    const listings = listingSuggestions ?? [];

    const flatItems: FlatItem[] = useMemo(() => [
        ...(subjectsData?.items ?? []).map((s): FlatItem => ({ key: `subject-${s.id}`, href: `/offerings/${s.id}` })),
        ...(resourceSuggestions ?? []).map((r): FlatItem => ({ key: `resource-${r.id}`, href: `/resources/r/${r.id}` })),
        ...(listingSuggestions ?? []).map((l): FlatItem => ({ key: `listing-${l.id}`, href: `/market/${l.id}` })),
    ], [subjectsData, resourceSuggestions, listingSuggestions]);

    // Reset the highlight during render (not an effect) per React's guidance for resetting on a value change.
    const [settledQuery, setSettledQuery] = useState(debouncedQuery);
    if (debouncedQuery !== settledQuery) {
        setSettledQuery(debouncedQuery);
        setHighlightedIndex(-1);
    }

    // Only ever mounted while open, so mount covers "opened" - no isOpen dependency needed.
    useEffect(() => {
        const id = requestAnimationFrame(() => inputRef.current?.focus());
        return () => cancelAnimationFrame(id);
    }, []);

    useEffect(() => {
        document.body.style.overflow = "hidden";
        return () => {
            document.body.style.overflow = "unset";
        };
    }, []);

    // Keeps a keyboard-highlighted row in view; `block: "nearest"` is a no-op if already visible.
    useEffect(() => {
        if (highlightedIndex < 0) return;
        resultsRef.current
            ?.querySelector(`[data-result-index="${highlightedIndex}"]`)
            ?.scrollIntoView({ block: "nearest" });
    }, [highlightedIndex]);

    const navigateTo = (href: string) => {
        onClose();
        router.push(href);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Escape") {
            onClose();
            return;
        }

        if (e.key === "ArrowDown") {
            e.preventDefault();
            setHighlightedIndex((i) => (i + 1 >= flatItems.length ? flatItems.length - 1 : i + 1));
            return;
        }

        if (e.key === "ArrowUp") {
            e.preventDefault();
            setHighlightedIndex((i) => (i - 1 < -1 ? -1 : i - 1));
            return;
        }

        if (e.key === "Enter") {
            e.preventDefault();
            const highlighted = flatItems[highlightedIndex];
            if (highlighted) {
                navigateTo(highlighted.href);
            } else if (trimmedQuery) {
                navigateTo(`/search?q=${encodeURIComponent(trimmedQuery)}`);
            }
        }
    };

    if (!isOpen) return null;

    const isSearching = subjectsFetching || resourcesFetching || listingsFetching;
    const hasQuery = trimmedQuery.length > 0;
    const hasResults = subjects.length > 0 || resources.length > 0 || listings.length > 0;

    return (
        <div
            className="fixed inset-0 z-100 flex items-start justify-center bg-black/70 p-4 pt-[12vh] backdrop-blur-sm animate-fade-in"
            onClick={(e) => e.target === e.currentTarget && onClose()}
        >
            <div className="w-full max-w-lg overflow-hidden rounded-lg border border-border bg-card-background shadow-xl animate-scale-in">
                <div className="flex items-center gap-3 border-b border-border px-4 py-3">
                    <Search className="size-4 shrink-0 text-foreground-tertiary" />
                    <input
                        ref={inputRef}
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Search resources, subjects, and listings..."
                        className="w-full bg-transparent text-sm text-foreground placeholder:text-foreground-tertiary focus:outline-none"
                    />
                    {isSearching && <Loader2 className="size-4 shrink-0 animate-spin text-foreground-tertiary" />}
                </div>

                <div ref={resultsRef} className="max-h-[60vh] overflow-y-auto p-2">
                    {!hasQuery ? (
                        <p className="px-3 py-6 text-center text-sm text-foreground-tertiary">
                            Start typing to search.
                        </p>
                    ) : !hasResults && !isSearching ? (
                        <p className="px-3 py-6 text-center text-sm text-foreground-tertiary">
                            No results for &ldquo;{trimmedQuery}&rdquo;.
                        </p>
                    ) : (
                        <>
                            {subjects.length > 0 && (
                                <div className="mb-1">
                                    <p className="px-3 pb-1 pt-2 font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">
                                        Subjects
                                    </p>
                                    {subjects.map((offering) => {
                                        const index = flatItems.findIndex((f) => f.key === `subject-${offering.id}`);
                                        return (
                                            <Link
                                                key={offering.id}
                                                href={`/offerings/${offering.id}`}
                                                onClick={onClose}
                                                onMouseEnter={() => setHighlightedIndex(index)}
                                                data-result-index={index}
                                                className={cn(
                                                    "flex items-center gap-3 rounded-md px-3 py-2 transition-colors",
                                                    index === highlightedIndex ? "bg-background-hover" : "hover:bg-background-hover"
                                                )}
                                            >
                                                <SubjectCodeTile code={offering.subject.code} size="sm" />
                                                <div className="min-w-0 flex-1">
                                                    <p className="truncate text-sm font-medium text-foreground">{offering.subject.name}</p>
                                                    <p className="truncate text-xs text-foreground-secondary">
                                                        {offering.subject.code}, {offering.program.code}, {SemesterLabel[offering.semester]} Semester
                                                    </p>
                                                </div>
                                            </Link>
                                        );
                                    })}
                                </div>
                            )}

                            {resources.length > 0 && (
                                <div className="mb-1">
                                    <p className="px-3 pb-1 pt-2 font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">
                                        Resources
                                    </p>
                                    {resources.map((resource) => {
                                        const index = flatItems.findIndex((f) => f.key === `resource-${resource.id}`);
                                        return (
                                            <Link
                                                key={resource.id}
                                                href={`/resources/r/${resource.id}`}
                                                onClick={onClose}
                                                onMouseEnter={() => setHighlightedIndex(index)}
                                                data-result-index={index}
                                                className={cn(
                                                    "flex items-center gap-3 rounded-md px-3 py-2 transition-colors",
                                                    index === highlightedIndex ? "bg-background-hover" : "hover:bg-background-hover"
                                                )}
                                            >
                                                <span className={`flex size-9 shrink-0 items-center justify-center rounded-md ${TYPE_BADGE_COLOR[resource.type].bg} ${TYPE_BADGE_COLOR[resource.type].text}`}>
                                                    <FileText className="size-4" />
                                                </span>
                                                <div className="min-w-0 flex-1">
                                                    <p className="truncate text-sm font-medium text-foreground">{resource.title}</p>
                                                    <p className="truncate text-xs text-foreground-secondary">
                                                        {resource.subjectCode}, {ResourceTypeLabel[resource.type]}
                                                    </p>
                                                </div>
                                            </Link>
                                        );
                                    })}
                                </div>
                            )}

                            {listings.length > 0 && (
                                <div>
                                    <p className="px-3 pb-1 pt-2 font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">
                                        Listings
                                    </p>
                                    {listings.map((listing) => {
                                        const index = flatItems.findIndex((f) => f.key === `listing-${listing.id}`);
                                        return (
                                            <Link
                                                key={listing.id}
                                                href={`/market/${listing.id}`}
                                                onClick={onClose}
                                                onMouseEnter={() => setHighlightedIndex(index)}
                                                data-result-index={index}
                                                className={cn(
                                                    "flex items-center gap-3 rounded-md px-3 py-2 transition-colors",
                                                    index === highlightedIndex ? "bg-background-hover" : "hover:bg-background-hover"
                                                )}
                                            >
                                                <span className="relative flex size-9 shrink-0 items-center justify-center overflow-hidden rounded-md bg-background-tertiary">
                                                    {listing.photoUrl ? (
                                                        // eslint-disable-next-line @next/next/no-img-element
                                                        <img src={listing.photoUrl} alt="" className="h-full w-full object-cover" />
                                                    ) : (
                                                        <ImageOff className="size-4 text-foreground-secondary" />
                                                    )}
                                                </span>
                                                <div className="min-w-0 flex-1">
                                                    <p className="truncate text-sm font-medium text-foreground">{listing.title}</p>
                                                    <p className="truncate text-xs text-foreground-secondary">
                                                        {MarketplaceCategoryLabel[listing.category]}, {formatListingPrice(listing.price)}
                                                    </p>
                                                </div>
                                            </Link>
                                        );
                                    })}
                                </div>
                            )}
                        </>
                    )}
                </div>

                {hasQuery && (
                    <button
                        type="button"
                        onClick={() => navigateTo(`/search?q=${encodeURIComponent(trimmedQuery)}`)}
                        className="flex w-full items-center justify-between border-t border-border px-4 py-2.5 text-xs text-foreground-secondary transition-colors hover:bg-background-hover hover:text-foreground cursor-pointer"
                    >
                        <span>View all results for &ldquo;{trimmedQuery}&rdquo;</span>
                        <span className="font-display uppercase tracking-wide">Enter</span>
                    </button>
                )}
            </div>
        </div>
    );
};

export default SearchDialog;
