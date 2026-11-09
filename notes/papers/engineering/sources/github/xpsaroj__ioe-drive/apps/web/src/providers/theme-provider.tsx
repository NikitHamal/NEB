"use client";

import { ThemeProvider as NextThemesProvider, type ThemeProviderProps } from "next-themes";

// Wraps next-themes' ThemeProvider so the app imports it from providers/ rather than next-themes directly.
export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
    return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}
