"use client";

import Link from "next/link";
import Image from "next/image";
import { useAuth } from '@clerk/nextjs';
import { useTheme } from "next-themes";

import { useMounted } from "@/hooks/use-mounted";

interface LogoProps {
    /** Defaults to the variant matching the site's current theme when omitted. */
    theme?: "light" | "dark";
    size?: number;
    bg?: boolean;
    /** Renders just the mark (no wrapping Link) - for callers nesting it in their own link. */
    disableLink?: boolean;
}

export default function Logo({
    theme,
    size = 6,
    bg = true,
    disableLink = false,
}: LogoProps) {
    const { isSignedIn } = useAuth();
    const { resolvedTheme } = useTheme();
    const mounted = useMounted();

    // Variant is the *opposite* of the site's theme (a dark mark for a light background).
    const siteIsDark = mounted && resolvedTheme === "dark";
    const logoTheme = theme ?? (siteIsDark ? "light" : "dark");

    const imagePath = `/logo/logo-${logoTheme}${bg ? "" : "-no-bg"}.svg`;

    const image = (
        <Image
            src={imagePath}
            // Decorative when paired with a wordmark, whose text is the accessible name instead.
            alt={disableLink ? "" : "IOE Drive Logo"}
            preload={true}
            width={size * 16}
            height={size * 16}
        />
    );

    if (disableLink) return image;

    return (
        <Link href={isSignedIn ? "/dashboard" : "/"}>
            {image}
        </Link>
    )
}
