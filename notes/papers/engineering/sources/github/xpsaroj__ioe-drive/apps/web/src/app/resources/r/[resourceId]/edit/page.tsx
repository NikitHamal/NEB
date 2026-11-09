"use client"
import { use } from "react"
import { useRouter } from "next/navigation";
import { ChevronLeft, SearchX } from "lucide-react";

import { useResource } from "@/hooks/queries/use-resources";
import { useMe } from "@/hooks/queries/use-me";
import Button from "@/components/ui/Button";
import { Breadcrumbs, PageStateHandler, type BreadcrumbItem } from "@/components/layout";
import { ResourceEditForm, ResourceFilesManager, ResourceLinksManager } from "@/components/common/resources";
import { ResourceStatus } from "@/types/entities";

interface ResourceEditPageProps {
    params: Promise<{
        resourceId: string;
    }>
}

const ResourceEditPage = ({
    params
}: ResourceEditPageProps) => {
    const { resourceId: rId } = use(params);
    const resourceId = Number(rId);

    const router = useRouter();

    const { data: resource, isPending, error } = useResource(resourceId);
    const { data: userData, isPending: userPending } = useMe();

    const breadcrumbs: BreadcrumbItem[] = [
        { label: "Resources", href: "/resources" },
        { label: resource?.title ?? "Edit Resource" },
    ];

    // A sticky element can only stick within its own parent's box, so this must NOT be
    // wrapped in a div that's shorter than the page - it needs to sit as a direct child
    // of the full-height page container below (a Fragment, not a div, achieves that).
    const header = (
        <>
            <div className="pb-4">
                <h1 className="text-2xl md:text-3xl font-bold">Edit Resource</h1>
            </div>

            <div className="sticky top-0 z-10 mb-6 flex items-center gap-2 border-b border-border bg-background/95 py-2.5 backdrop-blur-sm">
                <Button
                    icon={<ChevronLeft className="size-4" />}
                    iconOnly
                    variant="ghost"
                    size="xs"
                    className="border border-border shrink-0"
                    onClick={() => router.back()}
                    aria-label="Go back"
                />
                <Breadcrumbs items={breadcrumbs} />
            </div>
        </>
    )

    const emptyContent = (
        <div className="flex flex-col items-center justify-center gap-2 text-center">
            <SearchX className="size-8 text-foreground-tertiary" />
            <p className="text-foreground-secondary">The resource you are looking for does not exist.</p>
        </div>
    )

    const isMissing = !resourceId || isNaN(resourceId) || !resource;

    if (isMissing || isPending || userPending) {
        return (
            <PageStateHandler
                isPending={isPending || userPending}
                error={error}
                isEmpty={!isPending && !userPending && isMissing}
                header={header}
                loaderText="Loading resource details. Please wait."
                emptyContent={emptyContent}
            >
                {null}
            </PageStateHandler>
        );
    }

    const isOwner = !!userData && !!resource.uploadedBy && userData.id === resource.uploadedBy;

    if (!isOwner) {
        return (
            <div className="min-h-screen bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto">
                {header}
                <div className="border rounded-lg flex items-center justify-center py-16">
                    <div className="flex flex-col items-center gap-1 text-center">
                        <p className="text-lg font-medium">You can&apos;t edit this resource.</p>
                        <p className="text-foreground-secondary text-sm">
                            Only the person who uploaded a resource can edit it.
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    if (resource.status === ResourceStatus.REMOVED) {
        return (
            <div className="min-h-screen bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto">
                {header}
                <div className="border rounded-lg flex items-center justify-center py-16">
                    <div className="flex flex-col items-center gap-1 text-center">
                        <p className="text-lg font-medium">This resource has been removed.</p>
                        <p className="text-foreground-secondary text-sm">
                            Its files were purged by moderation, so it can no longer be edited.
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto">
            {header}
            <ResourceEditForm
                resource={resource}
                contentPanel={
                    <div className="space-y-6">
                        <ResourceFilesManager resource={resource} />
                        <ResourceLinksManager resource={resource} />
                    </div>
                }
            />
        </div>
    )
}

export default ResourceEditPage;
