import Link from "next/link";
import type { LucideIcon } from "lucide-react";

import Image from "@/components/ui/ImageContainer";
import { cn } from "@/utils/cn";

export interface FeatureListItem {
    title: string;
    description: string;
    icon: LucideIcon;
    /** Renders the card as a link when provided; a plain, non-interactive card otherwise. */
    href?: string;
}

interface FeatureListProps {
    items: FeatureListItem[];
    className?: string;
}

// Zigzag card list with connecting arrows - shared by the homepage's "What this site offers"
// and the About page's "How it works", so both stay visually consistent.
const FeatureList = ({ items, className }: FeatureListProps) => (
    <div className={cn("flex flex-col gap-8 sm:gap-12", className)}>
        {items.map((item, index) => (
            <FeatureRow key={item.title} item={item} index={index} isLast={index === items.length - 1} />
        ))}
    </div>
);

const FeatureRow = ({ item, index, isLast }: { item: FeatureListItem; index: number; isLast: boolean }) => {
    const { title, description, href, icon: Icon } = item;
    const reversed = index % 2 !== 0;

    const cardClasses = cn(
        "group w-full sm:w-7/12 border rounded-lg p-6 transition-all duration-300",
        href &&
            "hover:scale-[1.05] hover:border-accent hover:-translate-y-0.5 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-background"
    );

    const cardContent = (
        <>
            <div className="size-10 rounded-md bg-accent-soft flex items-center justify-center mb-3">
                <Icon className="size-5 text-accent" />
            </div>
            <h3 className={cn("text-xl text-foreground font-semibold mb-2", href && "group-hover:text-accent transition-colors")}>
                {title}
            </h3>
            <p className="text-sm text-foreground-secondary">{description}</p>
        </>
    );

    return (
        <div className={cn("flex items-end gap-6", reversed ? "flex-row-reverse" : "flex-row")}>
            {href ? (
                <Link href={href} className={cardClasses}>
                    {cardContent}
                </Link>
            ) : (
                <div className={cardClasses}>{cardContent}</div>
            )}

            {!isLast && (
                <div className={cn(reversed && "transform scale-x-[-1]", "-mb-10 hidden sm:block")}>
                    <Image src="/images/home/rounded-arrow.png" alt="Arrow" width={8} height={8} />
                </div>
            )}
        </div>
    );
};

export default FeatureList;
