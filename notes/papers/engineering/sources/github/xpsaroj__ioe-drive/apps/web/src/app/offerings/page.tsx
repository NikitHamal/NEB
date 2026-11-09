"use client"
import { Suspense, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { Inbox, ListChecks, SlidersHorizontal } from "lucide-react";

import { SubjectOfferingCard } from "@/components/common/offering";
import { BookSpines, DEFAULT_SHELF_SPINES } from "@/components/decor";
import Select from "@/components/ui/Select";
import Loader from "@/components/ui/Loader";
import { useAuth } from "@clerk/nextjs";
import { useMe } from "@/hooks/queries/use-me";
import { usePrograms, useSubjectOfferings } from "@/hooks/queries/use-academics";
import { getErrorMessage } from "@/lib/errors";
import { Semester, SemesterLabel } from "@/types/entities";

const OfferingsBrowseContent = () => {
    const router = useRouter();
    const searchParams = useSearchParams();

    const { isLoaded: authLoaded, isSignedIn } = useAuth();
    const { data: userData, isPending: profilePending } = useMe();
    const profile = userData?.profile;

    const { data: programs, isPending: programsPending } = usePrograms();

    const urlProgramId = searchParams.get("programId");
    const urlSemester = searchParams.get("semester") as Semester | null;

    const programId = urlProgramId ? Number(urlProgramId) : undefined;
    const semester = urlSemester || undefined;

    const profileHasDefault = !!(profile?.programId && profile?.semester);
    const waitingForProfileDefault = !!isSignedIn && (!authLoaded || profilePending);
    // About to auto-redirect below - keep loading instead of flashing the filter prompt.
    const pendingAutoRedirect = !!isSignedIn && !profilePending && profileHasDefault && !urlProgramId && !urlSemester;

    // Default the filter from the signed-in user's profile, first landing with no URL selection.
    useEffect(() => {
        if (urlProgramId || urlSemester) return;
        if (!isSignedIn || profilePending) return;
        if (profile?.programId && profile?.semester) {
            const params = new URLSearchParams();
            params.set("programId", String(profile.programId));
            params.set("semester", profile.semester);
            router.replace(`/offerings?${params.toString()}`);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isSignedIn, profilePending, profile?.programId, profile?.semester, urlProgramId, urlSemester]);

    const { data: subjectOfferings, error: offeringsError, isPending: offeringsPending } = useSubjectOfferings(programId, semester);
    const hasOfferings = !!subjectOfferings && subjectOfferings.length > 0;

    const updateFilter = (next: { programId?: string; semester?: string }) => {
        const params = new URLSearchParams(searchParams.toString());

        if (next.programId !== undefined) {
            if (next.programId) params.set("programId", next.programId);
            else params.delete("programId");
        }

        if (next.semester !== undefined) {
            if (next.semester) params.set("semester", next.semester);
            else params.delete("semester");
        }

        router.replace(`/offerings?${params.toString()}`);
    };

    const pageHeader = (
        <div className="relative overflow-hidden rounded-lg border border-border bg-background-secondary p-6 md:p-8">
            <BookSpines spines={DEFAULT_SHELF_SPINES} />

            <div className="relative z-10 flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                <div className="max-w-md">
                    <h1 className="text-2xl md:text-3xl font-bold text-foreground">Curriculum Directory</h1>
                    <p className="mt-1 text-foreground-secondary">
                        Filter by program and semester to find specific subject details.
                    </p>
                </div>
                {hasOfferings && (
                    <div className="flex shrink-0 items-center gap-2 self-start rounded-lg border border-border bg-background px-3 py-2">
                        <ListChecks className="size-4 text-foreground-tertiary" />
                        <p className="font-display text-xs uppercase tracking-wide text-foreground-secondary">
                            Subjects: <span className="font-semibold text-foreground">{subjectOfferings.length}</span>
                        </p>
                    </div>
                )}
            </div>
        </div>
    );

    const filterBar = (
        <div className="flex flex-col border-b sm:flex-row">
            <div className="flex-1 p-4">
                <Select
                    label="Program"
                    placeholder="Select Program"
                    helperText={programsPending ? "Loading programs..." : "Select your department"}
                    value={programId ? String(programId) : ""}
                    disabled={programsPending}
                    onChange={(e) => updateFilter({ programId: e.target.value })}
                    options={(programs ?? []).map((prog) => ({
                        value: String(prog.id),
                        label: `${prog.code} - ${prog.name}`,
                    }))}
                />
            </div>

            <div className="flex-1 p-4">
                <Select
                    label="Semester"
                    placeholder="Select Semester"
                    helperText={programId ? "Choose your semester" : "Select a program first"}
                    value={semester ?? ""}
                    onChange={(e) => updateFilter({ semester: e.target.value })}
                    options={Object.keys(SemesterLabel).map((sem) => ({
                        value: sem,
                        label: `${SemesterLabel[sem as Semester]} ${+sem > 8 ? "(Architecture)" : ""}`,
                    }))}
                />
            </div>
        </div>
    );

    if (waitingForProfileDefault || pendingAutoRedirect) {
        return (
            <div className="min-h-screen bg-background text-foreground max-w-7xl mx-auto md:px-8 px-6 md:space-y-8 space-y-6">
                <div className="pt-6 md:pt-8">
                    {pageHeader}
                    <div className="mt-6">{filterBar}</div>
                </div>
                <div className="flex-1 flex items-center justify-center py-16">
                    <Loader text="Loading your subject offerings. Please wait." />
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background text-foreground max-w-7xl mx-auto md:px-8 px-6 md:space-y-8 space-y-6">
            <div className="pt-6 md:pt-8">
                {pageHeader}
                <div className="mt-6">{filterBar}</div>
                {isSignedIn && authLoaded && !profilePending && !profileHasDefault && (
                    <p className="text-xs text-foreground-tertiary mt-2">
                        Tip: set your program and semester in your{" "}
                        <Link href="/profile" className="underline hover:text-foreground">
                            profile
                        </Link>{" "}
                        to see your current semester here by default.
                    </p>
                )}
            </div>

            {!programId || !semester ? (
                <div className="flex-1 border border-border flex flex-col items-center justify-center gap-2 rounded-lg py-16">
                    <SlidersHorizontal className="size-5 text-foreground-tertiary" />
                    <p className="text-sm text-foreground-secondary">
                        Select a program and semester above to browse subject offerings.
                    </p>
                </div>
            ) : offeringsPending ? (
                <div className="flex-1 flex items-center justify-center py-16">
                    <Loader text="Loading subject offerings. Please wait." />
                </div>
            ) : offeringsError ? (
                <div className="flex-1 flex items-center justify-center py-16">
                    <p className="text-error">{getErrorMessage(offeringsError, "Couldn't load subject offerings. Please try again.")}</p>
                </div>
            ) : !hasOfferings ? (
                <div className="flex-1 border border-border flex flex-col items-center justify-center gap-2 rounded-lg py-16">
                    <Inbox className="size-5 text-foreground-tertiary" />
                    <p className="text-sm text-foreground-secondary">
                        No subjects offered for this program and semester.
                    </p>
                </div>
            ) : (
                <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 md:mb-8">
                    {subjectOfferings.map((offering) => (
                        <SubjectOfferingCard key={offering.id} offering={offering} />
                    ))}
                </div>
            )}
        </div>
    )
}

const OfferingsPage = () => {
    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading subject offerings. Please wait." />
            </div>
        }>
            <OfferingsBrowseContent />
        </Suspense>
    );
}

export default OfferingsPage;
