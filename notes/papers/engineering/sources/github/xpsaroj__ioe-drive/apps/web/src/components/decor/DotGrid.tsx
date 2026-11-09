import { cn } from "@/utils/cn";

interface DotGridProps {
    className?: string;
}

// Meant to sit behind real content inside a `relative overflow-hidden` container.
const DotGrid = ({ className }: DotGridProps) => (
    <div
        className={cn("pointer-events-none absolute inset-0", className)}
        style={{
            backgroundImage: "radial-gradient(var(--color-border) 1px, transparent 1px)",
            backgroundSize: "16px 16px",
        }}
    />
);

export default DotGrid;
