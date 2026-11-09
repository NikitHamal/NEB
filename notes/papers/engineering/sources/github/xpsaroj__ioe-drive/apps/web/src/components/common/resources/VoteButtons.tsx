"use client";
import { ArrowBigDown, ArrowBigUp } from "lucide-react";
import { toast } from "sonner";

import Button from "@/components/ui/Button";
import { useMe, useResourceVoteValues, useSetResourceVote, useClearResourceVote } from "@/hooks/queries/use-me";
import { getErrorMessage } from "@/lib/errors";
import { ResourceStatus } from "@/types/entities";

interface VoteButtonsProps {
    resourceId: number;
    upvoteCount: number;
    downvoteCount: number;
    /** Disables the buttons for the resource's own uploader - voting on your own resource isn't allowed, but the count still shows. */
    uploadedBy?: number;
    status: ResourceStatus;
}

const VoteButtons = ({ resourceId, upvoteCount, downvoteCount, uploadedBy, status }: VoteButtonsProps) => {
    const { data: userData } = useMe();
    const { data: voteValues } = useResourceVoteValues();
    const { mutate: setVote, isPending: isSettingVote } = useSetResourceVote();
    const { mutate: clearVote, isPending: isClearingVote } = useClearResourceVote();

    if (!userData) return null;

    const isOwner = userData.id === uploadedBy;
    // Only an APPROVED resource is publicly live - a moderator/the uploader can still see a
    // PENDING/REJECTED/REMOVED one, but voting on it doesn't mean anything, so the buttons stay
    // visible (for count context) but disabled rather than disappearing. Same treatment for the
    // uploader themselves - they can't vote on their own resource, but should still see the count.
    const isVotable = status === ResourceStatus.APPROVED;
    const myVote = voteValues?.[resourceId];
    const isDisabled = isSettingVote || isClearingVote || !isVotable || isOwner;

    const handleVote = (value: 1 | -1) => {
        const resourceIdString = String(resourceId);
        const onError = (error: unknown) => {
            toast.error(getErrorMessage(error, "Couldn't record your vote. Please try again."));
        };

        if (myVote === value) {
            clearVote(resourceIdString, { onError });
        } else {
            setVote({ resourceId: resourceIdString, value }, { onError });
        }
    };

    const disabledTitle = isOwner
        ? "You can't vote on your own resource"
        : !isVotable
            ? "Only approved resources can be voted on"
            : undefined;

    return (
        <div className="flex items-center gap-1">
            <Button
                variant="ghost"
                size="xs"
                icon={<ArrowBigUp className="size-4" fill={myVote === 1 ? "currentColor" : "none"} />}
                onClick={() => handleVote(1)}
                disabled={isDisabled}
                title={disabledTitle}
                className={myVote === 1 ? "text-success hover:text-success hover:bg-success/10" : "text-foreground-secondary hover:text-success hover:bg-success/10"}
                aria-label={myVote === 1 ? "Remove upvote" : "Upvote"}
                aria-pressed={myVote === 1}
            >
                {upvoteCount}
            </Button>
            <Button
                variant="ghost"
                size="xs"
                icon={<ArrowBigDown className="size-4" fill={myVote === -1 ? "currentColor" : "none"} />}
                onClick={() => handleVote(-1)}
                disabled={isDisabled}
                title={disabledTitle}
                className={myVote === -1 ? "text-error hover:text-error hover:bg-error/10" : "text-foreground-secondary hover:text-error hover:bg-error/10"}
                aria-label={myVote === -1 ? "Remove downvote" : "Downvote"}
                aria-pressed={myVote === -1}
            >
                {downvoteCount}
            </Button>
        </div>
    );
};

export default VoteButtons;
