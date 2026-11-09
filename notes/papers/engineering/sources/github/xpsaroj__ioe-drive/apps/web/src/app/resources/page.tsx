"use client"
import { Suspense, useEffect, useRef, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { ChevronRight, ChevronDown, Inbox, Search, SlidersHorizontal, UploadCloud } from "lucide-react";

import { SubjectDetails } from "@/components/common/offering";
import { ResourceList, ResourceCard } from "@/components/common/resources";
import SearchDialog from "@/components/layout/SearchDialog";
import Pagination from "@/components/ui/Pagination";
import Button from "@/components/ui/Button";
import Select from "@/components/ui/Select";
import Loader from "@/components/ui/Loader";
import { getErrorMessage } from "@/lib/errors";
import { useAuth } from "@clerk/nextjs";
import { useMe } from "@/hooks/queries/use-me";
import { usePrograms, useSubjectOfferings } from "@/hooks/queries/use-academics";
import { useResourcesBySubjectOfferingId } from "@/hooks/queries/use-resources";
import { usePageParam } from "@/hooks/use-page-param";
import { Semester, SemesterLabel, SubjectOfferingWithSubject } from "@/types/entities";

const ResourcesBrowseContent = () => {
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
            router.replace(`/resources?${params.toString()}`);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [isSignedIn, profilePending, profile?.programId, profile?.semester, urlProgramId, urlSemester]);

    const [selectedSubject, setSelectedSubject] = useState<SubjectOfferingWithSubject | null>(null);
    const [showSubjectDetails, setShowSubjectDetails] = useState(false);
    const [showFilters, setShowFilters] = useState(true);
    const [searchOpen, setSearchOpen] = useState(false);

    // Reset the in-page subject-tab selection whenever the program/semester filter changes
    useEffect(() => {
        setSelectedSubject(null);
        setShowSubjectDetails(false);
    }, [programId, semester]);

    const { data: subjectOfferings, error: offeringsError, isPending: offeringsPending } = useSubjectOfferings(programId, semester);

    // ?offeringId= (e.g. from an offering's "Browse Resources" button) beats the first-in-list default.
    const urlOfferingId = searchParams.get("offeringId");
    const linkedOffering = urlOfferingId ? subjectOfferings?.find((s) => String(s.id) === urlOfferingId) : undefined;

    const currentSubject = selectedSubject?.subject ?? linkedOffering?.subject ?? subjectOfferings?.[0]?.subject;
    const currentOfferingId = selectedSubject?.id ?? linkedOffering?.id ?? subjectOfferings?.[0]?.id;

    const { page, setPage } = usePageParam();
    // Reset to page 1 on a real subject change (not the initial mount), so a shared ?page=N link still works on first load.
    const previousOfferingIdRef = useRef<number | undefined>(undefined);
    useEffect(() => {
        if (
            previousOfferingIdRef.current !== undefined &&
            previousOfferingIdRef.current !== currentOfferingId
        ) {
            setPage(1);
        }
        previousOfferingIdRef.current = currentOfferingId;
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [currentOfferingId]);

    const {
        data: resourcesData,
        isLoading: resourcesLoading,
        error: resourcesError,
        isPlaceholderData: resourcesPlaceholder,
    } = useResourcesBySubjectOfferingId(currentOfferingId, page);
    const resources = resourcesData?.items;

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

        router.replace(`/resources?${params.toString()}`);
    };

    const hasOfferings = !!subjectOfferings && subjectOfferings.length > 0;

    const pageHeader = (
        <div className="flex items-start justify-between gap-4 pb-6 border-b border-border">
            <div>
                <h1 className="text-2xl md:text-3xl font-bold text-foreground">Resource Explorer</h1>
                <p className="text-foreground-secondary mt-1">Browse, filter, and access academic materials.</p>
            </div>
            <div className="flex items-center gap-2 shrink-0">
                <Button
                    variant={showFilters ? "secondary" : "primary"}
                    size="sm"
                    iconOnly
                    icon={<SlidersHorizontal className="size-4" />}
                    onClick={() => setShowFilters((prev) => !prev)}
                    aria-label={showFilters ? "Hide filters" : "Show filters"}
                />
                <Button
                    variant="secondary"
                    size="sm"
                    iconOnly
                    icon={<Search className="size-4" />}
                    onClick={() => setSearchOpen(true)}
                    aria-label="Search"
                />
            </div>
        </div>
    );

    const filterBar = (
        <div className="flex flex-col sm:flex-row border-b border-border">
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

            <div className="flex-1 p-4">
                <Select
                    label="Subject"
                    placeholder="Select Subject"
                    helperText={
                        !programId || !semester
                            ? "Select a program and semester first"
                            : offeringsPending
                                ? "Loading subjects..."
                                : "Pick a course"
                    }
                    value={currentOfferingId ? String(currentOfferingId) : ""}
                    disabled={!hasOfferings}
                    onChange={(e) => {
                        const subject = subjectOfferings?.find((s) => String(s.id) === e.target.value);
                        if (subject) setSelectedSubject(subject);
                    }}
                    options={(subjectOfferings ?? []).map((s) => ({
                        value: String(s.id),
                        label: `${s.subject.code} - ${s.subject.name}`,
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
                    <Loader text="Loading your resources. Please wait." />
                </div>
                {searchOpen && <SearchDialog isOpen={searchOpen} onClose={() => setSearchOpen(false)} />}
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background text-foreground max-w-7xl mx-auto md:px-8 px-6 md:space-y-8 space-y-6">
            <div className="pt-6 md:pt-8">{pageHeader}</div>

            {showFilters && (
                <div className="sticky md:top-0 z-10 bg-background/40 backdrop-blur-sm">
                    {filterBar}
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
            )}

            {!programId || !semester ? (
                <div className="flex-1 border flex flex-col items-center justify-center gap-2 rounded-lg py-16">
                    <SlidersHorizontal className="size-5 text-foreground-tertiary" />
                    <p className="text-sm text-foreground-secondary">
                        Select a program and semester above to browse resources.
                    </p>
                </div>
            ) : offeringsPending ? (
                <div className="flex-1 flex items-center justify-center py-16">
                    <Loader text="Loading resources. Please wait." />
                </div>
            ) : offeringsError ? (
                <div className="flex-1 flex items-center justify-center py-16">
                    <p className="text-error">{getErrorMessage(offeringsError, "Couldn't load resources. Please try again.")}</p>
                </div>
            ) : !hasOfferings ? (
                <div className="flex-1 border flex flex-col items-center justify-center gap-2 rounded-lg py-16">
                    <Inbox className="size-5 text-foreground-tertiary" />
                    <p className="text-sm text-foreground-secondary">
                        No resources available for this program and semester.
                    </p>
                </div>
            ) : (
                <>
                    <div>
                        <div className="flex flex-row items-center gap-2">
                            <Button
                                variant="ghost"
                                size="xs"
                                iconOnly
                                icon={showSubjectDetails ? <ChevronDown className="size-4" /> : <ChevronRight className="size-4" />}
                                onClick={() => setShowSubjectDetails((prev) => !prev)}
                                className="border border-border"
                            />
                            <h3 className="text-lg font-semibold text-foreground">Subject Details</h3>
                        </div>
                        {showSubjectDetails && currentSubject && (
                            <div className="mt-3">
                                <SubjectDetails
                                    subject={currentSubject}
                                />
                            </div>
                        )}
                    </div>

                    <div className="pb-6 md:pb-8 space-y-6">
                        <h3 className="text-lg font-semibold text-foreground">Available Resources</h3>
                        <ResourceList
                            resources={resources || []}
                            // isLoading alone misses subject/page switches: placeholderData keeps the
                            // previous query's (stale, possibly empty) resources on screen with no
                            // indication a new fetch is in flight - isPlaceholderData covers that gap.
                            loading={resourcesLoading || resourcesPlaceholder}
                            error={resourcesError ? getErrorMessage(resourcesError, "Couldn't load resources. Please try again.") : null}
                            renderItem={(resource) =>
                                <ResourceCard
                                    resource={resource}
                                />
                            }
                            emptyState={
                                <>
                                    <span className="flex size-10 items-center justify-center rounded-full bg-accent-soft text-accent">
                                        <UploadCloud className="size-5" />
                                    </span>
                                    <div className="flex flex-col items-center">
                                        <p className="text-sm font-medium text-foreground">No resources yet</p>
                                        <p className="text-sm text-foreground-secondary mt-1">Be the first to share one for this subject.</p>
                                    </div>
                                    <Button href="/resources/share" size="sm" className="mt-1">
                                        Share a Resource
                                    </Button>
                                </>
                            }
                        />
                        <Pagination
                            page={page}
                            totalPages={resourcesData?.meta?.totalPages ?? 1}
                            onPageChange={setPage}
                            disabled={resourcesPlaceholder}
                        />
                    </div>
                </>
            )}

            {searchOpen && <SearchDialog isOpen={searchOpen} onClose={() => setSearchOpen(false)} />}
        </div>
    )
}

const ResourcesPage = () => {
    return (
        <Suspense fallback={
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <Loader text="Loading resources. Please wait." />
            </div>
        }>
            <ResourcesBrowseContent />
        </Suspense>
    );
}

export default ResourcesPage;
