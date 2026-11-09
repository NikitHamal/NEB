import Link from "next/link";
import type { LucideIcon } from "lucide-react";

import { cn } from "@/utils/cn";

export interface StatStripItem {
    href: string;
    label: string;
    value: number | undefined;
    icon?: LucideIcon;
}

interface StatStripProps {
    items: StatStripItem[];
    /** "boxed": one divided box (default). "inline": borderless, for sitting next to other text. "cards": separate cards with an icon, for stats as primary content. */
    variant?: "boxed" | "inline" | "cards";
    className?: string;
}

// Shared between the dashboard hero and the library hub.
const StatStrip = ({ items, variant = "boxed", className }: StatStripProps) => {
    if (variant === "cards") {
        return (
            <div className={cn("grid grid-cols-1 sm:grid-cols-3 gap-4", className)}>
                {items.map((item) => (
                    <Link
                        key={item.label}
                        href={item.href}
                        className="flex items-center gap-3 rounded-lg border border-border p-4 transition-colors hover:bg-background-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-background"
                    >
                        {item.icon && (
                            <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-accent text-accent-foreground">
                                <item.icon className="size-5" />
                            </span>
                        )}
                        <div>
                            <p className="font-display text-[11px] uppercase tracking-wide text-foreground-secondary">{item.label}</p>
                            <p className="text-lg font-bold text-foreground leading-tight mt-0.5">{item.value ?? "–"}</p>
                        </div>
                    </Link>
                ))}
            </div>
        );
    }

    if (variant === "inline") {
        return (
            <div className={cn("flex divide-x divide-border", className)}>
                {items.map((item) => (
                    <Link
                        key={item.label}
                        href={item.href}
                        className="px-4 first:pl-0 last:pr-0 text-center sm:text-left rounded-xs transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
                    >
                        <p className="font-display text-[11px] uppercase tracking-wide text-foreground-secondary">{item.label}</p>
                        <p className="text-xl font-bold text-foreground leading-tight mt-1">{item.value ?? "–"}</p>
                    </Link>
                ))}
            </div>
        );
    }

    return (
        <div className={cn("flex flex-col sm:flex-row border border-border rounded-lg divide-y sm:divide-y-0 sm:divide-x divide-border overflow-hidden", className)}>
            {items.map((item) => (
                <Link
                    key={item.label}
                    href={item.href}
                    className="flex-1 px-5 py-4 text-center sm:text-left transition-colors hover:bg-background-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-inset"
                >
                    <p className="text-2xl font-bold text-foreground leading-none">{item.value ?? "–"}</p>
                    <p className="font-display text-[11px] uppercase tracking-wide text-foreground-secondary mt-1.5">{item.label}</p>
                </Link>
            ))}
        </div>
    );
};

export default StatStrip;
