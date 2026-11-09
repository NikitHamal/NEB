import type { Metadata } from "next";

import { SITE_NAME } from "@/lib/site";
import { SERVER_API_BASE_URL } from "@/lib/server-api-url";
import ResourceDetailPageClient from "./ResourceDetailPageClient";

interface ResourceDetailPageProps {
    params: Promise<{
        resourceId: string;
    }>;
}

// A non-APPROVED resource 404s here for an unauthenticated request - the generic title fallback is expected, not a bug.
export async function generateMetadata({ params }: ResourceDetailPageProps): Promise<Metadata> {
    const { resourceId } = await params;

    const response = await fetch(`${SERVER_API_BASE_URL}/resources/${resourceId}`, {
        next: { revalidate: 3600 },
    });

    if (!response.ok) {
        return { title: "Resource Not Found" };
    }

    const body = await response.json();
    if (!body.success) {
        return { title: "Resource Not Found" };
    }

    const resource = body.data;
    const description = resource.description || `${resource.title} - shared on ${SITE_NAME}.`;

    return {
        title: resource.title,
        description,
        openGraph: { title: resource.title, description, type: "article" },
    };
}

const ResourceDetailPage = (props: ResourceDetailPageProps) => {
    return <ResourceDetailPageClient {...props} />;
};

export default ResourceDetailPage;
