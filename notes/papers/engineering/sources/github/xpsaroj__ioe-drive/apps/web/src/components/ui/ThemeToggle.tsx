"use client";

import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

import { useMounted } from "@/hooks/use-mounted";
import Button from "./Button";

// Renders a neutral (light-mode) icon until mounted, since resolved theme isn't known during SSR.
export default function ThemeToggle() {
    const { resolvedTheme, setTheme } = useTheme();
    const mounted = useMounted();

    const isDark = mounted && resolvedTheme === "dark";

    return (
        <Button
            variant="ghost"
            size="sm"
            iconOnly
            aria-label={mounted ? `Switch to ${isDark ? "light" : "dark"} mode` : "Toggle theme"}
            onClick={() => setTheme(isDark ? "light" : "dark")}
            icon={isDark ? <Sun className="size-5" /> : <Moon className="size-5" />}
            className=""
        />
    );
}
