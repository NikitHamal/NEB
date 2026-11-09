import { cn } from "@/utils/cn";

interface SubjectCodeTileProps {
    code: string;
    /** `sm` for compact inline rows; `md` for a standalone subject block. */
    size?: "sm" | "md";
    className?: string;
}

const sizeClasses = {
    sm: "size-6 rounded-md text-[9px]",
    md: "size-10 rounded-lg text-sm",
};

// Keeps the two-letter truncation and visual language in one place instead of duplicated per call site.
const SubjectCodeTile = ({ code, size = "sm", className }: SubjectCodeTileProps) => (
    <span
        className={cn(
            sizeClasses[size],
            "flex shrink-0 items-center justify-center bg-foreground font-display font-semibold text-accent-foreground",
            className,
        )}
    >
        {code.slice(0, 2)}
    </span>
);

export default SubjectCodeTile;
