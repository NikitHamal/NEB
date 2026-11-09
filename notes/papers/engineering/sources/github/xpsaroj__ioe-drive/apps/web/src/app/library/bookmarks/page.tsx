"use client"
import { Suspense } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft } from "lucide-react";

import { ResourceList, BookmarkedResourceCard } from "@/components/common/resources";
import { EntityPageStateHandler } from "@/components/layout";
import Button from "@/components/ui/Button";
import Pagination from "@/components/ui/Pagination";
import Loader from "@/components/ui/Loader";
import { useBookmarkedResources } from "@/hooks/queries/use-me";
import { usePageParam } from "@/hooks/use-page-param";

const MyBookmarkedResourcesContent = () => {
    const router = useRouter();
    const { page, setPage } = usePageParam();
    const { data, isPending, error, isPlaceholderData } = useBookmarkedResources(page);
    const bookmarkedResources = data?.items;

    // Reachable from more than one place, so a real back button beats assuming the breadcrumb's first crumb.
    const backButton = (
        <Button
            icon={<ChevronLeft className="size-4" />}
            iconOnly
            variant="ghost"
            size="xs"
            className="border border-border shrink-0"
            onClick={() => router.back()}
            aria-label="Go back"
        />
    );

    return (
        <EntityPageStateHandler
            title="My Bookmarked Resources"
            breadcrumbs={[{ label: "Library", href: "/library" }, { label: "Bookmarks" }]}
            beforeBreadcrumb={backButton}
            isPending={isPending}
            error={error}
            isEmpty={!bookmarkedResources || bookmarkedResources.length === 0}
            loaderText="Loading bookmarked resources. Please wait."
            emptyTitle="Oops. Looks like you haven't bookmarked any resources yet."
            emptyDescription="Click the bookmark icon on resources to save them for later. Once you bookmark resources, you'll be able to see them here."
            emptyButtonText="Explore Resources"
            emptyButtonHref="/resources"
        >
            <div className="space-y-6">
                <ResourceList
                    resources={bookmarkedResources || []}
                    renderItem={(item) => (
                        <BookmarkedResourceCard item={item} />
                    )}
                />
                <Pagination
                    page={page}
                    totalPages={data?.meta?.totalPages ?? 1}
                    onPageChange={setPage}
                    disabled={isPlaceholderData}
                />
            </div>
        </EntityPageStateHandler>
    )
}

const MyBookmarkedResourcesPage = () => {
    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading bookmarked resources. Please wait." />
            </div>
        }>
            <MyBookmarkedResourcesContent />
        </Suspense>
    );
}

export default MyBookmarkedResourcesPage;
