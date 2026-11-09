"use client"
import { Suspense, use, useEffect } from "react"
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ChevronLeft, Lightbulb } from "lucide-react";

import { useResource, useSimilarResources } from "@/hooks/queries/use-resources";
import { useSubjectDetails } from "@/hooks/queries/use-academics";
import { useMe, useMarkResourceAsRecentlyAccessed } from "@/hooks/queries/use-me";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import Loader from "@/components/ui/Loader";
import { EntityPageStateHandler, type BreadcrumbItem } from "@/components/layout";
import {
    ResourceFileList,
    ResourceLinkList,
    EditResourceButton,
    DeleteResourceButton,
    BookmarkButton,
    ResourceEngagementRow,
    ResourceModeratorActionBar,
    ReportResourceButton,
    STATUS_BADGE_VARIANT,
    TYPE_BADGE_COLOR,
} from "@/components/common/resources";
import { UploaderInfo } from "@/components/common/user";
import { SubjectCodeTile } from "@/components/common/offering";
import { isModeratorOrAdmin, ModerationReasonLabel, ResourceStatus, ResourceStatusLabel, ResourceTypeLabel, SemesterLabel } from "@/types/entities";

interface ResourceDetailPageClientProps {
    params: Promise<{
        resourceId: string;
    }>
}

const SIMILAR_RESOURCES_SHOWN = 4;

const ResourceDetailContent = ({
    params
}: ResourceDetailPageClientProps) => {
    const { resourceId: rId } = use(params);
    const resourceId = Number(rId);

    const router = useRouter();

    const { data: resource, isPending, error } = useResource(resourceId);
    const { data: userData } = useMe();
    const isOwner = !!userData && !!resource?.uploadedBy && userData.id === resource.uploadedBy;
    const isModerator = isModeratorOrAdmin(userData?.role);

    const { data: offeringDetails } = useSubjectDetails(resource?.subjectOffering.id ?? 0);
    const { data: similarResources, isPending: similarPending } = useSimilarResources(resourceId, SIMILAR_RESOURCES_SHOWN);

    const { mutate: markAsRecentlyAccessed } = useMarkResourceAsRecentlyAccessed();

    useEffect(() => {
        if (userData && resource) {
            markAsRecentlyAccessed(String(resource.id));
        }
        // Depend on userData.id (not the userData object) so an unrelated profile
        // refetch producing a new object reference doesn't re-fire this. mutate's
        // identity is stable across renders (TanStack Query), so it's fine to omit.
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [userData?.id, resource?.id]);

    const breadcrumbs: BreadcrumbItem[] = [
        { label: "Resources", href: "/resources" },
        { label: resource?.title ?? "Resource" },
    ];

    const backButton = (
        <Button
            icon={<ChevronLeft className="size-4" />}
            iconOnly
            variant="ghost"
            size="xs"
            className="border border-border shrink-0"
            onClick={() => router.back()}
            aria-label="Go back"
        />
    );

    // The badge sits right next to the title itself (via the composed `title` node
    // below) rather than here, so this only needs to hold owner-only actions. The
    // bookmark toggle lives as a prominent "Save" button in the body.
    const actions = resource && isOwner ? (
        <div className="flex items-center gap-1 shrink-0 border border-border p-0.5 rounded-lg">
            <EditResourceButton resource={resource} />
            <DeleteResourceButton
                resourceId={resource.id}
                onDeleted={() => router.push("/library/uploads")}
            />
        </div>
    ) : undefined;

    const title = resource ? (
        <>
            {resource.title}
            <Badge size="sm" color={TYPE_BADGE_COLOR[resource.type]}>{ResourceTypeLabel[resource.type]}</Badge>
            {resource.status !== ResourceStatus.APPROVED && (
                <Badge size="sm" variant={STATUS_BADGE_VARIANT[resource.status]}>
                    {ResourceStatusLabel[resource.status]}
                </Badge>
            )}
        </>
    ) : "Resource Details";

    const isMissing = !resourceId || isNaN(resourceId) || !resource;

    if (isMissing) {
        return (
            <EntityPageStateHandler
                title={title}
                breadcrumbs={breadcrumbs}
                beforeBreadcrumb={backButton}
                isPending={isPending}
                error={error}
                isEmpty={true}
                loaderText="Loading resource details. Please wait."
                emptyTitle="Resource not found"
                emptyDescription="This resource may have been removed, or the link you followed is incorrect."
                emptyButtonText="Browse Resources"
                emptyButtonHref="/resources"
            >
                {null}
            </EntityPageStateHandler>
        );
    }

    // Owner needs this to find out why their upload was actioned (no notification system);
    // a moderator needs it too since ResourceModeratorActionBar only exposes actions to take
    // next, not the reason recorded by whoever already actioned it.
    const showModerationNotice =
        (isOwner || isModerator) &&
        (resource.status === ResourceStatus.REJECTED || resource.status === ResourceStatus.REMOVED);

    const { files = [], links = [], subjectOffering } = resource;
    const createdAt = new Date(resource.createdAt);
    const formattedCreatedAt = createdAt.toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
    });

    return (
        <EntityPageStateHandler
            title={title}
            breadcrumbs={breadcrumbs}
            beforeBreadcrumb={backButton}
            actions={actions}
            isPending={isPending}
            error={error}
            isEmpty={false}
            loaderText="Loading resource details. Please wait."
            emptyTitle="Resource not found"
            emptyDescription="This resource may have been removed, or the link you followed is incorrect."
            emptyButtonText="Browse Resources"
            emptyButtonHref="/resources"
        >
            <div className="space-y-8">
                <div className="flex flex-col gap-4 pb-8 border-b border-border sm:flex-row sm:items-center sm:justify-between">
                    <UploaderInfo
                        user={resource.uploader}
                        subtitle={formattedCreatedAt}
                        size="md"
                    />

                    {userData && (
                        <div className="sm:w-auto sm:shrink-0">
                            <BookmarkButton resourceId={resource.id} showLabel />
                        </div>
                    )}
                </div>


                <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
                    <div className="space-y-8 lg:col-span-2">
                        {showModerationNotice && (
                            <div className="rounded-lg border border-border bg-background-tertiary p-6">
                                <p className="font-medium text-foreground">
                                    {resource.status === ResourceStatus.REMOVED ? "This resource was removed" : "This resource was rejected"}
                                    {resource.moderationReason && `: ${ModerationReasonLabel[resource.moderationReason]}`}
                                </p>
                                {resource.moderationNote && (
                                    <p className="mt-1 text-sm text-foreground-secondary">{resource.moderationNote}</p>
                                )}
                                {isOwner && resource.status === ResourceStatus.REJECTED && (
                                    <p className="mt-1 text-sm text-foreground-secondary">Edit this resource to resubmit it for review.</p>
                                )}
                            </div>
                        )}

                        <div className="rounded-lg border border-border p-6">
                            <h2 className="mb-3 text-lg font-semibold text-foreground">Description</h2>
                            <p className="text-foreground-secondary leading-relaxed">{resource.description}</p>
                        </div>

                        <div className="rounded-lg border border-border p-6">
                            <ResourceFileList resourceFiles={files} />
                        </div>

                        {links.length > 0 && (
                            <div className="rounded-lg border border-border p-6">
                                <ResourceLinkList resourceLinks={links} />
                            </div>
                        )}

                        <ResourceEngagementRow
                            resourceId={resource.id}
                            upvoteCount={resource.upvoteCount}
                            downvoteCount={resource.downvoteCount}
                            downloadCount={resource.downloadCount}
                            uploadedBy={resource.uploadedBy}
                            status={resource.status}
                            className="rounded-lg border border-border p-6"
                        />

                        {/* Mutually exclusive: a moderator/admin gets direct action
                        controls; anyone else who isn't the uploader gets a way to flag
                        the resource instead - never both in the same spot. */}
                        {isModerator ? (
                            <ResourceModeratorActionBar resourceId={resource.id} status={resource.status} />
                        ) : (
                            !isOwner && resource.status === ResourceStatus.APPROVED && userData && (
                                <ReportResourceButton resourceId={resource.id} />
                            )
                        )}
                    </div>

                    <div className="space-y-6">
                        <div className="rounded-lg border border-border p-6">
                            <p className="mb-3 font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                                Related Subject
                            </p>
                            <div className="flex items-center gap-3 mb-4">
                                <SubjectCodeTile code={subjectOffering.subject.code} size="md" />
                                <div className="min-w-0">
                                    <p className="truncate font-semibold text-foreground">{subjectOffering.subject.name}</p>
                                    <p className="text-xs text-foreground-secondary flex items-center gap-2">
                                        <span>{subjectOffering.subject.code}</span>
                                        {offeringDetails && <span>{SemesterLabel[offeringDetails.semester]} Semester</span>}
                                    </p>
                                </div>
                            </div>
                            <Button href={`/offerings/${subjectOffering.id}`} variant="secondary" size="sm" className="w-full">
                                View Subject Page
                            </Button>
                        </div>

                        <div className="rounded-lg border border-border p-6">
                            <div className="mb-3 flex items-center gap-2 font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                                <Lightbulb className="size-3.5" />
                                Similar Resources
                            </div>
                            {similarPending ? (
                                <div className="-mx-6 divide-y divide-border">
                                    {Array.from({ length: 3 }).map((_, i) => (
                                        <div key={i} className="flex items-center gap-3 px-6 py-3">
                                            <div className="h-4 w-full animate-pulse rounded bg-skeleton-base" />
                                        </div>
                                    ))}
                                </div>
                            ) : similarResources && similarResources.length > 0 ? (
                                <div className="-mx-6 divide-y divide-border">
                                    {similarResources.map((item) => (
                                        <Link
                                            key={item.id}
                                            href={`/resources/r/${item.id}`}
                                            className="flex items-center justify-between gap-3 px-6 py-3 transition-colors hover:bg-background-hover"
                                        >
                                            <p className="truncate text-sm text-foreground">{item.title}</p>
                                            <Badge size="sm" color={TYPE_BADGE_COLOR[item.type]} className="shrink-0">{ResourceTypeLabel[item.type]}</Badge>
                                        </Link>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-sm text-foreground-tertiary">
                                    No other resources shared for this subject yet.
                                </p>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </EntityPageStateHandler>
    )
}

const ResourceDetailPageClient = (props: ResourceDetailPageClientProps) => {
    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading resource details. Please wait." />
            </div>
        }>
            <ResourceDetailContent {...props} />
        </Suspense>
    );
}

export default ResourceDetailPageClient;
