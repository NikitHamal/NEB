"use client";
import { Suspense } from "react";

import { ResourceList } from "@/components/common/resources";
import { ResourceReportRow } from "@/components/common/moderation";
import Loader from "@/components/ui/Loader";
import Pagination from "@/components/ui/Pagination";
import { useResourceReports } from "@/hooks/queries/use-moderation";
import { getErrorMessage } from "@/lib/errors";
import { usePageParam } from "@/hooks/use-page-param";

const ReportsQueueContent = () => {
    const { page, setPage } = usePageParam();
    const { data, isPending, error, isPlaceholderData } = useResourceReports(page);

    return (
        <div className="space-y-6">
            <ResourceList
                resources={data?.items || []}
                loading={isPending}
                error={error ? getErrorMessage(error, "Couldn't load reports. Please try again.") : null}
                emptyMessage="No open reports - every reported resource has been reviewed."
                renderItem={(report) => <ResourceReportRow report={report} />}
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

const ReportsQueuePage = () => (
    <Suspense fallback={
        <div className="flex items-center justify-center py-16">
            <Loader text="Loading reports. Please wait." />
        </div>
    }>
        <ReportsQueueContent />
    </Suspense>
);

export default ReportsQueuePage;
