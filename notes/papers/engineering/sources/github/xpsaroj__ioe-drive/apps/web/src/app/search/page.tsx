"use client"
import { Suspense } from "react";
import { useRouter, usePathname, useSearchParams } from "next/navigation";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import { Breadcrumbs } from "@/components/layout";
import { ItemList } from "@/components/common/list";
import { ResourceList, ResourceCard } from "@/components/common/resources";
import { MarketplaceListingCard } from "@/components/common/marketplace";
import { SubjectCodeTile } from "@/components/common/offering";
import Button from "@/components/ui/Button";
import Pagination from "@/components/ui/Pagination";
import Loader from "@/components/ui/Loader";
import { getErrorMessage } from "@/lib/errors";
import { useSearchResources } from "@/hooks/queries/use-resources";
import { useSearchSubjects } from "@/hooks/queries/use-academics";
import { useListings } from "@/hooks/queries/use-marketplace";
import { usePageParam } from "@/hooks/use-page-param";
import { cn } from "@/utils/cn";
import { SemesterLabel } from "@/types/entities";

const SUBJECT_RESULTS_SHOWN = 6;

type ResultTab = "resources" | "listings";

const SearchContent = () => {
    const router = useRouter();
    const pathname = usePathname();
    const searchParams = useSearchParams();
    const q = searchParams.get("q")?.trim() ?? "";

    const activeTab: ResultTab = searchParams.get("tab") === "listings" ? "listings" : "resources";
    const setActiveTab = (tab: ResultTab) => {
        const params = new URLSearchParams(searchParams.toString());
        if (tab === "resources") params.delete("tab");
        else params.set("tab", tab);
        router.replace(`${pathname}?${params.toString()}`);
    };

    // Independent page params so switching tabs never disturbs the other tab's pagination.
    const { page: resourcesPage, setPage: setResourcesPage } = usePageParam("resourcesPage");
    const { page: listingsPage, setPage: setListingsPage } = usePageParam("listingsPage");

    const { data: subjectsData, isPending: subjectsPending } = useSearchSubjects(q, 1, SUBJECT_RESULTS_SHOWN);
    const {
        data: resourcesData,
        isLoading: resourcesLoading,
        error: resourcesError,
        isPlaceholderData: resourcesPlaceholder,
    } = useSearchResources(q, resourcesPage);
    const {
        data: listingsData,
        isPending: listingsPending,
        error: listingsError,
        isPlaceholderData: listingsPlaceholder,
    } = useListings({ q }, listingsPage);

    const subjects = subjectsData?.items ?? [];
    const resources = resourcesData?.items ?? [];
    const listings = listingsData?.items ?? [];

    const tabs: { key: ResultTab; label: string; count?: number }[] = [
        { key: "resources", label: "Resources", count: resourcesData?.meta?.total },
        { key: "listings", label: "Listings", count: listingsData?.meta?.total },
    ];

    return (
        <div className="min-h-screen bg-background text-foreground max-w-7xl mx-auto md:px-8 px-6 md:py-8 py-6 space-y-8">
            <div className="sticky top-0 z-10 flex items-center gap-2 border-b border-border bg-background/95 py-2.5 backdrop-blur-sm">
                <Button
                    icon={<ChevronLeft className="size-4" />}
                    iconOnly
                    variant="ghost"
                    size="xs"
                    className="border border-border shrink-0"
                    onClick={() => router.back()}
                    aria-label="Go back"
                />
                <Breadcrumbs items={[{ label: "Dashboard", href: "/dashboard" }, { label: "Search" }]} />
            </div>

            <div className="pb-6 border-b border-border">
                <h1 className="text-2xl md:text-3xl font-bold text-foreground">
                    {q ? <>Results for &ldquo;{q}&rdquo;</> : "Search"}
                </h1>
                <p className="text-foreground-secondary mt-1">
                    {q ? "Subjects, resources, and listings matching your search." : "Enter a search term to get started."}
                </p>
            </div>

            {q && (
                <div className="space-y-8">
                    {!subjectsPending && subjects.length > 0 && (
                        <div className="space-y-3">
                            <h2 className="text-lg font-semibold text-foreground">Subjects</h2>
                            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
                                {subjects.map((offering) => (
                                    <Link
                                        key={offering.id}
                                        href={`/offerings/${offering.id}`}
                                        className="flex items-center gap-3 rounded-lg border border-border p-4 transition-colors hover:border-accent hover:bg-background-hover"
                                    >
                                        <SubjectCodeTile code={offering.subject.code} size="md" />
                                        <div className="min-w-0">
                                            <p className="truncate font-semibold text-foreground">{offering.subject.name}</p>
                                            <p className="truncate text-xs text-foreground-secondary">
                                                {offering.subject.code}, {offering.program.code}, {SemesterLabel[offering.semester]} Semester
                                            </p>
                                        </div>
                                    </Link>
                                ))}
                            </div>
                        </div>
                    )}

                    <div className="space-y-6">
                        {/* Docks directly below the breadcrumb bar above (top-0, 45px tall) once scrolled past. */}
                        <div className="sticky top-[45px] z-10 flex gap-1 border-b border-border bg-background/95 backdrop-blur-sm">
                            {tabs.map((tab) => (
                                <button
                                    key={tab.key}
                                    type="button"
                                    onClick={() => setActiveTab(tab.key)}
                                    className={cn(
                                        "px-4 py-2 -mb-px border-b-2 text-sm font-medium transition-colors",
                                        activeTab === tab.key
                                            ? "border-foreground text-foreground"
                                            : "border-transparent text-foreground-secondary hover:text-foreground"
                                    )}
                                >
                                    {tab.label}{tab.count !== undefined ? ` (${tab.count})` : ""}
                                </button>
                            ))}
                        </div>

                        {activeTab === "resources" ? (
                            <div className="space-y-6">
                                <ResourceList
                                    resources={resources}
                                    loading={resourcesLoading}
                                    error={resourcesError ? getErrorMessage(resourcesError, "Couldn't load search results. Please try again.") : null}
                                    renderItem={(resource) => <ResourceCard resource={resource} />}
                                    emptyMessage={`No resources found for "${q}".`}
                                />
                                <Pagination
                                    page={resourcesPage}
                                    totalPages={resourcesData?.meta?.totalPages ?? 1}
                                    onPageChange={setResourcesPage}
                                    disabled={resourcesPlaceholder}
                                />
                            </div>
                        ) : (
                            <div className="space-y-6">
                                <ItemList
                                    items={listings}
                                    loading={listingsPending}
                                    error={listingsError ? getErrorMessage(listingsError, "Couldn't load search results. Please try again.") : null}
                                    renderItem={(listing) => <MarketplaceListingCard listing={listing} />}
                                    emptyMessage={`No listings found for "${q}".`}
                                />
                                <Pagination
                                    page={listingsPage}
                                    totalPages={listingsData?.meta?.totalPages ?? 1}
                                    onPageChange={setListingsPage}
                                    disabled={listingsPlaceholder}
                                />
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

const SearchPage = () => {
    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading search results. Please wait." />
            </div>
        }>
            <SearchContent />
        </Suspense>
    );
};

export default SearchPage;
