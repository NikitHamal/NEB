import React from "react";
import Badge, { BadgeProps } from "@/components/ui/Badge";

export interface MimeTypeBadgeProps
    extends Omit<BadgeProps, "children" | "variant" | "color"> {
    mimeType: string;
}

// Theme tag tokens, not raw Tailwind color literals - auto dark-mode via the .dark class.
// Same hue-per-mime-type mapping as ResourceFileItem's FILE_TYPE_META.
const mimeColorMap: Record<
    string,
    { bg: string; text: string; border?: string }
> = {
    pdf: { bg: "bg-tag-rose-bg", text: "text-tag-rose-text", border: "border-tag-rose-text" },
    png: { bg: "bg-tag-violet-bg", text: "text-tag-violet-text", border: "border-tag-violet-text" },
    jpg: { bg: "bg-tag-violet-bg", text: "text-tag-violet-text", border: "border-tag-violet-text" },
    jpeg: { bg: "bg-tag-violet-bg", text: "text-tag-violet-text", border: "border-tag-violet-text" },
    json: { bg: "bg-tag-sepia-bg", text: "text-tag-sepia-text", border: "border-tag-sepia-text" },
    csv: { bg: "bg-tag-olive-bg", text: "text-tag-olive-text", border: "border-tag-olive-text" },
    zip: { bg: "bg-tag-slate-bg", text: "text-tag-slate-text", border: "border-tag-slate-text" },
};

const specialMimeMap: Record<string, string> = {
    "vnd.openxmlformats-officedocument.wordprocessingml.document": "DOCX",
    "vnd.openxmlformats-officedocument.spreadsheetml.sheet": "XLSX",
    "vnd.openxmlformats-officedocument.presentationml.presentation": "PPTX",
    "vnd.ms-excel": "XLS",
    "vnd.ms-powerpoint": "PPT",
};

export function getMimeLabel(mimeType: string) {
    if (!mimeType) return "FILE";

    const [, subtype] = mimeType.split("/");

    if (!subtype) return mimeType.toUpperCase();

    if (specialMimeMap[subtype]) {
        return specialMimeMap[subtype];
    }

    return subtype.toUpperCase();
}

export function getMimeKey(mimeType: string) {
    const [, subtype] = mimeType.split("/");
    return subtype?.split(".").pop()?.toLowerCase() || "file";
}

const MimeTypeBadge: React.FC<MimeTypeBadgeProps> = ({
    mimeType,
    ...props
}) => {
    const label = getMimeLabel(mimeType);
    const key = getMimeKey(mimeType);
    const color = mimeColorMap[key];

    return (
        <Badge size="sm" color={color} {...props}>
            {label}
        </Badge>
    );
};

export default MimeTypeBadge;