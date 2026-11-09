"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

import Loader from "@/components/ui/Loader";
import { useMe } from "@/hooks/queries/use-me";
import { UserRole } from "@/types/entities";

// UX-only redirect for non-admins - the real boundary is the server-side @Roles("ADMIN") guard.
const AdminGate = ({ children }: { children: React.ReactNode }) => {
    const { data: userData, isPending } = useMe();
    const router = useRouter();

    const isAdmin = userData?.role === UserRole.ADMIN;

    useEffect(() => {
        if (!isPending && userData && !isAdmin) {
            router.replace("/dashboard");
        }
    }, [isPending, userData, isAdmin, router]);

    if (isPending || !userData || !isAdmin) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading admin tools. Please wait." />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto space-y-6">
            <div className="space-y-2 pb-2">
                <p className="font-display text-xs tracking-[0.2em] uppercase text-foreground-tertiary">
                    Platform Administration
                </p>
                <h1 className="text-2xl md:text-3xl font-bold text-foreground">Admin</h1>
                <p className="text-foreground-secondary text-base leading-relaxed">
                    Manage user roles.
                </p>
            </div>

            {children}
        </div>
    );
};

export default AdminGate;
