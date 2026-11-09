import { Wrench } from "lucide-react";

import Badge from "@/components/ui/Badge";

const CommunityPage = () => {
    return (
        <div className="min-h-screen flex flex-col bg-background text-foreground max-w-7xl mx-auto md:p-8 p-6 space-y-6">
            <div className="pb-6 border-b border-border">
                <div className="flex flex-wrap items-center gap-3">
                    <h1 className="text-2xl md:text-3xl font-bold text-foreground">Community</h1>
                    <Badge variant="warning" size="sm">Coming Soon</Badge>
                </div>
                <p className="text-foreground-secondary mt-2 max-w-2xl">
                    Connect with peers, ask questions, and share notes across programs and
                    semesters.
                </p>
            </div>

            <div className="flex flex-1 items-center justify-center rounded-lg border border-border p-6">
                <div className="flex max-w-xs flex-col items-center gap-3 text-center">
                    <span className="flex size-11 items-center justify-center rounded-full bg-accent-soft text-accent">
                        <Wrench className="size-5" />
                    </span>
                    <div>
                        <p className="font-semibold text-foreground">Feed under construction</p>
                        <p className="mt-1 text-sm text-foreground-secondary">
                            This feature is on its way. Check back soon.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CommunityPage;
