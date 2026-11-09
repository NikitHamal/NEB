"use client";
import { useMe } from "@/hooks/queries/use-me";
import { usePrograms } from "@/hooks/queries/use-academics";

export function AppDataInitializer({
    children
}: {
    children: React.ReactNode
}) {
    // Preload essential user data and programs on app initialization
    const { } = useMe();
    const { } = usePrograms();

    return <>{children}</>;
}