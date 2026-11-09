"use client"
import { useRouter } from "next/navigation";
import { use } from "react"
import { ChevronLeft } from "lucide-react"

import Button from "@/components/ui/Button";
import { EntityPageStateHandler, type BreadcrumbItem } from "@/components/layout";
import { useSubjectDetails } from "@/hooks/queries/use-academics";
import { SubjectOfferingDetails } from "@/components/common/offering";

interface OfferingPageClientProps {
    params: Promise<{ offeringId: string }>
}

const OfferingPageClient = ({
    params
}: OfferingPageClientProps) => {
    const router = useRouter();
    const { offeringId } = use(params)
    const { data: offering, isPending, error } = useSubjectDetails(Number(offeringId));

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

    const breadcrumbs: BreadcrumbItem[] = [
        { label: "Offerings", href: "/offerings" },
        { label: offering?.subject.code ?? "Offering Details" },
    ];

    return (
        <EntityPageStateHandler
            title={offering ? `${offering.subject.code} - ${offering.subject.name}` : "Offering Details"}
            breadcrumbs={breadcrumbs}
            beforeBreadcrumb={backButton}
            isPending={isPending}
            error={error}
            isEmpty={!offering}
            loaderText="Loading offering details. Please wait."
            emptyTitle="Subject offering not found"
            emptyDescription="This subject offering may not exist, or the link you followed is incorrect."
            emptyButtonText="Browse Offerings"
            emptyButtonHref="/offerings"
        >
            {offering && (
                <SubjectOfferingDetails offering={offering} />
            )}
        </EntityPageStateHandler>
    )
}

export default OfferingPageClient;