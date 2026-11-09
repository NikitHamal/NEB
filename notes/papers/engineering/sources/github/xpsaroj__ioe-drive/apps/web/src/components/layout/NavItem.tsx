import type { LucideIcon } from "lucide-react";

import Button from "@/components/ui/Button";
import { cn } from "@/utils/cn";

interface NavItemProps {
    href: string;
    icon: LucideIcon;
    name: string;
    active: boolean;
    onClick?: () => void;
    /** E.g. an unread messages count - omitted or 0 renders no badge at all. */
    badgeCount?: number;
}

// Shared by the desktop sidebar (Navbar) and mobile drawer (MobileNav) so both stay visually identical.
const NavItem = ({ href, icon: Icon, name, active, onClick, badgeCount }: NavItemProps) => {
    return (
        <Button
            href={href}
            onClick={onClick}
            variant="ghost"
            className={cn(
                "w-full justify-start border-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-background",
                active
                    ? "bg-accent-soft text-accent hover:bg-accent-soft"
                    : "text-foreground-secondary hover:text-foreground"
            )}
        >
            <div className="flex flex-1 gap-2.5 items-center">
                <Icon className={cn("size-4.5", active && "text-accent")} />
                <span className={cn("text-sm flex-1", active ? "font-semibold" : "font-medium")}>{name}</span>
                {!!badgeCount && (
                    <span className="flex min-w-5 items-center justify-center rounded-full bg-accent px-1.5 py-0.5 text-[11px] font-semibold text-accent-foreground">
                        {badgeCount}
                    </span>
                )}
            </div>
        </Button>
    );
};

export default NavItem;
