import { cn } from "@/utils/cn";

interface WordmarkTextProps {
    size?: "sm" | "md" | "lg";
    className?: string;
}

const sizeStyles: Record<NonNullable<WordmarkTextProps["size"]>, string> = {
    sm: "text-sm",
    md: "text-base",
    lg: "text-lg sm:text-2xl",
};

// Pair with <Logo disableLink /> inside a single Link so icon and text share one click target.
const WordmarkText = ({ size = "md", className }: WordmarkTextProps) => {
    return (
        <span className={cn("font-display tracking-tight select-none whitespace-nowrap", sizeStyles[size], className)}>
            <span className="font-semibold">IOE</span>
            <span className="font-medium text-foreground-secondary ml-1">Drive</span>
        </span>
    );
};

export default WordmarkText;
