import MarketplaceListingCard from "./MarketplaceListingCard";
import EditListingButton from "./EditListingButton";
import DeleteListingButton from "./DeleteListingButton";
import ListingStatusToggleButton from "./ListingStatusToggleButton";
import type { ListingSummary } from "@/types/api";
import { MarketplaceListingStatus, MarketplaceReportReasonLabel } from "@/types/entities";

interface MyListingCardProps {
    listing: ListingSummary;
}

// Only ever rendered on the poster's own "My Listings" page - every item shown is guaranteed to be theirs.
const MyListingCard = ({ listing }: MyListingCardProps) => {
    const showModerationNotice =
        listing.status === MarketplaceListingStatus.REJECTED || listing.status === MarketplaceListingStatus.REMOVED;

    const moderationNotice = showModerationNotice ? (
        <>
            <p className="font-medium text-foreground">
                {listing.status === MarketplaceListingStatus.REMOVED ? "This listing was removed" : "This listing was rejected"}
                {listing.moderationReason && `: ${MarketplaceReportReasonLabel[listing.moderationReason]}`}
            </p>
            {listing.moderationNote && (
                <p className="mt-1 text-foreground-secondary">{listing.moderationNote}</p>
            )}
            {listing.status === MarketplaceListingStatus.REJECTED && (
                <p className="mt-1 text-foreground-secondary">Edit this listing to resubmit it for review.</p>
            )}
        </>
    ) : undefined;

    return (
        <MarketplaceListingCard
            listing={listing}
            notice={moderationNotice}
            actions={
                <div className="flex items-center gap-2 shrink-0">
                    <ListingStatusToggleButton listingId={listing.id} status={listing.status} />
                    <EditListingButton listingId={listing.id} status={listing.status} />
                    <DeleteListingButton listingId={listing.id} />
                </div>
            }
        />
    );
};

export default MyListingCard;
