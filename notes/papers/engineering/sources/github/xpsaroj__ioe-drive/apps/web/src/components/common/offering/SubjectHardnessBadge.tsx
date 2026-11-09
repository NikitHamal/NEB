import React from "react";
import Badge, { BadgeProps } from "@/components/ui/Badge";
import { SubjectHardnessLevel } from "@/types/entities";

// Theme tokens, not raw Tailwind color literals - auto dark-mode via the .dark class.
const hardnessColorMap: Record<
    SubjectHardnessLevel,
    { bg: string; text: string; border?: string }
> = {
    [SubjectHardnessLevel.EASY]: {
        bg: "bg-badge-success",
        text: "text-badge-success-text",
        border: "border-success",
    },
    [SubjectHardnessLevel.MEDIUM]: {
        bg: "bg-badge-warning",
        text: "text-badge-warning-text",
        border: "border-warning",
    },
    [SubjectHardnessLevel.HARD]: {
        bg: "bg-tag-clay-bg",
        text: "text-tag-clay-text",
        border: "border-tag-clay-text",
    },
    [SubjectHardnessLevel.VERY_HARD]: {
        bg: "bg-badge-error",
        text: "text-badge-error-text",
        border: "border-error",
    },
};

export interface SubjectHardnessBadgeProps
    extends Omit<BadgeProps, "children" | "variant" | "color"> {
    level: SubjectHardnessLevel;
}

const SubjectHardnessBadge: React.FC<SubjectHardnessBadgeProps> = ({
    level,
    ...props
}) => {
    const color = hardnessColorMap[level];

    return (
        <Badge color={color} {...props}>
            {level}
        </Badge>
    );
};

export default SubjectHardnessBadge;