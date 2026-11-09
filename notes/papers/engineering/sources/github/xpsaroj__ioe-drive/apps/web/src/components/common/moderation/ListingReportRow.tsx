"use client";
import Link from "next/link";
import { toast } from "sonner";

import Button from "@/components/ui/Button";
import { useDismissListingReport } from "@/hooks/queries/use-moderation";
import { getErrorMessage } from "@/lib/errors";
import { MarketplaceReportReasonLabel } from "@/types/entities";
import type { ListingReportItem } from "@/types/api";

interface ListingReportRowProps {
    report: ListingReportItem;
}

// Reporter's identity shows here (moderator-only view), never on any poster- or public-facing surface.
const ListingReportRow = ({ report }: ListingReportRowProps) => {
    const { mutate: dismiss, isPending } = useDismissListingReport();

    const handleDismiss = () => {
        dismiss(report.id, {
            onSuccess: () => toast.success("Report dismissed."),
            onError: (error) => toast.error(getErrorMessage(error, "Couldn't dismiss the report. Please try again.")),
        });
    };

    return (
        <div className="flex flex-col gap-3 rounded-lg border border-border p-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="min-w-0 space-y-1">
                <Link href={`/market/${report.listingId}`} className="font-semibold text-foreground hover:underline">
                    {report.listing.title}
                </Link>
                <p className="text-xs text-foreground-secondary">
                    Reported by {report.reporter.fullName}
                </p>
                <p className="text-sm text-foreground-secondary">
                    <span className="font-medium text-foreground">{MarketplaceReportReasonLabel[report.reason]}</span>
                    {report.note && <span> &mdash; {report.note}</span>}
                </p>
            </div>

            <div className="flex items-center gap-2 shrink-0">
                <Button href={`/market/${report.listingId}`} variant="secondary" size="sm">
                    Review
                </Button>
                <Button variant="ghost" size="sm" onClick={handleDismiss} disabled={isPending}>
                    {isPending ? "Dismissing..." : "Dismiss"}
                </Button>
            </div>
        </div>
    );
};

export default ListingReportRow;
