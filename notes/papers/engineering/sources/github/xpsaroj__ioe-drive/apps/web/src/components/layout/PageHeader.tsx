import { cn } from "@/utils/cn";

import Breadcrumbs, { type BreadcrumbItem } from "./Breadcrumbs";

export type { BreadcrumbItem };

interface PageHeaderProps {
    title: React.ReactNode;
    breadcrumbs: BreadcrumbItem[];
    /** Optional right-aligned content next to the title (e.g. a primary action button). */
    actions?: React.ReactNode;
    className?: string;
    /** Rendered before the breadcrumb trail inside its sticky bar, e.g. a back button. */
    beforeBreadcrumb?: React.ReactNode;
}

// Renders as a fragment, not a wrapping element - the sticky breadcrumb bar needs to sit directly in the page's scroll container to stay stuck.
const PageHeader = ({ title, breadcrumbs, actions, className, beforeBreadcrumb }: PageHeaderProps) => {
    return (
        <>
            <div className={cn("flex items-start justify-between gap-4 pb-4", className)}>
                <h1 className="flex flex-wrap items-center gap-2 text-xl font-medium text-foreground md:text-2xl">{title}</h1>
                {actions && <div className="shrink-0">{actions}</div>}
            </div>
            <div className="sticky top-0 z-10 mb-6 flex items-center gap-2 border-b border-border bg-background/95 py-2.5 backdrop-blur-sm">
                {beforeBreadcrumb}
                <Breadcrumbs items={breadcrumbs} />
            </div>
        </>
    );
};

export default PageHeader;
