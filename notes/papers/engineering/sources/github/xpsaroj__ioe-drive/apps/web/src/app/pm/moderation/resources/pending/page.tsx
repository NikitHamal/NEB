"use client";
import { Suspense } from "react";

import { ResourceList, UploadedResourceCard } from "@/components/common/resources";
import Loader from "@/components/ui/Loader";
import Pagination from "@/components/ui/Pagination";
import { usePendingResources } from "@/hooks/queries/use-moderation";
import { getErrorMessage } from "@/lib/errors";
import { usePageParam } from "@/hooks/use-page-param";

const PendingQueueContent = () => {
    const { page, setPage } = usePageParam();
    const { data, isPending, error, isPlaceholderData } = usePendingResources(page);

    return (
        <div className="space-y-6">
            <ResourceList
                resources={data?.items || []}
                loading={isPending}
                error={error ? getErrorMessage(error, "Couldn't load pending resources. Please try again.") : null}
                emptyMessage="Nothing waiting for review - every uploaded resource has been reviewed."
                renderItem={(item) => <UploadedResourceCard item={item} />}
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

const PendingQueuePage = () => (
    <Suspense fallback={
        <div className="flex items-center justify-center py-16">
            <Loader text="Loading pending resources. Please wait." />
        </div>
    }>
        <PendingQueueContent />
    </Suspense>
);

export default PendingQueuePage;
