"use client"
import { Suspense } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft } from "lucide-react";

import { EntityPageStateHandler } from "@/components/layout";
import { ItemList } from "@/components/common/list";
import { MyListingCard } from "@/components/common/marketplace";
import Button from "@/components/ui/Button";
import Pagination from "@/components/ui/Pagination";
import Loader from "@/components/ui/Loader";
import { useMyMarketplaceListings } from "@/hooks/queries/use-me";
import { usePageParam } from "@/hooks/use-page-param";

const MyListingsContent = () => {
    const router = useRouter();
    const { page, setPage } = usePageParam();
    const { data, isPending, error, isPlaceholderData } = useMyMarketplaceListings(page);
    const listings = data?.items;

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
            title="My Listings"
            breadcrumbs={[{ label: "Library", href: "/library" }, { label: "Listings" }]}
            beforeBreadcrumb={backButton}
            isPending={isPending}
            error={error}
            isEmpty={!listings || listings.length === 0}
            loaderText="Loading your listings. Please wait."
            emptyTitle="You haven't posted any listings yet."
            emptyDescription="Post something for sale, or something you're looking for, and it'll show up here - including fulfilled listings, which are hidden from the public browse page."
            emptyButtonText="Post a Listing"
            emptyButtonHref="/market/create"
        >
            <div className="space-y-6">
                <ItemList
                    items={listings || []}
                    renderItem={(item) => <MyListingCard listing={item} />}
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

const MyListingsPage = () => {
    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading your listings. Please wait." />
            </div>
        }>
            <MyListingsContent />
        </Suspense>
    );
}

export default MyListingsPage;
