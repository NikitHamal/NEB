"use client";
import { useState } from "react";
import { toast } from "sonner";
import { Flag } from "lucide-react";

import Button from "@/components/ui/Button";
import { ModerationActionModal } from "@/components/common/moderation";
import { useReportResource } from "@/hooks/queries/use-resources";
import { getErrorMessage } from "@/lib/errors";
import { ModerationReason, ModerationReasonLabel } from "@/types/entities";
import type { ModerationReasonInput } from "@/lib/validators/resources";

const REASON_OPTIONS = Object.values(ModerationReason).map((reason) => ({
    value: reason,
    label: ModerationReasonLabel[reason],
}));

interface ReportResourceButtonProps {
    resourceId: number;
}

// Mutually exclusive with ResourceModeratorActionBar, whose bar style this matches - a viewer sees exactly one.
const ReportResourceButton = ({ resourceId }: ReportResourceButtonProps) => {
    const [isOpen, setIsOpen] = useState(false);
    const { mutate, isPending } = useReportResource(resourceId);

    const handleSubmit = (data: { reason: string; note?: string }) => {
        mutate(data as ModerationReasonInput, {
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
                Found something misleading or inappropriate about this resource?
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
                title="Report Resource"
                description="Let a moderator know what's wrong with this resource. Your identity isn't shared with its uploader."
                submitLabel="Submit Report"
                isSubmitting={isPending}
                reasonOptions={REASON_OPTIONS}
                onSubmit={handleSubmit}
            />
        </div>
    );
};

export default ReportResourceButton;
