"use client"
import { Suspense, use } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft } from "lucide-react";

import { useUserById } from "@/hooks/queries/use-user";
import { useResourcesByUploaderId } from "@/hooks/queries/use-resources";
import { usePageParam } from "@/hooks/use-page-param";
import { EntityPageStateHandler } from "@/components/layout";
import { ResourceList, UploadedResourceCard } from "@/components/common/resources";
import Button from "@/components/ui/Button";
import Pagination from "@/components/ui/Pagination";
import Loader from "@/components/ui/Loader";

interface UserResourcesPageProps {
    params: Promise<{
        userId: string;
    }>;
}

const UserResourcesContent = ({ userId }: { userId: number }) => {
    const router = useRouter();
    const { page, setPage } = usePageParam();

    const { data: user } = useUserById(userId);
    const { data, isPending, error, isPlaceholderData } = useResourcesByUploaderId(userId, page);
    const resources = data?.items;

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
            title={user ? `${user.fullName}'s Resources` : "Uploaded Resources"}
            breadcrumbs={[{ label: "User Profile", href: `/users/${userId}` }, { label: "Resources" }]}
            beforeBreadcrumb={backButton}
            isPending={isPending}
            error={error}
            isEmpty={!resources || resources.length === 0}
            loaderText="Loading uploaded resources. Please wait."
            emptyTitle="No resources uploaded yet."
            emptyDescription="This user has not uploaded any resources."
            emptyButtonText="Browse Resources"
            emptyButtonHref="/resources"
        >
            <div className="space-y-6">
                <ResourceList
                    resources={resources || []}
                    renderItem={(item) => <UploadedResourceCard item={item} />}
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

const UserResourcesPage = ({ params }: UserResourcesPageProps) => {
    const { userId: uId } = use(params);
    const userId = Number(uId);

    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading uploaded resources. Please wait." />
            </div>
        }>
            <UserResourcesContent userId={userId} />
        </Suspense>
    );
};

export default UserResourcesPage;
