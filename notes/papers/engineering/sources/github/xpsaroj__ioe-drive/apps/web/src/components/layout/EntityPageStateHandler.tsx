"use client";
import { Inbox, type LucideIcon } from "lucide-react";

import { PageHeader, PageStateHandler, type BreadcrumbItem } from "@/components/layout";
import Button from "@/components/ui/Button";

interface EntityPageStateHandlerProps {
    title: React.ReactNode;
    breadcrumbs: BreadcrumbItem[];
    /** Optional right-aligned content next to the title (e.g. bookmark/edit/delete). */
    actions?: React.ReactNode;
    /** Rendered before the breadcrumb trail inside its sticky bar, e.g. a back button. See PageHeader. */
    beforeBreadcrumb?: React.ReactNode;
    isPending: boolean;
    error: Error | null | undefined;
    isEmpty: boolean;
    loaderText: string;
    emptyIcon?: LucideIcon;
    emptyTitle: string;
    emptyDescription: string;
    emptyButtonText: string;
    emptyButtonHref: string;
    children: React.ReactNode;
}

// Combines PageHeader + PageStateHandler with a standard "empty state with a CTA
// button" convention - generic across any single-entity detail page (a resource, a
// marketplace listing, an inbox, etc.), not tied to any one domain.
const EntityPageStateHandler = ({
    title,
    breadcrumbs,
    actions,
    beforeBreadcrumb,
    isPending,
    error,
    isEmpty,
    loaderText,
    emptyIcon: EmptyIcon = Inbox,
    emptyTitle,
    emptyDescription,
    emptyButtonText,
    emptyButtonHref,
    children,
}: EntityPageStateHandlerProps) => {
    const headerSection = (
        <PageHeader title={title} breadcrumbs={breadcrumbs} actions={actions} beforeBreadcrumb={beforeBreadcrumb} />
    );

    const emptyContent = (
        <div className="flex flex-col items-center justify-center gap-3 text-center">
            <span className="flex size-12 items-center justify-center rounded-full bg-accent-soft text-accent">
                <EmptyIcon className="size-6" />
            </span>
            <div>
                <p className="text-base sm:text-lg font-semibold text-foreground">{emptyTitle}</p>
                <p className="text-sm sm:text-base text-foreground-secondary mt-1 md:max-w-xl">
                    {emptyDescription}
                </p>
            </div>
            <Button href={emptyButtonHref} size="sm" className="mt-1">{emptyButtonText}</Button>
        </div>
    )

    return (
        <PageStateHandler
            isPending={isPending}
            error={error}
            isEmpty={isEmpty}
            loaderText={loaderText}
            header={headerSection}
            emptyContent={emptyContent}
        >
            {children}
        </PageStateHandler>
    );
};

export default EntityPageStateHandler;
