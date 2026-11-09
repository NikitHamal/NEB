"use client"
import { Suspense, use } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft } from "lucide-react";

import { useUserById } from "@/hooks/queries/use-user";
import { useListings } from "@/hooks/queries/use-marketplace";
import { usePageParam } from "@/hooks/use-page-param";
import { EntityPageStateHandler } from "@/components/layout";
import { ItemList } from "@/components/common/list";
import { MarketplaceListingCard } from "@/components/common/marketplace";
import Button from "@/components/ui/Button";
import Pagination from "@/components/ui/Pagination";
import Loader from "@/components/ui/Loader";

interface UserListingsPageProps {
    params: Promise<{
        userId: string;
    }>;
}

const UserListingsContent = ({ userId }: { userId: number }) => {
    const router = useRouter();
    const { page, setPage } = usePageParam();

    const { data: user } = useUserById(userId);
    const { data, isPending, error, isPlaceholderData } = useListings({ userId }, page);
    const listings = data?.items;

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

    return (
        <EntityPageStateHandler
            title={user ? `${user.fullName}'s Listings` : "Posted Listings"}
            breadcrumbs={[{ label: "User Profile", href: `/users/${userId}` }, { label: "Listings" }]}
            beforeBreadcrumb={backButton}
            isPending={isPending}
            error={error}
            isEmpty={!listings || listings.length === 0}
            loaderText="Loading posted listings. Please wait."
            emptyTitle="No listings posted yet."
            emptyDescription="This user has not posted any listings."
            emptyButtonText="Browse Market"
            emptyButtonHref="/market"
        >
            <div className="space-y-6">
                <ItemList
                    items={listings || []}
                    renderItem={(listing) => <MarketplaceListingCard listing={listing} />}
                />
                <Pagination
                    page={page}
                    totalPages={data?.meta?.totalPages ?? 1}
                    onPageChange={setPage}
                    disabled={isPlaceholderData}
                />
            </div>
        </EntityPageStateHandler>
    );
};

const UserListingsPage = ({ params }: UserListingsPageProps) => {
    const { userId: uId } = use(params);
    const userId = Number(uId);

    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading posted listings. Please wait." />
            </div>
        }>
            <UserListingsContent userId={userId} />
        </Suspense>
    );
};

export default UserListingsPage;
