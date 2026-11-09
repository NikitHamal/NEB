import Link from "next/link";
import { ClipboardList } from "lucide-react";

import SubjectHardnessBadge from "./SubjectHardnessBadge";
import Badge from "@/components/ui/Badge";
import type { SubjectOfferingWithSubject } from "@/types/entities";

interface SubjectOfferingCardProps {
    offering: SubjectOfferingWithSubject;
}

// Shared by the curriculum directory and a program's own subject list
const SubjectOfferingCard = ({ offering }: SubjectOfferingCardProps) => {
    const { marks } = offering.subject;
    const marksTotal = marks.theoryFinal + marks.theoryAssessment + marks.practicalFinal + marks.practicalAssessment;

    return (
        <Link
            href={`/offerings/${offering.id}`}
            className="group flex flex-col rounded-lg border border-border bg-card-background p-5 transition-colors hover:border-accent hover:bg-card-hover"
        >
            <div className="flex items-start justify-between gap-3">
                <span className="rounded-md border border-accent/30 bg-accent-soft px-2 py-1 font-display text-xs uppercase tracking-wide text-accent">
                    {offering.subject.code}
                </span>
                <SubjectHardnessBadge level={offering.subject.hardnessLevel} size="sm" className="shrink-0" />
            </div>

            <p className="mt-3 font-semibold text-foreground decoration-2 underline-offset-2 group-hover:underline">
                {offering.subject.name}
            </p>

            {offering.subject.description && (
                <p className="mt-1 line-clamp-3 text-sm sm:text-base text-foreground-secondary">
                    {offering.subject.description}
                </p>
            )}

            <div className="mt-4 flex items-center justify-between gap-3 border-t border-border pt-3">
                <span className="flex items-center gap-1.5 text-xs text-foreground-secondary">
                    <ClipboardList className="size-3.5" />
                    {marksTotal} marks
                </span>
                {offering.isElective && <Badge size="sm" variant="info">Elective</Badge>}
            </div>
        </Link>
    );
};

export default SubjectOfferingCard;
