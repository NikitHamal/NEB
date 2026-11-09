"use client";

import { ClerkProvider } from "@clerk/nextjs";
import { dark } from "@clerk/themes";
import { useTheme } from "next-themes";

import { useMounted } from "@/hooks/use-mounted";

// Renders light until mount to avoid a hydration mismatch (resolvedTheme is only known client-side).
export function ClerkThemeProvider({ children }: { children: React.ReactNode }) {
    const { resolvedTheme } = useTheme();
    const mounted = useMounted();

    const isDark = mounted && resolvedTheme === "dark";

    return (
        <ClerkProvider appearance={{ baseTheme: isDark ? dark : undefined }}>
            {children}
        </ClerkProvider>
    );
}
