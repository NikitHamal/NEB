import type { Metadata } from "next";

import { SITE_NAME } from "@/lib/site";
import { SERVER_API_BASE_URL } from "@/lib/server-api-url";
import ListingDetailPageClient from "./ListingDetailPageClient";

interface ListingDetailPageProps {
    params: Promise<{
        listingId: string;
    }>;
}

// A REMOVED listing 404s here for an unauthenticated request - the generic title fallback is expected, not a bug.
export async function generateMetadata({ params }: ListingDetailPageProps): Promise<Metadata> {
    const { listingId } = await params;

    const response = await fetch(`${SERVER_API_BASE_URL}/marketplace/listings/${listingId}`, {
        next: { revalidate: 3600 },
    });

    if (!response.ok) {
        return { title: "Listing Not Found" };
    }

    const body = await response.json();
    if (!body.success) {
        return { title: "Listing Not Found" };
    }

    const listing = body.data;
    const description = listing.description || `${listing.title} - posted on ${SITE_NAME}.`;

    return {
        title: listing.title,
        description,
        openGraph: { title: listing.title, description, type: "article" },
    };
}

const ListingDetailPage = (props: ListingDetailPageProps) => {
    return <ListingDetailPageClient {...props} />;
};

export default ListingDetailPage;
