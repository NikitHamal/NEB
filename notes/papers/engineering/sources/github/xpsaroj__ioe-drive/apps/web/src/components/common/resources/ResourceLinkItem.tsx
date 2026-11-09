import { ExternalLink } from "lucide-react";

import type { ResourceLinkSummary } from "@/types/api";

export const getHostname = (url: string): string => {
    try {
        return new URL(url).hostname.replace(/^www\./, "");
    } catch {
        return url;
    }
};

interface ResourceLinkItemProps {
    link: ResourceLinkSummary;
}

// Width comes from the parent grid's track sizing (see ResourceLinkList), same as ResourceFileItem.
const ResourceLinkItem = ({ link }: ResourceLinkItemProps) => (
    <a
        href={link.url}
        target="_blank"
        rel="noopener noreferrer"
        className="flex w-full items-center gap-2.5 rounded-lg border border-border p-2 transition-colors duration-150 hover:border-foreground-tertiary hover:bg-background-tertiary"
    >
        <span className="flex size-9 shrink-0 items-center justify-center rounded-md bg-background-tertiary text-foreground-secondary">
            <ExternalLink className="size-4" />
        </span>
        <div className="min-w-0">
            <p className="truncate text-sm font-medium text-foreground">{link.label}</p>
            <p className="truncate font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">
                {getHostname(link.url)}
            </p>
        </div>
    </a>
);

export default ResourceLinkItem;
