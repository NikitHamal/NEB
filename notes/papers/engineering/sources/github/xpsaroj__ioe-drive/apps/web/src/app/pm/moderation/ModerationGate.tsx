"use client";
import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import clsx from "clsx";

import Loader from "@/components/ui/Loader";
import { useMe } from "@/hooks/queries/use-me";
import { isModeratorOrAdmin } from "@/types/entities";

const TABS = [
    { label: "Pending Resources", href: "/pm/moderation/resources/pending" },
    { label: "Resource Reports", href: "/pm/moderation/resources/reports" },
    { label: "Pending Listings", href: "/pm/moderation/listings/pending" },
    { label: "Marketplace Reports", href: "/pm/moderation/listings/reports" },
];

// UX-only redirect for non-moderators - the real boundary is the server-side @Roles guard.
const ModerationGate = ({ children }: { children: React.ReactNode }) => {
    const { data: userData, isPending } = useMe();
    const router = useRouter();
    const pathname = usePathname();

    const isModerator = isModeratorOrAdmin(userData?.role);

    useEffect(() => {
        if (!isPending && userData && !isModerator) {
            router.replace("/dashboard");
        }
    }, [isPending, userData, isModerator, router]);

    if (isPending || !userData || !isModerator) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading moderation tools. Please wait." />
            </div>
        );
    }

    return (
        <div className="min-h-screen flex flex-col bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto space-y-6">
            <div className="space-y-2 pb-2">
                <p className="font-display text-xs tracking-[0.2em] uppercase text-foreground-tertiary">
                    Platform Moderation
                </p>
                <h1 className="text-2xl md:text-3xl font-bold text-foreground">Moderation</h1>
                <p className="text-foreground-secondary text-base leading-relaxed">
                    Review pending resource uploads, resource reports, pending marketplace listings,
                    and marketplace listing reports.
                </p>
            </div>

            <div className="flex gap-1 border-b border-border">
                {TABS.map((tab) => (
                    <Link
                        key={tab.href}
                        href={tab.href}
                        className={clsx(
                            "px-4 py-2 -mb-px border-b-2 text-sm font-medium transition-colors",
                            pathname.startsWith(tab.href)
                                ? "border-foreground text-foreground"
                                : "border-transparent text-foreground-secondary hover:text-foreground"
                        )}
                    >
                        {tab.label}
                    </Link>
                ))}
            </div>

                {children}
        </div>
    );
};

export default ModerationGate;
