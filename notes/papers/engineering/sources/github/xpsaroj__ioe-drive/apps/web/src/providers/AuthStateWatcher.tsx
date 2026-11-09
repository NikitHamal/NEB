"use client";
import { useEffect } from "react";
import { useAuth } from "@clerk/nextjs"
import { useQueryClient } from "@tanstack/react-query";

import { meKeys } from "@/hooks/queries/use-me";
import { academicsKeys } from "@/hooks/queries/use-academics";
import { messagingKeys } from "@/hooks/queries/use-messaging";

export function AuthStateWatcher({
    children
}: {
    children: React.ReactNode
}) {
    const { isSignedIn } = useAuth();
    const queryClient = useQueryClient();

    useEffect(() => {
        if (!isSignedIn) {
            queryClient.removeQueries({ queryKey: meKeys.all });
            queryClient.removeQueries({ queryKey: [...academicsKeys.all, "subject-offerings"] });
            queryClient.removeQueries({ queryKey: messagingKeys.all });
        }
    }, [isSignedIn, queryClient]);

    return <>{children}</>;
}