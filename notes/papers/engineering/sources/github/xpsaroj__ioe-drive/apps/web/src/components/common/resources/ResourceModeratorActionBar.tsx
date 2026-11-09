"use client";
import { useState } from "react";
import { toast } from "sonner";
import { Check, ShieldOff, X } from "lucide-react";

import Button from "@/components/ui/Button";
import { ModerationActionModal } from "@/components/common/moderation";
import { useApproveResource, useRejectResource, useRemoveResource } from "@/hooks/queries/use-resources";
import { getErrorMessage } from "@/lib/errors";
import { ModerationReason, ModerationReasonLabel, ResourceStatus } from "@/types/entities";
import type { ModerationReasonInput } from "@/lib/validators/resources";

const REASON_OPTIONS = Object.values(ModerationReason).map((reason) => ({
    value: reason,
    label: ModerationReasonLabel[reason],
}));

interface ResourceModeratorActionBarProps {
    resourceId: number;
    status: ResourceStatus;
}

// Which actions show depends on status: only PENDING can be approved, REMOVED is terminal.
const ResourceModeratorActionBar = ({ resourceId, status }: ResourceModeratorActionBarProps) => {
    const [openModal, setOpenModal] = useState<"reject" | "remove" | null>(null);

    const { mutate: approve, isPending: isApproving } = useApproveResource(resourceId);
    const { mutate: reject, isPending: isRejecting } = useRejectResource(resourceId);
    const { mutate: remove, isPending: isRemoving } = useRemoveResource(resourceId);

    const canApprove = status === ResourceStatus.PENDING;
    const canReject = status === ResourceStatus.PENDING || status === ResourceStatus.APPROVED;
    const canRemove = status !== ResourceStatus.REMOVED;

    if (!canApprove && !canReject && !canRemove) return null;

    const handleApprove = () => {
        approve(undefined, {
            onSuccess: () => toast.success("Resource approved."),
            onError: (error) => toast.error(getErrorMessage(error, "Couldn't approve the resource. Please try again.")),
        });
    };

    const handleReject = (data: { reason: string; note?: string }) => {
        reject(data as ModerationReasonInput, {
            onSuccess: () => {
                toast.success("Resource rejected.");
                setOpenModal(null);
            },
            onError: (error) => toast.error(getErrorMessage(error, "Couldn't reject the resource. Please try again.")),
        });
    };

    const handleRemove = (data: { reason: string; note?: string }) => {
        remove(data as ModerationReasonInput, {
            onSuccess: () => {
                toast.success("Resource removed.");
                setOpenModal(null);
            },
            onError: (error) => toast.error(getErrorMessage(error, "Couldn't remove the resource. Please try again.")),
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
                title="Reject Resource"
                description="This sends the resource back to its uploader along with your reason - they can edit and resubmit it for another review."
                submitLabel="Reject"
                isSubmitting={isRejecting}
                reasonOptions={REASON_OPTIONS}
                onSubmit={handleReject}
            />

            <ModerationActionModal
                isOpen={openModal === "remove"}
                onClose={() => setOpenModal(null)}
                title="Remove Resource"
                description="This permanently deletes the resource's files and can't be undone or resubmitted. The uploader will see your reason on their own uploads page."
                submitLabel="Remove"
                isSubmitting={isRemoving}
                reasonOptions={REASON_OPTIONS}
                onSubmit={handleRemove}
            />
        </div>
    );
};

export default ResourceModeratorActionBar;
