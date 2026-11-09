"use client"
import { useUser } from "@clerk/nextjs"

import StatStrip from "@/components/ui/StatStrip"
import { ScatteredCodeTiles, type ScatteredTile } from "@/components/decor"
import { useMe, useUploadedResources, useBookmarkedResourceIds, useRecentResources } from "@/hooks/queries/use-me"
import { SemesterLabel } from "@/types/entities"

// Kept to a thin top band so it never sits behind the welcome text or stats.
const DASHBOARD_HERO_TILES: ScatteredTile[] = [
    { code: "BCT", top: "6%", left: "10%", rotate: -6, size: "size-8 text-[10px]" },
    { code: "BEE", top: "12%", left: "32%", rotate: 5, size: "size-7 text-[9px]" },
    { code: "BEX", top: "6%", left: "56%", rotate: 4, size: "size-8 text-[10px]", solid: true },
    { code: "BCE", top: "12%", left: "80%", rotate: -4, size: "size-7 text-[9px]" },
]

const DashboardHero = () => {
    const { user } = useUser()
    const { data: userData } = useMe();
    const profile = userData?.profile;

    const { data: uploaded } = useUploadedResources(1);
    const { data: bookmarkedIds } = useBookmarkedResourceIds();
    const { data: recent } = useRecentResources(1);

    const hasProfile = !!(profile?.program && profile?.semester);

    return (
        <div className="relative overflow-hidden rounded-lg border border-border bg-background-secondary p-6 sm:min-h-[9.5rem]">
            <ScatteredCodeTiles tiles={DASHBOARD_HERO_TILES} className="hidden sm:block" />

            <div className="relative z-10 flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
                <div>
                    {hasProfile && profile?.program && profile?.semester && (
                        <span className="inline-block mb-3 rounded-full bg-background-tertiary px-3 py-1 font-display text-[11px] uppercase tracking-wide text-foreground-secondary">
                            {profile.program.code}, {SemesterLabel[profile.semester]} Semester
                        </span>
                    )}
                    <h1 className="text-2xl md:text-3xl font-bold text-foreground">Welcome back, {user?.firstName || "User"}.</h1>
                    <p className="text-foreground-secondary mt-2">
                        You&apos;re making steady progress this week. Pick up right where you left off.
                    </p>
                </div>

                <StatStrip
                    variant="inline"
                    className="border border-border rounded-lg px-5 py-3 bg-background"
                    items={[
                        { href: "/library/uploads", label: "Uploaded", value: uploaded?.meta?.total },
                        { href: "/library/bookmarks", label: "Bookmarked", value: bookmarkedIds?.length },
                        { href: "/library/recent", label: "Viewed", value: recent?.meta?.total },
                    ]}
                />
            </div>
        </div>
    )
}

export default DashboardHero
