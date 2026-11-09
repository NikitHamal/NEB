import Link from "next/link";

import { UploaderSummary } from "@/types/api";
import { cn } from "@/utils/cn";
import UserAvatar from "./UserAvatar";

interface UploaderInfoProps {
    user?: UploaderSummary;
    subtitle?: string;
    /** `sm` for rows inside cards/tiles (default); `md` for page-level bylines. */
    size?: "sm" | "md";
    /** Renders as plain text instead of a link to the profile - for use inside an ancestor that's already a link/button, since HTML forbids nesting <a> inside <a>. */
    disableLink?: boolean;
}

const rowGap = {
    sm: "gap-2",
    md: "gap-3",
};

const nameSizes = {
    sm: "text-xs",
    md: "text-sm",
};

const subtitleSizes = {
    sm: "text-[10px]",
    md: "text-[11px]",
};

const UploaderInfo = ({ user, subtitle, size = "sm", disableLink = false }: UploaderInfoProps) => {
    const fullName = user?.fullName ?? "";

    const content = (
        <>
            <UserAvatar
                fullName={fullName}
                avatarUrl={user?.profile?.profilePictureUrl}
                size={size}
            />
            <span className="flex min-w-0 flex-col">
                <span
                    className={cn(
                        nameSizes[size],
                        "truncate font-medium text-foreground underline-offset-2 group-hover/uploader:underline"
                    )}
                >
                    {fullName || "Unknown User"}
                </span>
                {subtitle && (
                    // Same mono-caps voice as timestamps/eyebrow labels elsewhere (e.g. ResourcePreviewTile).
                    <span
                        className={cn(
                            subtitleSizes[size],
                            "truncate font-display uppercase tracking-wide text-foreground-tertiary"
                        )}
                    >
                        {subtitle}
                    </span>
                )}
            </span>
        </>
    );

    if (!user?.id || disableLink) {
        return (
            <span className={cn(rowGap[size], "flex min-w-0 items-center")}>
                {content}
            </span>
        );
    }

    return (
        // Named group so this link's hover doesn't also react to an ancestor `group` (e.g. a card).
        <Link
            href={`/users/${user.id}`}
            className={cn(
                rowGap[size],
                "group/uploader flex min-w-0 items-center rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-background"
            )}
        >
            {content}
        </Link>
    );
};

export default UploaderInfo;
