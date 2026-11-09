import Link from "next/link";
import { ImageOff } from "lucide-react";

import { formatListingPrice } from "@/utils/marketplace";

interface ListingPreviewTileProps {
    listingId: number;
    title: string;
    photoUrl?: string;
    price?: number | null;
    categoryLabel: string;
    timeLabel: string;
}

// Same visual language as ResourcePreviewTile (stretched link, hover lift), swapping the
// generic file-type icon for the listing's actual cover photo, since listings are always photo-led elsewhere.
const ListingPreviewTile = ({ listingId, title, photoUrl, price, categoryLabel, timeLabel }: ListingPreviewTileProps) => (
    <div className="group/card relative flex flex-col gap-3 border border-border bg-card-background rounded-lg p-4 transition-all duration-150 hover:border-accent hover:bg-card-hover hover:-translate-y-0.5 hover:shadow-md">
        <Link
            href={`/market/${listingId}`}
            aria-label={title}
            className="absolute inset-0 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-background"
        />

        <div className="relative aspect-[4/3] w-full overflow-hidden rounded-lg bg-background-tertiary">
            {photoUrl ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={photoUrl} alt={title} className="h-full w-full object-cover" />
            ) : (
                <div className="flex h-full w-full items-center justify-center">
                    <ImageOff className="size-6 text-foreground-tertiary" />
                </div>
            )}
        </div>

        <div>
            <p className="text-sm font-semibold text-foreground line-clamp-2 group-hover/card:underline underline-offset-2">
                {title}
            </p>
            <p className="text-xs text-foreground-secondary mt-1 flex items-center gap-2">
                <span>{categoryLabel}</span>
                <span>{formatListingPrice(price)}</span>
            </p>
        </div>

        <span className="font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">
            {timeLabel}
        </span>
    </div>
);

export default ListingPreviewTile;
