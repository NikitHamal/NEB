import Image from "next/image";
import { User2 } from "lucide-react";

import { cn } from "@/utils/cn";

interface UserAvatarProps {
    fullName: string;
    avatarUrl?: string;
    size?: "sm" | "md" | "lg" | "xl";
    className?: string;
}

const avatarSizes = {
    sm: "size-8",
    md: "size-10",
    lg: "size-24",
    xl: "size-32",
};

const imageSizes = {
    sm: 32,
    md: 40,
    lg: 96,
    xl: 128,
};

const initialsSizes = {
    sm: "text-[10px]",
    md: "text-xs",
    lg: "text-3xl",
    xl: "text-4xl",
};

const iconPadding = {
    sm: "p-1.5",
    md: "p-2",
    lg: "p-6",
    xl: "p-8",
};

/** "Saroj Here" -> "SH"; single-word names fall back to their first letter. */
const getInitials = (fullName: string) => {
    const parts = fullName.trim().split(/\s+/).filter(Boolean);
    if (parts.length === 0) return "";
    const first = parts[0][0];
    const last = parts.length > 1 ? parts[parts.length - 1][0] : "";
    return (first + last).toUpperCase();
};

const UserAvatar = ({
    fullName,
    avatarUrl,
    size = "md",
    className,
}: UserAvatarProps) => {
    const initials = getInitials(fullName);

    return (
        <span
            className={cn(
                avatarSizes[size],
                "relative flex shrink-0 select-none items-center justify-center overflow-hidden rounded-full border bg-background-tertiary text-foreground-secondary",
                className,
            )}
        >
            {avatarUrl ? (
                <Image
                    src={avatarUrl}
                    alt={fullName || "User avatar"}
                    width={imageSizes[size]}
                    height={imageSizes[size]}
                    className="size-full object-cover"
                />
            ) : initials ? (
                <span className={cn(initialsSizes[size], "font-display font-medium leading-none")}>
                    {initials}
                </span>
            ) : (
                <User2 className={cn("size-full", iconPadding[size])} />
            )}
        </span>
    );
};

export default UserAvatar;
