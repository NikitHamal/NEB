import ResourceFileItem from "./ResourceFileItem";
import type { ResourceFileSummary } from "@/types/api";

interface ResourceFileListProps {
    resourceFiles: ResourceFileSummary[];
    loading?: boolean;
    error?: string | null;
    /** Hide the "Files" heading - for compact contexts where it'd repeat on every item. */
    showLabel?: boolean;
}

const ResourceFileList = ({
    resourceFiles,
    loading = false,
    error = null,
    showLabel = true,
}: ResourceFileListProps) => {
    if (loading) {
        return (
            <div>
                <p className="text-xs text-foreground-tertiary">Loading files. Please wait...</p>
            </div>
        )
    }

    if (error) {
        return (
            <div>
                <p className="text-xs text-error">{error || "Error loading files. Please try again."}</p>
            </div>
        )
    }

    if (!resourceFiles || resourceFiles.length === 0) {
        return (
            <div>
                <p className="text-xs text-foreground-tertiary">No files attached to this resource.</p>
            </div>
        )
    }

    return (
        <div>
            {showLabel && <p className="mb-3 text-lg font-semibold text-foreground">Files</p>}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                {resourceFiles.map((file) => (
                    <ResourceFileItem key={file.id} file={file} />
                ))}
            </div>
        </div>
    )
}

export default ResourceFileList;
