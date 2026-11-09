"use client"
import { Suspense } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft } from "lucide-react";

import { EntityPageStateHandler } from "@/components/layout";
import { ConversationList } from "@/components/common/messaging";
import Button from "@/components/ui/Button";
import Pagination from "@/components/ui/Pagination";
import Loader from "@/components/ui/Loader";
import { useConversations } from "@/hooks/queries/use-messaging";
import { useMe } from "@/hooks/queries/use-me";
import { usePageParam } from "@/hooks/use-page-param";

const MessagesContent = () => {
    const router = useRouter();
    const { page, setPage } = usePageParam();
    const { data: userData } = useMe();
    const { data, isPending, error, isPlaceholderData } = useConversations(page);
    const conversations = data?.items;

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
            title="Messages"
            breadcrumbs={[{ label: "Messages" }]}
            beforeBreadcrumb={backButton}
            isPending={isPending || !userData}
            error={error}
            isEmpty={!conversations || conversations.length === 0}
            loaderText="Loading your messages. Please wait."
            emptyTitle="No conversations yet."
            emptyDescription="When you message a seller, or someone messages you about a listing, it'll show up here."
            emptyButtonText="Browse Market"
            emptyButtonHref="/market"
        >
            <div className="space-y-6">
                {userData && conversations && (
                    <ConversationList conversations={conversations} currentUserId={userData.id} />
                )}
                <Pagination
                    page={page}
                    totalPages={data?.meta?.totalPages ?? 1}
                    onPageChange={setPage}
                    disabled={isPlaceholderData}
                />
            </div>
        </EntityPageStateHandler>
    )
}

const MessagesPage = () => {
    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading your messages. Please wait." />
            </div>
        }>
            <MessagesContent />
        </Suspense>
    );
}

export default MessagesPage;
