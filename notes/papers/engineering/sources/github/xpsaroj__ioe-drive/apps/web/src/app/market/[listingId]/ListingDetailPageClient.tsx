"use client"
import { Suspense, use, useState } from "react"
import { useRouter } from "next/navigation";
import { ChevronLeft, ImageOff } from "lucide-react";

import { useListing } from "@/hooks/queries/use-marketplace";
import { useMe } from "@/hooks/queries/use-me";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import Loader from "@/components/ui/Loader";
import {
    LISTING_TYPE_BADGE_VARIANT,
    LISTING_STATUS_BADGE_VARIANT,
    CATEGORY_BADGE_COLOR,
    EditListingButton,
    DeleteListingButton,
    ListingStatusToggleButton,
    ListingModeratorActionBar,
    ReportListingButton,
} from "@/components/common/marketplace";
import { UploaderInfo } from "@/components/common/user";
import { SubjectCodeTile } from "@/components/common/offering";
import { StartConversationButton } from "@/components/common/messaging";
import { cn } from "@/utils/cn";
import { formatListingPrice } from "@/utils/marketplace";
import { isModeratorOrAdmin, MarketplaceListingStatus, MarketplaceListingStatusLabel, MarketplaceListingType, MarketplaceListingTypeLabel, MarketplaceCategoryLabel, MarketplaceReportReasonLabel } from "@/types/entities";
import { EntityPageStateHandler, type BreadcrumbItem } from "@/components/layout";

interface ListingDetailPageClientProps {
    params: Promise<{
        listingId: string;
    }>
}

const ListingDetailContent = ({
    params
}: ListingDetailPageClientProps) => {
    const { listingId: lId } = use(params);
    const listingId = Number(lId);

    const router = useRouter();

    const { data: listing, isPending, error } = useListing(listingId);
    const { data: userData } = useMe();
    const isOwner = !!userData && !!listing?.postedBy && userData.id === listing.postedBy;
    const isModerator = isModeratorOrAdmin(userData?.role);

    const [activePhotoIndex, setActivePhotoIndex] = useState(0);

    const breadcrumbs: BreadcrumbItem[] = [
        { label: "Market", href: "/market" },
        { label: listing?.title ?? "Listing" },
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

    const actions = listing && isOwner ? (
        <div className="flex items-center gap-2 shrink-0">
            <ListingStatusToggleButton listingId={listing.id} status={listing.status} />
            <div className="flex items-center gap-1 border border-border p-0.5 rounded-lg">
                <EditListingButton listingId={listing.id} status={listing.status} />
                <DeleteListingButton listingId={listing.id} onDeleted={() => router.push("/market")} />
            </div>
        </div>
    ) : undefined;

    const title = listing ? (
        <>
            {listing.title}
            <Badge size="sm" variant={LISTING_TYPE_BADGE_VARIANT[listing.type]}>
                {MarketplaceListingTypeLabel[listing.type]}
            </Badge>
            <Badge size="sm" color={CATEGORY_BADGE_COLOR[listing.category]}>
                {MarketplaceCategoryLabel[listing.category]}
            </Badge>
            {listing.status !== MarketplaceListingStatus.ACTIVE && (
                <Badge size="sm" variant={LISTING_STATUS_BADGE_VARIANT[listing.status]}>
                    {MarketplaceListingStatusLabel[listing.status]}
                </Badge>
            )}
        </>
    ) : "Listing Details";

    const isMissing = !listingId || isNaN(listingId) || !listing;

    if (isMissing) {
        return (
            <EntityPageStateHandler
                title={title}
                breadcrumbs={breadcrumbs}
                beforeBreadcrumb={backButton}
                isPending={isPending}
                error={error}
                isEmpty={true}
                loaderText="Loading listing details. Please wait."
                emptyTitle="Listing not found"
                emptyDescription="This listing may have been removed, or the link you followed is incorrect."
                emptyButtonText="Browse Market"
                emptyButtonHref="/market"
            >
                {null}
            </EntityPageStateHandler>
        );
    }

    // Owner needs this to find out why their listing was rejected/removed (no notification system);
    // a moderator needs it too since ListingModeratorActionBar only exposes actions to take
    // next, not the reason recorded by whoever already actioned it.
    const showModerationNotice =
        (isOwner || isModerator) &&
        (listing.status === MarketplaceListingStatus.REJECTED || listing.status === MarketplaceListingStatus.REMOVED);

    const photos = listing.photos ?? [];
    const activePhoto = photos[activePhotoIndex] ?? photos[0];
    const createdAt = new Date(listing.createdAt);
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
            loaderText="Loading listing details. Please wait."
            emptyTitle="Listing not found"
            emptyDescription="This listing may have been removed, or the link you followed is incorrect."
            emptyButtonText="Browse Market"
            emptyButtonHref="/market"
        >
            <div className="space-y-8">
                {showModerationNotice && (
                    <div className="rounded-lg border border-border bg-background-tertiary p-6">
                        <p className="font-medium text-foreground">
                            {listing.status === MarketplaceListingStatus.REMOVED ? "This listing was removed" : "This listing was rejected"}
                            {listing.moderationReason && `: ${MarketplaceReportReasonLabel[listing.moderationReason]}`}
                        </p>
                        {listing.moderationNote && (
                            <p className="mt-1 text-sm text-foreground-secondary">{listing.moderationNote}</p>
                        )}
                        {isOwner && listing.status === MarketplaceListingStatus.REJECTED && (
                            <p className="mt-1 text-sm text-foreground-secondary">Edit this listing to resubmit it for review.</p>
                        )}
                    </div>
                )}

                <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
                    <div className="space-y-8 lg:col-span-2">
                        <div className="space-y-3">
                            <div className="aspect-[4/3] w-full overflow-hidden rounded-lg border border-border bg-background-tertiary">
                                {activePhoto ? (
                                    // Signed URLs are per-request and short-lived - plain <img>, not an oversight.
                                    // eslint-disable-next-line @next/next/no-img-element
                                    <img
                                        src={activePhoto.photoUrl}
                                        alt={listing.title}
                                        className="h-full w-full object-contain"
                                    />
                                ) : (
                                    <div className="flex h-full w-full items-center justify-center">
                                        <ImageOff className="size-8 text-foreground-tertiary" />
                                    </div>
                                )}
                            </div>

                            {photos.length > 1 && (
                                <div className="flex flex-wrap gap-2">
                                    {photos.map((photo, index) => (
                                        <button
                                            key={photo.id}
                                            type="button"
                                            onClick={() => setActivePhotoIndex(index)}
                                            className={cn(
                                                "size-16 shrink-0 overflow-hidden rounded-lg border-2 transition-colors",
                                                index === activePhotoIndex ? "border-accent" : "border-transparent hover:border-border-hover",
                                            )}
                                        >
                                            {/* eslint-disable-next-line @next/next/no-img-element */}
                                            <img src={photo.photoUrl} alt="" className="h-full w-full object-cover" />
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>

                        <div className="rounded-lg border border-border p-6">
                            <h2 className="mb-3 text-lg font-semibold text-foreground">Description</h2>
                            <p className="text-foreground-secondary leading-relaxed whitespace-pre-wrap">{listing.description}</p>
                        </div>

                        {/* Mutually exclusive: a moderator/admin gets direct action controls; anyone
                        else who isn't the poster gets a way to flag the listing instead - never both. */}
                        {isModerator ? (
                            <ListingModeratorActionBar listingId={listing.id} status={listing.status} />
                        ) : (
                            !isOwner &&
                            userData &&
                            (listing.status === MarketplaceListingStatus.ACTIVE ||
                                listing.status === MarketplaceListingStatus.FULFILLED) && (
                                <ReportListingButton listingId={listing.id} />
                            )
                        )}
                    </div>

                    <div className="space-y-6">
                        <div className="rounded-lg border border-border p-6">
                            <p className="mb-3 font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                                Price
                            </p>
                            <p className="text-2xl font-bold text-foreground mb-4">{formatListingPrice(listing.price)}</p>

                            <div className="border-t border-border pt-4">
                                <UploaderInfo
                                    user={listing.poster}
                                    subtitle={`Posted ${formattedCreatedAt}`}
                                    size="md"
                                />
                            </div>

                            {userData &&
                                !isOwner &&
                                (listing.status === MarketplaceListingStatus.ACTIVE ||
                                    listing.status === MarketplaceListingStatus.FULFILLED) && (
                                <div className="mt-4 border-t border-border pt-4">
                                    <StartConversationButton
                                        listingId={listing.id}
                                        label={listing.type === MarketplaceListingType.SELLING ? "Message Seller" : "Message Poster"}
                                    />
                                </div>
                            )}
                        </div>

                        {listing.subjectOffering && (
                            <div className="rounded-lg border border-border p-6">
                                <p className="mb-3 font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                                    Related Subject
                                </p>
                                <div className="flex items-center gap-3 mb-4">
                                    <SubjectCodeTile code={listing.subjectOffering.subject.code} size="md" />
                                    <div className="min-w-0">
                                        <p className="truncate font-semibold text-foreground">{listing.subjectOffering.subject.name}</p>
                                        <p className="text-xs text-foreground-secondary">{listing.subjectOffering.subject.code}</p>
                                    </div>
                                </div>
                                <Button href={`/offerings/${listing.subjectOffering.id}`} variant="secondary" size="sm" className="w-full">
                                    View Subject Page
                                </Button>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </EntityPageStateHandler>
    )
}

const ListingDetailPageClient = (props: ListingDetailPageClientProps) => {
    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading listing details. Please wait." />
            </div>
        }>
            <ListingDetailContent {...props} />
        </Suspense>
    );
}

export default ListingDetailPageClient;
