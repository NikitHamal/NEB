"use client";
import { toast } from "sonner";
import { CheckCircle2, RotateCcw } from "lucide-react";

import Button from "@/components/ui/Button";
import { useMarkListingFulfilled, useReactivateListing } from "@/hooks/queries/use-marketplace";
import { getErrorMessage } from "@/lib/errors";
import { MarketplaceListingStatus } from "@/types/entities";

interface ListingStatusToggleButtonProps {
    listingId: number;
    status: MarketplaceListingStatus;
}

// Only meaningful for ACTIVE/FULFILLED - PENDING/REJECTED/REMOVED all have no toggle at all.
const ListingStatusToggleButton = ({ listingId, status }: ListingStatusToggleButtonProps) => {
    const { mutate: markFulfilled, isPending: isMarking } = useMarkListingFulfilled(listingId);
    const { mutate: reactivate, isPending: isReactivating } = useReactivateListing(listingId);

    if (status !== MarketplaceListingStatus.ACTIVE && status !== MarketplaceListingStatus.FULFILLED) return null;

    if (status === MarketplaceListingStatus.FULFILLED) {
        return (
            <Button
                size="sm"
                variant="secondary"
                icon={<RotateCcw className="size-4" />}
                disabled={isReactivating}
                onClick={() =>
                    reactivate(undefined, {
                        onSuccess: () => toast.success("Listing reactivated."),
                        onError: (error) =>
                            toast.error(getErrorMessage(error, "Couldn't reactivate the listing. Please try again.")),
                    })
                }
            >
                {isReactivating ? "Reactivating..." : "Reactivate"}
            </Button>
        );
    }

    return (
        <Button
            size="sm"
            variant="secondary"
            icon={<CheckCircle2 className="size-4" />}
            disabled={isMarking}
            onClick={() =>
                markFulfilled(undefined, {
                    onSuccess: () => toast.success("Listing marked as fulfilled."),
                    onError: (error) =>
                        toast.error(getErrorMessage(error, "Couldn't mark the listing as fulfilled. Please try again.")),
                })
            }
        >
            {isMarking ? "Updating..." : "Mark as Fulfilled"}
        </Button>
    );
};

export default ListingStatusToggleButton;
