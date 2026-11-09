import { BookOpen } from "lucide-react";

import SubjectHardnessBadge from "./SubjectHardnessBadge";
import ProgramCard from "./ProgramCard";
import Button from "@/components/ui/Button";
import type { SubjectWithProgramAndMarks } from "@/types/entities";

const SubjectDetails = ({ subject }: { subject: SubjectWithProgramAndMarks }) => {
    const { code, name, description, syllabusUrl, hardnessLevel, program, marks } = subject;

    const marksTotal = marks
        ? marks.theoryFinal + marks.theoryAssessment + marks.practicalFinal + marks.practicalAssessment
        : 0;

    return (
        <div className="space-y-5 rounded-lg border border-border p-6">
            <div className="flex items-start justify-between gap-4">
                <div className="min-w-0">
                    <p className="font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                        {code}
                    </p>
                    <h2 className="text-xl font-bold text-foreground">{name}</h2>
                </div>
                <SubjectHardnessBadge level={hardnessLevel} className="shrink-0" />
            </div>

            {description && (
                <p className="text-sm sm:text-base leading-relaxed text-foreground-secondary">{description}</p>
            )}

            {marks && (
                <div className="border-t border-border pt-4">
                    <p className="mb-3 font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                        Marks Distribution
                    </p>
                    <div className="flex flex-col md:flex-row gap-3">
                        <div className="rounded-lg border border-border p-3 flex-1">
                            <p className="mb-2 text-sm font-semibold text-foreground">Theory</p>
                            <div className="flex flex-col gap-1.5">
                                <div className="flex items-center justify-between">
                                    <span className="text-sm text-foreground-secondary">Final</span>
                                    <span className="text-sm font-medium text-foreground">{marks.theoryFinal}</span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <span className="text-sm text-foreground-secondary">Assessment</span>
                                    <span className="text-sm font-medium text-foreground">{marks.theoryAssessment}</span>
                                </div>
                            </div>
                        </div>
                        <div className="rounded-lg border border-border p-3 flex-1">
                            <p className="mb-2 text-sm font-semibold text-foreground">Practical</p>
                            <div className="flex flex-col gap-1.5">
                                <div className="flex items-center justify-between">
                                    <span className="text-sm text-foreground-secondary">Final</span>
                                    <span className="text-sm font-medium text-foreground">{marks.practicalFinal}</span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <span className="text-sm text-foreground-secondary">Assessment</span>
                                    <span className="text-sm font-medium text-foreground">{marks.practicalAssessment}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="mt-3 flex flex-col md:flex-row items-center justify-between gap-3">
                        <div className="text-sm text-foreground-secondary border-accent/20 bg-accent-soft p-3 flex-1 rounded-lg flex items-center justify-between w-full">
                            <span className="text-base font-semibold text-foreground">Total</span>
                            <span className="text-base font-semibold text-accent">{marksTotal}</span>
                        </div>
                        
                        {syllabusUrl && (
                            <Button
                                href={syllabusUrl}
                                variant="secondary"
                                icon={<BookOpen className="size-4" />}
                                className="w-full md:w-80"
                            >
                                View Official Syllabus
                            </Button>
                        )}
                    </div>
                </div>
            )}

            <div>
                <p className="mb-1 font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                    Belongs to Program
                </p>
                <ProgramCard program={program} />
            </div>
        </div>
    )
}

export default SubjectDetails;
