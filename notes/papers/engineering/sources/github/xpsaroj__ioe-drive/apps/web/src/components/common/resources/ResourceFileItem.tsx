import Link from "next/link";
import { File, FileArchive, FileImage, FileJson, FileSpreadsheet, FileText, Presentation, type LucideIcon } from "lucide-react";

import { getMimeKey, getMimeLabel } from "./MimeTypeBadge";
import { formatFileSize } from "@/utils/file";
import type { ResourceFileSummary } from "@/types/api";

export interface FileTypeMeta {
    icon: LucideIcon;
    className: string;
}

// Theme tag tokens, not raw Tailwind color literals - auto dark-mode via the .dark class.
export const FILE_TYPE_META: Record<string, FileTypeMeta> = {
    pdf: { icon: FileText, className: "bg-tag-rose-bg text-tag-rose-text" },
    png: { icon: FileImage, className: "bg-tag-violet-bg text-tag-violet-text" },
    jpg: { icon: FileImage, className: "bg-tag-violet-bg text-tag-violet-text" },
    jpeg: { icon: FileImage, className: "bg-tag-violet-bg text-tag-violet-text" },
    document: { icon: FileText, className: "bg-tag-blue-bg text-tag-blue-text" },
    sheet: { icon: FileSpreadsheet, className: "bg-tag-olive-bg text-tag-olive-text" },
    "ms-excel": { icon: FileSpreadsheet, className: "bg-tag-olive-bg text-tag-olive-text" },
    csv: { icon: FileSpreadsheet, className: "bg-tag-olive-bg text-tag-olive-text" },
    presentation: { icon: Presentation, className: "bg-tag-clay-bg text-tag-clay-text" },
    "ms-powerpoint": { icon: Presentation, className: "bg-tag-clay-bg text-tag-clay-text" },
    json: { icon: FileJson, className: "bg-tag-sepia-bg text-tag-sepia-text" },
    zip: { icon: FileArchive, className: "bg-tag-slate-bg text-tag-slate-text" },
};

export const DEFAULT_FILE_TYPE_META: FileTypeMeta = {
    icon: File,
    className: "bg-background-tertiary text-foreground-secondary",
};

interface ResourceFileItemProps {
    file: ResourceFileSummary;
}

// Width comes entirely from the parent grid's track sizing (see ResourceFileList) - this
// just fills its cell, so the same markup works at any column count.
const ResourceFileItem = ({ file }: ResourceFileItemProps) => {
    const { id: fileId, resourceId, originalFileName, mimeType, fileSize } = file;
    const { icon: Icon, className } = FILE_TYPE_META[getMimeKey(mimeType)] ?? DEFAULT_FILE_TYPE_META;

    return (
        <Link
            href={`/resources/r/${resourceId}/files/${fileId}`}
            className="flex w-full items-center gap-2.5 rounded-lg border border-border p-2 transition-colors duration-150 hover:border-foreground-tertiary hover:bg-background-tertiary"
        >
            <span className={`flex size-9 shrink-0 items-center justify-center rounded-md ${className}`}>
                <Icon className="size-4" />
            </span>
            <div className="min-w-0">
                <p className="truncate text-sm font-medium text-foreground">{originalFileName}</p>
                <p className="font-display text-[11px] uppercase tracking-wide text-foreground-tertiary flex items-center gap-2">
                    <span>{getMimeLabel(mimeType)}</span>
                    <span>{formatFileSize(fileSize)}</span>
                </p>
            </div>
        </Link>
    )
}

export default ResourceFileItem;
