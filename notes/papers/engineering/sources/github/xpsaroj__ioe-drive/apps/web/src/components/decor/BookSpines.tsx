"use client";
import { motion } from "motion/react";

import { cn } from "@/utils/cn";

export interface BookSpine {
    /** Position along the row, e.g. "12%". */
    left: string;
    /** Tailwind width class, e.g. "w-2". */
    width: string;
    /** Height as a percentage of the container, e.g. "55%". */
    height: string;
    solid?: boolean;
}

interface BookSpinesProps {
    spines: BookSpine[];
    className?: string;
}

// Kept entirely right of ~48% so the shelf never sits behind left-aligned header text.
export const DEFAULT_SHELF_SPINES: BookSpine[] = [
    { left: "48%", width: "w-2", height: "38%" },
    { left: "52%", width: "w-1.5", height: "60%", solid: true },
    { left: "56%", width: "w-2.5", height: "45%" },
    { left: "61%", width: "w-2", height: "65%" },
    { left: "65%", width: "w-1.5", height: "40%", solid: true },
    { left: "69%", width: "w-3", height: "55%" },
    { left: "74%", width: "w-2", height: "35%" },
    { left: "78%", width: "w-1.5", height: "62%", solid: true },
    { left: "82%", width: "w-2.5", height: "48%" },
    { left: "87%", width: "w-2", height: "58%" },
    { left: "91%", width: "w-1.5", height: "42%", solid: true },
    { left: "95%", width: "w-2.5", height: "52%" },
];

// The Library hub's own signature texture, distinct from ScatteredCodeTiles/DotGrid used elsewhere.
const BookSpines = ({ spines, className }: BookSpinesProps) => (
    <div className={cn("pointer-events-none absolute inset-x-0 bottom-0 h-full", className)}>
        {spines.map((spine, index) => (
            <motion.span
                key={index}
                initial={{ scaleY: 0 }}
                animate={{ scaleY: 1 }}
                transition={{ duration: 0.4, ease: "easeOut", delay: index * 0.04 }}
                style={{ left: spine.left, height: spine.height, transformOrigin: "bottom" }}
                className={cn(
                    "absolute bottom-0 rounded-t-sm",
                    spine.width,
                    spine.solid ? "bg-accent/20" : "bg-foreground/[0.08]",
                )}
            />
        ))}
    </div>
);

export default BookSpines;
