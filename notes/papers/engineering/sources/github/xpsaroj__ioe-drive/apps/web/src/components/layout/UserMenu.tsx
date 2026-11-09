import { UserButton, ClerkLoading, ClerkLoaded, useClerk } from "@clerk/nextjs";
import { useRef } from "react";

import { useMe } from "@/hooks/queries/use-me";
import { UserAvatar } from "@/components/common/user";
import { SemesterLabel } from "@/types/entities";

export const UserMenu = () => {
    const { user } = useClerk();
    const { data: userData, isLoading, error } = useMe();
    const profile = userData ? userData?.profile : null;

    const buttonRef = useRef<HTMLDivElement>(null);

    const handleOpenMenu = () => {
        const btn = buttonRef.current?.querySelector("button");
        btn?.click(); // triggers Clerk popup
    };

    // e.g. "6th · BCT · Pulchowk" - semester, program code, college's first word.
    const profileSummary = [
        profile?.semester && SemesterLabel[profile.semester],
        profile?.program?.code,
        profile?.college?.trim().split(" ")[0],
    ].filter(Boolean).join(", ");

    return (
        <div
            onClick={handleOpenMenu}
            className="relative flex min-w-0 cursor-pointer items-center gap-2.5 overflow-hidden"
        >
            <ClerkLoading>
                <span className="size-10 shrink-0 animate-pulse rounded-full border bg-background-tertiary" />
            </ClerkLoading>
            <ClerkLoaded>
                <UserAvatar
                    fullName={user?.fullName ?? ""}
                    avatarUrl={user?.imageUrl}
                    size="md"
                />
            </ClerkLoaded>

            <div className="flex min-w-0 flex-col">
                <span className="truncate text-sm font-medium text-foreground">
                    {user?.fullName || "User"}
                </span>
                {isLoading ? (
                    <span className="font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">
                        Loading...
                    </span>
                ) : error ? (
                    <span className="font-display text-[11px] uppercase tracking-wide text-error">
                        Profile unavailable
                    </span>
                ) : profileSummary && (
                    <span className="truncate font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">
                        {profileSummary}
                    </span>
                )}
            </div>

            <div ref={buttonRef} className="absolute bottom-0 right-0 opacity-0 -mb-2 pointer-events-none">
                <UserButton />
            </div>
        </div>
    );
};
