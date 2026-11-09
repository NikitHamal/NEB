import { Pencil } from "lucide-react";

import Button from "@/components/ui/Button";
import { MarketplaceListingStatus } from "@/types/entities";

interface EditListingButtonProps {
    listingId: number;
    status: MarketplaceListingStatus;
}

const EditListingButton = ({ listingId, status }: EditListingButtonProps) => {
    // A REMOVED listing's photos were already purged by moderation - it's terminal, no editing.
    if (status === MarketplaceListingStatus.REMOVED) return null;

    return (
        <Button
            href={`/market/${listingId}/edit`}
            variant="ghost"
            size="xs"
            iconOnly
            icon={<Pencil className="size-4" />}
            className="text-foreground-secondary hover:text-info hover:bg-info/10"
            aria-label="Edit listing"
        />
    );
};

export default EditListingButton;
