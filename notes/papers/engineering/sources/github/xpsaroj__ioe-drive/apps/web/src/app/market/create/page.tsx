"use client"
import { useRouter } from "next/navigation";
import { ChevronLeft } from "lucide-react";

import Button from "@/components/ui/Button";
import { Breadcrumbs } from "@/components/layout";
import { ListingUploadForm } from "@/components/common/marketplace";

const CreateListingPage = () => {
    const router = useRouter();

    return (
        <div className="min-h-screen bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto">
            <div className="pb-4">
                <h1 className="text-2xl md:text-3xl font-bold">Post a Listing</h1>
                <p className="text-foreground-secondary mt-2">
                    List something for sale, or post what you&apos;re looking for, to reach fellow IOE students.
                </p>
            </div>

            <div className="sticky top-0 z-10 mb-6 flex items-center gap-2 border-b border-border bg-background/95 py-2.5 backdrop-blur-sm">
                <Button
                    icon={<ChevronLeft className="size-4" />}
                    iconOnly
                    variant="ghost"
                    size="xs"
                    className="border border-border shrink-0"
                    onClick={() => router.back()}
                    aria-label="Go back"
                />
                <Breadcrumbs items={[{ label: "Market", href: "/market" }, { label: "Post a Listing" }]} />
            </div>

            <ListingUploadForm />
        </div>
    );
};

export default CreateListingPage;
