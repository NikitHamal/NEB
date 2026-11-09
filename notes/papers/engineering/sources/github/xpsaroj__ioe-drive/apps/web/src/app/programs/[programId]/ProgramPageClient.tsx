"use client"
import { use } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft, ListChecks } from "lucide-react";

import Button from "@/components/ui/Button";
import { EntityPageStateHandler, type BreadcrumbItem } from "@/components/layout";
import { SubjectOfferingCard, ProgramCard } from "@/components/common/offering";
import { usePrograms, useSubjectOfferings } from "@/hooks/queries/use-academics";
import { SemesterLabel, type Semester, type SubjectOfferingWithSubject } from "@/types/entities";

interface ProgramPageClientProps {
    params: Promise<{ programId: string }>;
}

// Offerings arrive pre-sorted by semester from the backend, so a single linear pass
// clusters them into semester sections without needing to re-sort here.
const groupBySemester = (offerings: SubjectOfferingWithSubject[]) => {
    const groups: { semester: Semester; offerings: SubjectOfferingWithSubject[] }[] = [];
    for (const offering of offerings) {
        const last = groups[groups.length - 1];
        if (last && last.semester === offering.semester) {
            last.offerings.push(offering);
        } else {
            groups.push({ semester: offering.semester, offerings: [offering] });
        }
    }
    return groups;
};

const ProgramPageClient = ({ params }: ProgramPageClientProps) => {
    const router = useRouter();
    const { programId: programIdParam } = use(params);
    const programId = Number(programIdParam);

    const { data: programs, isPending: programsPending, error: programsError } = usePrograms();
    const program = programs?.find((p) => p.id === programId);

    const { data: offerings, isPending: offeringsPending, error: offeringsError } = useSubjectOfferings(programId);

    const isPending = programsPending || (!!program && offeringsPending);
    const error = programsError || offeringsError;
    const isEmpty = !programsPending && !program;

    const breadcrumbs: BreadcrumbItem[] = [
        { label: "Programs", href: "/programs" },
        { label: program?.code ?? "Program" },
    ];

    const backButton = (
        <Button
            icon={<ChevronLeft className="size-4" />}
            iconOnly
            variant="ghost"
            size="xs"
            className="border border-border shrink-0"
            onClick={() => router.back()}
            aria-label="Go back"
        />
    );

    const title = program
        ? program.code !== "SH"
            ? `Bachelor in ${program.name} (${program.code})`
            : program.name
        : "Program Details";

    const semesterGroups = groupBySemester(offerings ?? []);

    return (
        <EntityPageStateHandler
            title={title}
            breadcrumbs={breadcrumbs}
            beforeBreadcrumb={backButton}
            actions={
                program ? (
                    <Button href={`/resources?programId=${program.id}&semester=1`} icon={<ListChecks className="size-4" />}>
                        View resources for this program
                    </Button>
                ) : undefined
            }
            isPending={isPending}
            error={error}
            isEmpty={isEmpty}
            loaderText="Loading program details. Please wait."
            emptyTitle="Program not found"
            emptyDescription="This program may not exist, or the link you followed is incorrect."
            emptyButtonText="Browse All Programs"
            emptyButtonHref="/programs"
        >
            <div className="space-y-8">
                {program && <ProgramCard program={program} />}

                {semesterGroups.length === 0 ? (
                    <div className="flex flex-col items-center justify-center gap-2 rounded-lg border border-border py-16">
                        <ListChecks className="size-5 text-foreground-tertiary" />
                        <p className="text-sm text-foreground-secondary">
                            No subjects have been added for this program yet.
                        </p>
                    </div>
                ) : (
                    semesterGroups.map((group) => (
                        <div key={group.semester}>
                            <h2 className="mb-3 font-display text-sm font-semibold uppercase tracking-wide text-foreground-secondary">
                                {SemesterLabel[group.semester]} Semester
                            </h2>
                            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                                {group.offerings.map((offering) => (
                                    <SubjectOfferingCard key={offering.id} offering={offering} />
                                ))}
                            </div>
                        </div>
                    ))
                )}
            </div>
        </EntityPageStateHandler>
    );
};

export default ProgramPageClient;
