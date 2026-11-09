import Link from "next/link";
import { ChevronRight } from "lucide-react";

import { cn } from "@/utils/cn";

export interface BreadcrumbItem {
    label: string;
    /** Omit on the current page's own crumb - it renders as plain text, not a link. */
    href?: string;
}

interface BreadcrumbsProps {
    items: BreadcrumbItem[];
    className?: string;
}

// The last item always renders as plain text, regardless of whether it has an `href`.
const Breadcrumbs = ({ items, className }: BreadcrumbsProps) => {
    return (
        <nav aria-label="Breadcrumb" className={cn("min-w-0", className)}>
            <ol className="flex items-center gap-1.5 overflow-x-auto text-sm">
                {items.map((item, index) => {
                    const isLast = index === items.length - 1;

                    return (
                        <li key={`${item.label}-${index}`} className="flex shrink-0 items-center gap-1.5">
                            {index > 0 && (
                                <ChevronRight className="size-3.5 shrink-0 text-foreground-muted" aria-hidden="true" />
                            )}
                            {item.href && !isLast ? (
                                <Link
                                    href={item.href}
                                    className="rounded-xs text-foreground-secondary transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-foreground focus-visible:ring-offset-2 focus-visible:ring-offset-background"
                                >
                                    {item.label}
                                </Link>
                            ) : (
                                <span
                                    className={isLast ? "font-medium text-foreground" : "text-foreground-secondary"}
                                    aria-current={isLast ? "page" : undefined}
                                >
                                    {item.label}
                                </span>
                            )}
                        </li>
                    );
                })}
            </ol>
        </nav>
    );
};

export default Breadcrumbs;
