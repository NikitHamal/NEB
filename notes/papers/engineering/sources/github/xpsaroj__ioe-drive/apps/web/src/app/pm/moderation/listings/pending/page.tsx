"use client";
import { Suspense } from "react";

import { ItemList } from "@/components/common/list";
import { MarketplaceListingCard } from "@/components/common/marketplace";
import Loader from "@/components/ui/Loader";
import Pagination from "@/components/ui/Pagination";
import { usePendingListings } from "@/hooks/queries/use-moderation";
import { getErrorMessage } from "@/lib/errors";
import { usePageParam } from "@/hooks/use-page-param";

const PendingListingsQueueContent = () => {
    const { page, setPage } = usePageParam();
    const { data, isPending, error, isPlaceholderData } = usePendingListings(page);

    return (
        <div className="space-y-6">
            <ItemList
                items={data?.items || []}
                loading={isPending}
                error={error ? getErrorMessage(error, "Couldn't load pending listings. Please try again.") : null}
                emptyMessage="Nothing waiting for review - every posted listing has been reviewed."
                renderItem={(item) => <MarketplaceListingCard listing={item} />}
            />
            <Pagination
                page={page}
                totalPages={data?.meta?.totalPages ?? 1}
                onPageChange={setPage}
                disabled={isPlaceholderData}
            />
        </div>
    );
};

const PendingListingsQueuePage = () => (
    <Suspense fallback={
        <div className="flex items-center justify-center py-16">
            <Loader text="Loading pending listings. Please wait." />
        </div>
    }>
        <PendingListingsQueueContent />
    </Suspense>
);

export default PendingListingsQueuePage;
