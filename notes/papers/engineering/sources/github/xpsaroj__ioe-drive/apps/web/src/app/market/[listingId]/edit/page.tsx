"use client"
import { use } from "react"
import { useRouter } from "next/navigation";
import { ChevronLeft, SearchX } from "lucide-react";

import { useListing } from "@/hooks/queries/use-marketplace";
import { useMe } from "@/hooks/queries/use-me";
import Button from "@/components/ui/Button";
import { Breadcrumbs, PageStateHandler, type BreadcrumbItem } from "@/components/layout";
import { ListingEditForm, ListingPhotosManager } from "@/components/common/marketplace";
import { MarketplaceListingStatus } from "@/types/entities";

interface ListingEditPageProps {
    params: Promise<{
        listingId: string;
    }>
}

const ListingEditPage = ({
    params
}: ListingEditPageProps) => {
    const { listingId: lId } = use(params);
    const listingId = Number(lId);

    const router = useRouter();

    const { data: listing, isPending, error } = useListing(listingId);
    const { data: userData, isPending: userPending } = useMe();

    const breadcrumbs: BreadcrumbItem[] = [
        { label: "Market", href: "/market" },
        { label: listing?.title ?? "Edit Listing" },
    ];

    // A sticky element can only stick within its own parent's box, so this must NOT be
    // wrapped in a div that's shorter than the page - it needs to sit as a direct child
    // of the full-height page container below (a Fragment, not a div, achieves that).
    const header = (
        <>
            <div className="pb-4">
                <h1 className="text-2xl md:text-3xl font-bold">Edit Listing</h1>
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
            <p className="text-foreground-secondary">The listing you are looking for does not exist.</p>
        </div>
    )

    const isMissing = !listingId || isNaN(listingId) || !listing;

    if (isMissing || isPending || userPending) {
        return (
            <PageStateHandler
                isPending={isPending || userPending}
                error={error}
                isEmpty={!isPending && !userPending && isMissing}
                header={header}
                loaderText="Loading listing details. Please wait."
                emptyContent={emptyContent}
            >
                {null}
            </PageStateHandler>
        );
    }

    const isOwner = !!userData && !!listing.postedBy && userData.id === listing.postedBy;

    if (!isOwner) {
        return (
            <div className="min-h-screen bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto">
                {header}
                <div className="border rounded-lg flex items-center justify-center py-16">
                    <div className="flex flex-col items-center gap-1 text-center">
                        <p className="text-lg font-medium">You can&apos;t edit this listing.</p>
                        <p className="text-foreground-secondary text-sm">
                            Only the person who posted a listing can edit it.
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    if (listing.status === MarketplaceListingStatus.REMOVED) {
        return (
            <div className="min-h-screen bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto">
                {header}
                <div className="border rounded-lg flex items-center justify-center py-16">
                    <div className="flex flex-col items-center gap-1 text-center">
                        <p className="text-lg font-medium">This listing has been removed.</p>
                        <p className="text-foreground-secondary text-sm">
                            Its photos were purged by moderation, so it can no longer be edited.
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto">
            {header}
            <ListingEditForm
                listing={listing}
                photosPanel={<ListingPhotosManager listing={listing} />}
            />
        </div>
    )
}

export default ListingEditPage;
