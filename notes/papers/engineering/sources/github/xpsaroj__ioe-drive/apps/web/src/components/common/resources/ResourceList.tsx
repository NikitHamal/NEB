import type { ReactNode } from "react";

import { ItemList } from "@/components/common/list";
import ResourceCardSkeleton from "./ResourceCardSkeleton";

interface ResourceListProps<T> {
    resources: T[];
    loading?: boolean;
    error?: string | null;
    renderItem: (item: T) => ReactNode;
    emptyMessage?: string;
    /** Overrides the default icon+message empty state, e.g. to add a CTA. */
    emptyState?: ReactNode;
}

// Thin resource-flavored wrapper around the generic ItemList - just supplies the
// resource-shaped loading skeleton, so every existing resource-domain call site keeps
// working unchanged.
const ResourceList = <T,>({
    resources,
    loading,
    error,
    renderItem,
    emptyMessage = "No resources found.",
    emptyState,
}: ResourceListProps<T>) => {
    return (
        <ItemList
            items={resources}
            loading={loading}
            error={error}
            renderItem={renderItem}
            emptyMessage={emptyMessage}
            emptyState={emptyState}
            renderSkeleton={() => <ResourceCardSkeleton />}
        />
    );
}

export default ResourceList;
