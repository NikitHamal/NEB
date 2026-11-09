import ResourceLinkItem from "./ResourceLinkItem";
import type { ResourceLinkSummary } from "@/types/api";

interface ResourceLinkListProps {
    resourceLinks: ResourceLinkSummary[];
    /** Hide the "Links" heading - for compact contexts where it'd repeat on every item. */
    showLabel?: boolean;
}

// Unlike ResourceFileList, renders nothing when empty - most resources have no links, and
// showing an empty-state block on every one of them would just be noise.
const ResourceLinkList = ({ resourceLinks, showLabel = true }: ResourceLinkListProps) => {
    if (!resourceLinks || resourceLinks.length === 0) return null;

    return (
        <div>
            {showLabel && <p className="mb-3 text-lg font-semibold text-foreground">Links</p>}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                {resourceLinks.map((link) => (
                    <ResourceLinkItem key={link.id} link={link} />
                ))}
            </div>
        </div>
    );
};

export default ResourceLinkList;
