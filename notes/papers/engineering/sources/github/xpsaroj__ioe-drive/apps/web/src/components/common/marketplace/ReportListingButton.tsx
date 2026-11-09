"use client";
import { useState } from "react";
import { toast } from "sonner";
import { Flag } from "lucide-react";

import Button from "@/components/ui/Button";
import { ModerationActionModal } from "@/components/common/moderation";
import { useReportListing } from "@/hooks/queries/use-marketplace";
import { getErrorMessage } from "@/lib/errors";
import { MarketplaceReportReason, MarketplaceReportReasonLabel } from "@/types/entities";
import type { MarketplaceReportReasonInput } from "@/lib/validators/marketplace";

const REASON_OPTIONS = Object.values(MarketplaceReportReason).map((reason) => ({
    value: reason,
    label: MarketplaceReportReasonLabel[reason],
}));

interface ReportListingButtonProps {
    listingId: number;
}

// Mutually exclusive with ListingModeratorActionBar, whose bar style this matches - a viewer sees exactly one.
const ReportListingButton = ({ listingId }: ReportListingButtonProps) => {
    const [isOpen, setIsOpen] = useState(false);
    const { mutate, isPending } = useReportListing(listingId);

    const handleSubmit = (data: { reason: string; note?: string }) => {
        mutate(data as MarketplaceReportReasonInput, {
            onSuccess: () => {
                toast.success("Thanks - we've received your report.");
                setIsOpen(false);
            },
            onError: (error) => toast.error(getErrorMessage(error, "Couldn't submit your report. Please try again.")),
        });
    };

    return (
        <div className="flex flex-col gap-3 rounded-lg border border-border p-4 sm:flex-row sm:items-center sm:justify-between">
            <p className="text-sm text-foreground-secondary">
                Found something misleading or inappropriate about this listing?
            </p>
            <Button
                variant="secondary"
                size="sm"
                icon={<Flag className="size-4" />}
                onClick={() => setIsOpen(true)}
                className="shrink-0"
            >
                Report
            </Button>

            <ModerationActionModal
                isOpen={isOpen}
                onClose={() => setIsOpen(false)}
                title="Report Listing"
                description="Let a moderator know what's wrong with this listing. Your identity isn't shared with its poster."
                submitLabel="Submit Report"
                isSubmitting={isPending}
                reasonOptions={REASON_OPTIONS}
                onSubmit={handleSubmit}
            />
        </div>
    );
};

export default ReportListingButton;
