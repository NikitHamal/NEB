import Link from "next/link";

import ResourceFileList from "./ResourceFileList";
import ResourceLinkList from "./ResourceLinkList";
import BookmarkButton from "./BookmarkButton";
import ResourceEngagementRow from "./ResourceEngagementRow";
import NewBadge from "./NewBadge";
import Badge, { type BadgeVariant } from "@/components/ui/Badge";
import type { ResourceSummary } from "@/types/api";
import { UploaderInfo } from "@/components/common/user";
import { SubjectCodeTile } from "@/components/common/offering";
import { ResourceStatus, ResourceStatusLabel, ResourceType, ResourceTypeLabel } from "@/types/entities";

/** APPROVED isn't shown - every public browse card is APPROVED, so the badge would be
 * pure noise there. It only appears where a non-APPROVED resource can show up at all:
 * the uploader's own uploads list, the moderation queues, and the detail page (which
 * reuses this same mapping - see the resource detail page). */
export const STATUS_BADGE_VARIANT: Record<ResourceStatus, BadgeVariant> = {
    [ResourceStatus.PENDING]: "warning",
    [ResourceStatus.APPROVED]: "success",
    [ResourceStatus.REJECTED]: "error",
    [ResourceStatus.REMOVED]: "secondary",
};

// Distinct color per type instead of uniform gray.
export const TYPE_BADGE_COLOR: Record<ResourceType, { bg: string; text: string; border?: string }> = {
    [ResourceType.NOTE]: { bg: "bg-tag-blue-bg", text: "text-tag-blue-text" },
    [ResourceType.PAST_QUESTION]: { bg: "bg-tag-violet-bg", text: "text-tag-violet-text" },
    [ResourceType.ASSESSMENT]: { bg: "bg-tag-rose-bg", text: "text-tag-rose-text" },
    [ResourceType.LAB_SHEET]: { bg: "bg-tag-teal-bg", text: "text-tag-teal-text" },
    [ResourceType.BOOK]: { bg: "bg-tag-sepia-bg", text: "text-tag-sepia-text" },
    [ResourceType.OTHER]: { bg: "bg-badge-background", text: "text-badge-foreground" },
};

interface ResourceCardProps {
    resource: ResourceSummary;
    meta?: string;
    /** Self-contained alert block rendered above everything else, e.g. a removed/rejected notice. */
    notice?: React.ReactNode;
    /**
     * Optional action buttons (e.g. edit/delete for the resource's owner), rendered
     * next to the title.
     */
    actions?: React.ReactNode;
}

const ResourceCard = ({
    resource,
    meta,
    notice,
    actions,
}: ResourceCardProps) => {
    const {
        title,
        description,
        type,
        files = [],
        links = [],
        uploader,
        uploadedBy,
        subjectOffering,
        upvoteCount,
        downvoteCount,
        downloadCount,
    } = resource;

    const createdAt = new Date(resource.createdAt);
    const formattedCreatedAt = createdAt.toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
    });

    return (
        <div className="group/card relative flex flex-col gap-4 rounded-lg border border-border bg-card-background p-4 transition-colors duration-400 hover:border-accent sm:p-5">
            {notice && (
                <div className="rounded-lg border border-border bg-background-tertiary px-3 py-2.5 text-sm">
                    {notice}
                </div>
            )}

            {meta && (
                <p className="font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">
                    {meta}
                </p>
            )}

            <div className="flex items-start justify-between gap-3">
                <div className="min-w-0 flex flex-wrap items-center gap-2">
                    <Link
                        href={`/resources/r/${resource.id}`}
                        className="font-semibold text-foreground decoration-2 underline-offset-3 group-hover/card:underline"
                    >
                        {title}
                    </Link>
                    <Badge size="sm" color={TYPE_BADGE_COLOR[type]}>{ResourceTypeLabel[type]}</Badge>
                    {resource.status !== ResourceStatus.APPROVED && (
                        <Badge size="sm" variant={STATUS_BADGE_VARIANT[resource.status]}>
                            {ResourceStatusLabel[resource.status]}
                        </Badge>
                    )}
                </div>
                <div className="flex items-center gap-2 shrink-0">
                    <NewBadge createdAt={resource.createdAt} />
                    <div className="flex items-center gap-1 border border-border p-0.5 rounded-lg">
                        <BookmarkButton resourceId={resource.id} />
                        {actions}
                    </div>
                </div>
            </div>

            {description && (
                <p className="text-sm sm:text-base text-foreground-secondary leading-relaxed line-clamp-2">
                    {description}
                </p>
            )}

            <ResourceFileList resourceFiles={files} showLabel={false} />
            <ResourceLinkList resourceLinks={links} showLabel={false} />

            <div className="flex items-center justify-between gap-3 pt-3 border-t border-border">
                <UploaderInfo
                    user={uploader}
                    subtitle={formattedCreatedAt}
                />

                <Link
                    href={`/offerings/${subjectOffering.id}`}
                    className="group/subject flex items-center gap-2 shrink-0 rounded-lg -mx-1.5 -my-1 px-1.5 py-1 transition-colors hover:bg-background-hover"
                >
                    <SubjectCodeTile code={subjectOffering?.subject?.code ?? ""} size="sm" />
                    <span className="text-xs text-foreground-secondary group-hover/subject:text-foreground group-hover/subject:underline">
                        {subjectOffering?.subject?.code}
                        <span className="hidden sm:inline"> {subjectOffering?.subject?.name}</span>
                    </span>
                </Link>
            </div>

            <ResourceEngagementRow
                resourceId={resource.id}
                upvoteCount={upvoteCount}
                downvoteCount={downvoteCount}
                downloadCount={downloadCount}
                uploadedBy={uploadedBy}
                status={resource.status}
                className="pt-3 border-t border-border"
            />
        </div>
    )
}

export default ResourceCard;
