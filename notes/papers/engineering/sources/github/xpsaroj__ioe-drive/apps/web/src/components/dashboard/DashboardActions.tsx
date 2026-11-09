"use client";
import Link from "next/link";
import { UploadCloud, Lightbulb, FileText, ArrowRight, Sparkles } from "lucide-react";

import { DotGrid } from "@/components/decor";
import { TYPE_BADGE_COLOR } from "@/components/common/resources";
import Button from "@/components/ui/Button";
import { useRecentResources } from "@/hooks/queries/use-me";
import { useSimilarResources } from "@/hooks/queries/use-resources";
import { ResourceTypeLabel } from "@/types/entities";

const DashboardActions = () => {
    const { data: recentData, isPending: recentPending } = useRecentResources(1);
    const recentItem = recentData?.items[0];

    const { data: similar, isPending: similarPending } = useSimilarResources(recentItem?.resourceId ?? 0, 1);
    const recommendation = similar?.[0];

    const isPending = recentPending || (!!recentItem && similarPending);

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <Link
                href="/resources/share"
                className="group flex flex-col items-center justify-center gap-3 rounded-lg border border-border bg-background-secondary px-6 py-10 text-center transition-colors duration-150 hover:border-accent hover:bg-background-tertiary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-background"
            >
                <span className="flex size-11 items-center justify-center rounded-full bg-accent text-accent-foreground">
                    <UploadCloud className="size-5" />
                </span>
                <span className="text-base font-semibold text-foreground">Upload Notes</span>
                <span className="text-sm text-foreground-secondary">
                    Share notes, past questions, or study guides with your batch.
                </span>
            </Link>

            <div className="relative overflow-hidden lg:col-span-2 rounded-lg border border-border bg-background-secondary p-6">
                <DotGrid />

                <div className="relative z-10 h-full flex flex-col">
                    <div className="flex items-center gap-2 text-sm text-foreground-secondary mb-4">
                        <Lightbulb className="size-4" />
                        <span>Recommended for you</span>
                    </div>

                    <div className="flex-1 flex flex-col justify-center">
                        {isPending ? (
                            <div className="h-16 animate-pulse rounded-lg bg-skeleton-base" />
                        ) : recommendation && recentItem ? (
                            <>
                                <p className="text-sm text-foreground-secondary mb-4">
                                    Because you viewed{" "}
                                    <span className="text-foreground font-medium">{recentItem.resource.title}</span>
                                </p>
                                <Link
                                    href={`/resources/r/${recommendation.id}`}
                                    className="flex items-center justify-between gap-4 rounded-lg bg-background px-4 py-3 transition-colors hover:bg-background-hover"
                                >
                                    <div className="flex items-center gap-3 min-w-0">
                                        <span className={`flex size-9 items-center justify-center rounded-full shrink-0 ${TYPE_BADGE_COLOR[recommendation.type].bg} ${TYPE_BADGE_COLOR[recommendation.type].text}`}>
                                            <FileText className="size-4" />
                                        </span>
                                        <div className="min-w-0">
                                            <p className="text-sm font-semibold text-foreground truncate">{recommendation.title}</p>
                                            <p className="text-xs text-foreground-secondary">
                                                {ResourceTypeLabel[recommendation.type]}
                                            </p>
                                        </div>
                                    </div>
                                    <ArrowRight className="size-4 text-foreground-secondary shrink-0" />
                                </Link>
                            </>
                        ) : (
                            <div className="flex flex-col items-center justify-center gap-3 text-center">
                                <span className="flex size-11 items-center justify-center rounded-full bg-accent-soft text-accent">
                                    <Sparkles className="size-5" />
                                </span>
                                <div>
                                    <p className="text-sm font-medium text-foreground">No recommendations yet</p>
                                    <p className="text-sm text-foreground-secondary mt-1">
                                        Browse a few resources and we&apos;ll start surfacing picks tailored to you here.
                                    </p>
                                </div>
                                <Button href="/resources" size="sm" variant="secondary" className="mt-1">
                                    Browse resources
                                </Button>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DashboardActions;
