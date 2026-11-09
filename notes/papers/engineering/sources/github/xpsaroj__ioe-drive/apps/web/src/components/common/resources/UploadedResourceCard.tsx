import ResourceCard from "./ResourceCard";
import EditResourceButton from "./EditResourceButton";
import DeleteResourceButton from "./DeleteResourceButton";
import type { ResourceSummary } from "@/types/api";
import { ModerationReasonLabel, ResourceStatus } from "@/types/entities";

interface Props {
    item: ResourceSummary;
    /** Only pass where every resource shown is guaranteed to belong to the current user. */
    showOwnerActions?: boolean;
}

const UploadedResourceCard = ({ item, showOwnerActions = false }: Props) => {
    // No notification system - this is how an uploader finds out their resource was rejected/removed.
    const showModerationNotice = item.status === ResourceStatus.REJECTED || item.status === ResourceStatus.REMOVED;

    const moderationNotice = showModerationNotice ? (
        <>
            <p className="font-medium text-foreground">
                {item.status === ResourceStatus.REMOVED ? "This resource was removed" : "This resource was rejected"}
                {item.moderationReason && `: ${ModerationReasonLabel[item.moderationReason]}`}
            </p>
            {item.moderationNote && (
                <p className="mt-1 text-foreground-secondary">{item.moderationNote}</p>
            )}
            {item.status === ResourceStatus.REJECTED && (
                <p className="mt-1 text-foreground-secondary">Edit this resource to resubmit it for review.</p>
            )}
        </>
    ) : undefined;

    return (
        <ResourceCard
            resource={item}
            notice={moderationNotice}
            actions={
                showOwnerActions ? (
                    <div className="flex items-center gap-1 shrink-0">
                        <EditResourceButton resource={item} />
                        <DeleteResourceButton resourceId={item.id} />
                    </div>
                ) : undefined
            }
        />
    );
};

export default UploadedResourceCard;
