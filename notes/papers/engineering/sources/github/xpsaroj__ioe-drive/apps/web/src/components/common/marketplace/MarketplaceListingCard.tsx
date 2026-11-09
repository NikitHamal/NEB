import Link from "next/link";
import { ImageOff } from "lucide-react";

import Badge, { type BadgeVariant } from "@/components/ui/Badge";
import type { ListingSummary } from "@/types/api";
import { UploaderInfo } from "@/components/common/user";
import { SubjectCodeTile } from "@/components/common/offering";
import {
    MarketplaceCategory,
    MarketplaceListingStatus,
    MarketplaceListingStatusLabel,
    MarketplaceListingType,
    MarketplaceListingTypeLabel,
    MarketplaceCategoryLabel,
} from "@/types/entities";
import { formatListingPrice } from "@/utils/marketplace";

export const LISTING_TYPE_BADGE_VARIANT: Record<MarketplaceListingType, BadgeVariant> = {
    [MarketplaceListingType.SELLING]: "success",
    [MarketplaceListingType.WANTED]: "info",
};

// Distinct color per category instead of uniform gray - reuses ResourceCard's hues where the association matches.
export const CATEGORY_BADGE_COLOR: Record<MarketplaceCategory, { bg: string; text: string; border?: string }> = {
    [MarketplaceCategory.TEXTBOOKS_AND_NOTES]: { bg: "bg-tag-sepia-bg", text: "text-tag-sepia-text" },
    [MarketplaceCategory.DRAFTING_AND_STATIONERY]: { bg: "bg-tag-slate-bg", text: "text-tag-slate-text" },
    [MarketplaceCategory.CALCULATORS_AND_ELECTRONICS]: { bg: "bg-tag-teal-bg", text: "text-tag-teal-text" },
    [MarketplaceCategory.LAB_AND_WORKSHOP_EQUIPMENT]: { bg: "bg-tag-olive-bg", text: "text-tag-olive-text" },
    [MarketplaceCategory.FURNITURE_AND_HOSTEL_ITEMS]: { bg: "bg-tag-clay-bg", text: "text-tag-clay-text" },
    [MarketplaceCategory.OTHER]: { bg: "bg-badge-background", text: "text-badge-foreground" },
};

// ACTIVE isn't shown - every public browse card is ACTIVE, so the badge would be pure noise
// there. It only appears where a non-ACTIVE listing can show up at all: the poster's own
// listings page and the detail page (reuses this same mapping).
export const LISTING_STATUS_BADGE_VARIANT: Record<MarketplaceListingStatus, BadgeVariant> = {
    [MarketplaceListingStatus.PENDING]: "warning",
    [MarketplaceListingStatus.ACTIVE]: "success",
    [MarketplaceListingStatus.FULFILLED]: "secondary",
    [MarketplaceListingStatus.REJECTED]: "error",
    [MarketplaceListingStatus.REMOVED]: "error",
};

interface MarketplaceListingCardProps {
    listing: ListingSummary;
    /** Self-contained alert block rendered above everything else, e.g. a removed notice. */
    notice?: React.ReactNode;
    /** Optional action buttons (e.g. edit/delete for the listing's owner), rendered next to the title. */
    actions?: React.ReactNode;
}

const MarketplaceListingCard = ({ listing, notice, actions }: MarketplaceListingCardProps) => {
    const { title, description, type, category, price, poster, photos, status } = listing;
    const coverPhoto = photos[0];

    const createdAt = new Date(listing.createdAt);
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

            <div className="flex flex-col gap-4 sm:flex-row">
                <Link
                    href={`/market/${listing.id}`}
                    className="relative aspect-[4/3] w-full shrink-0 overflow-hidden rounded-lg bg-background-tertiary sm:w-40"
                >
                    {coverPhoto ? (
                        // Signed URLs are per-request and short-lived - plain <img>, not an oversight.
                        // eslint-disable-next-line @next/next/no-img-element
                        <img src={coverPhoto.photoUrl} alt={title} className="h-full w-full object-cover" />
                    ) : (
                        <div className="flex h-full w-full items-center justify-center">
                            <ImageOff className="size-7 text-foreground-tertiary" />
                        </div>
                    )}
                </Link>

                <div className="flex min-w-0 flex-1 flex-col gap-3">
                    <div className="flex items-start justify-between gap-3">
                        <div className="min-w-0 flex flex-wrap items-center gap-2">
                            <Link
                                href={`/market/${listing.id}`}
                                className="font-semibold text-foreground decoration-2 underline-offset-3 group-hover/card:underline"
                            >
                                {title}
                            </Link>
                            <Badge size="sm" color={CATEGORY_BADGE_COLOR[category]}>
                                {MarketplaceCategoryLabel[category]}
                            </Badge>
                            {status !== MarketplaceListingStatus.ACTIVE && (
                                <Badge size="sm" variant={LISTING_STATUS_BADGE_VARIANT[status]}>
                                    {MarketplaceListingStatusLabel[status]}
                                </Badge>
                            )}
                        </div>
                        <div className="flex items-center gap-2 shrink-0">
                            <Badge size="sm" variant={LISTING_TYPE_BADGE_VARIANT[type]}>
                                {MarketplaceListingTypeLabel[type]}
                            </Badge>
                            {actions && (
                                <div className="flex items-center gap-1 border border-border p-0.5 rounded-lg">
                                    {actions}
                                </div>
                            )}
                        </div>
                    </div>

                    {description && (
                        <p className="text-sm sm:text-base text-foreground-secondary leading-relaxed line-clamp-2">
                            {description}
                        </p>
                    )}

                    <div className="mt-auto flex items-center justify-between gap-3 pt-3 border-t border-border">
                        <UploaderInfo user={poster} subtitle={formattedCreatedAt} />

                        <div className="flex items-center gap-3 shrink-0">
                            {listing.subjectOffering && (
                                <SubjectCodeTile code={listing.subjectOffering.subject.code} size="sm" />
                            )}
                            <span className="font-semibold text-foreground">{formatListingPrice(price)}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MarketplaceListingCard;
