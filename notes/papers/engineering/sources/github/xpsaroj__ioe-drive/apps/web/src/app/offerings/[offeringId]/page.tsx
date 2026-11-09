import type { Metadata } from "next";

import { SERVER_API_BASE_URL } from "@/lib/server-api-url";
import OfferingPageClient from "./OfferingPageClient";

interface OfferingPageProps {
    params: Promise<{ offeringId: string }>;
}

export async function generateMetadata({ params }: OfferingPageProps): Promise<Metadata> {
    const { offeringId } = await params;

    const response = await fetch(`${SERVER_API_BASE_URL}/subjects/${offeringId}`, {
        next: { revalidate: 3600 },
    });

    if (!response.ok) {
        return { title: "Subject Offering Not Found" };
    }

    const body = await response.json();
    if (!body.success) {
        return { title: "Subject Offering Not Found" };
    }

    const offering = body.data;
    const title = `${offering.subject.code} - ${offering.subject.name}`;
    const description =
        offering.subject.description ||
        `${offering.subject.name} (${offering.subject.code}) - ${offering.program.name} curriculum details, marks breakdown, and shared resources.`;

    return {
        title,
        description,
        openGraph: { title, description, type: "website" },
    };
}

const OfferingPage = (props: OfferingPageProps) => {
    return <OfferingPageClient {...props} />;
};

export default OfferingPage;
