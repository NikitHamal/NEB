"use client";
import { Suspense } from "react";

import { ItemList } from "@/components/common/list";
import { ListingReportRow } from "@/components/common/moderation";
import Loader from "@/components/ui/Loader";
import Pagination from "@/components/ui/Pagination";
import { useListingReports } from "@/hooks/queries/use-moderation";
import { getErrorMessage } from "@/lib/errors";
import { usePageParam } from "@/hooks/use-page-param";

const ListingReportsQueueContent = () => {
    const { page, setPage } = usePageParam();
    const { data, isPending, error, isPlaceholderData } = useListingReports(page);

    return (
        <div className="space-y-6">
            <ItemList
                items={data?.items || []}
                loading={isPending}
                error={error ? getErrorMessage(error, "Couldn't load reports. Please try again.") : null}
                emptyMessage="No open reports - every reported listing has been reviewed."
                renderItem={(report) => <ListingReportRow report={report} />}
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

const ListingReportsQueuePage = () => (
    <Suspense fallback={
        <div className="flex items-center justify-center py-16">
            <Loader text="Loading reports. Please wait." />
        </div>
    }>
        <ListingReportsQueueContent />
    </Suspense>
);

export default ListingReportsQueuePage;
