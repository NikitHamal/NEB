"use client";
import { useState } from "react";
import { toast } from "sonner";
import { Check, ShieldOff, X } from "lucide-react";

import Button from "@/components/ui/Button";
import { ModerationActionModal } from "@/components/common/moderation";
import {
    useApproveListingAsModerator,
    useRejectListingAsModerator,
    useRemoveListingAsModerator,
} from "@/hooks/queries/use-marketplace";
import { MarketplaceListingStatus, MarketplaceReportReason, MarketplaceReportReasonLabel } from "@/types/entities";
import { getErrorMessage } from "@/lib/errors";
import type { MarketplaceReportReasonInput } from "@/lib/validators/marketplace";

const REASON_OPTIONS = Object.values(MarketplaceReportReason).map((reason) => ({
    value: reason,
    label: MarketplaceReportReasonLabel[reason],
}));

interface ListingModeratorActionBarProps {
    listingId: number;
    status: MarketplaceListingStatus;
}

// Which actions show depends on status: only PENDING can be approved, PENDING/ACTIVE can be
// rejected, ACTIVE/FULFILLED can be removed.
const ListingModeratorActionBar = ({ listingId, status }: ListingModeratorActionBarProps) => {
    const [openModal, setOpenModal] = useState<"reject" | "remove" | null>(null);

    const { mutate: approve, isPending: isApproving } = useApproveListingAsModerator(listingId);
    const { mutate: reject, isPending: isRejecting } = useRejectListingAsModerator(listingId);
    const { mutate: remove, isPending: isRemoving } = useRemoveListingAsModerator(listingId);

    const canApprove = status === MarketplaceListingStatus.PENDING;
    const canReject = status === MarketplaceListingStatus.PENDING || status === MarketplaceListingStatus.ACTIVE;
    const canRemove = status === MarketplaceListingStatus.ACTIVE || status === MarketplaceListingStatus.FULFILLED;

    if (!canApprove && !canReject && !canRemove) return null;

    const handleApprove = () => {
        approve(undefined, {
            onSuccess: () => toast.success("Listing approved."),
            onError: (error) => toast.error(getErrorMessage(error, "Couldn't approve the listing. Please try again.")),
        });
    };

    const handleReject = (data: { reason: string; note?: string }) => {
        reject(data as MarketplaceReportReasonInput, {
            onSuccess: () => {
                toast.success("Listing rejected.");
                setOpenModal(null);
            },
            onError: (error) => toast.error(getErrorMessage(error, "Couldn't reject the listing. Please try again.")),
        });
    };

    const handleRemove = (data: { reason: string; note?: string }) => {
        remove(data as MarketplaceReportReasonInput, {
            onSuccess: () => {
                toast.success("Listing removed.");
                setOpenModal(null);
            },
            onError: (error) => toast.error(getErrorMessage(error, "Couldn't remove the listing. Please try again.")),
        });
    };

    return (
        <div className="flex flex-col gap-3 rounded-lg border border-border p-4 sm:flex-row sm:items-center sm:justify-between">
            <p className="font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                Moderator Actions
            </p>

            <div className="flex flex-wrap items-center gap-2">
                {canApprove && (
                    <Button size="sm" icon={<Check className="size-4" />} onClick={handleApprove} disabled={isApproving}>
                        {isApproving ? "Approving..." : "Approve"}
                    </Button>
                )}

                {canReject && (
                    <Button
                        size="sm"
                        variant="secondary"
                        icon={<X className="size-4" />}
                        onClick={() => setOpenModal("reject")}
                    >
                        Reject
                    </Button>
                )}

                {canRemove && (
                    <Button
                        size="sm"
                        variant="destructive"
                        icon={<ShieldOff className="size-4" />}
                        onClick={() => setOpenModal("remove")}
                    >
                        Remove
                    </Button>
                )}
            </div>

            <ModerationActionModal
                isOpen={openModal === "reject"}
                onClose={() => setOpenModal(null)}
                title="Reject Listing"
                description="This sends the listing back to its poster along with your reason - they can edit and resubmit it for another review."
                submitLabel="Reject"
                isSubmitting={isRejecting}
                reasonOptions={REASON_OPTIONS}
                onSubmit={handleReject}
            />

            <ModerationActionModal
                isOpen={openModal === "remove"}
                onClose={() => setOpenModal(null)}
                title="Remove Listing"
                description="This permanently deletes the listing's photos and can't be undone or resubmitted. The poster will see your reason on their own listings page."
                submitLabel="Remove"
                isSubmitting={isRemoving}
                reasonOptions={REASON_OPTIONS}
                onSubmit={handleRemove}
            />
        </div>
    );
};

export default ListingModeratorActionBar;
