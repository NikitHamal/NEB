import { NotebookPen } from "lucide-react";

import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import type { SubjectOffering } from "@/types/entities";

const numberToRoman = (num: number): string => {
    const romanNumerals: { [key: number]: string } = {
        1: "I",
        2: "II",
        3: "III",
        4: "IV",
        5: "V",
        7: "VII",
        8: "VIII",
        9: "IX",
        10: "X",
    };
    return romanNumerals[num] || num.toString();
}

interface AcademicTermInfoProps extends Omit<SubjectOffering, "id" | "subjectId" | "programId"> {
    /** Built by the caller (SubjectOfferingDetails) since it needs the offering's actual program. */
    browseResourcesHref: string;
}

const AcademicTermInfo = ({ year, semester, isElective, browseResourcesHref }: AcademicTermInfoProps) => {
    return (
        <div className="rounded-lg border border-border p-6">
            <p className="mb-2 font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                Offering Details
            </p>
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <div>
                    <div className="flex flex-wrap items-center gap-2">
                        <h2 className="text-xl font-bold text-foreground">
                            Year {numberToRoman(+year)}, Part {numberToRoman(Math.floor(+semester / +year))}
                        </h2>
                        {isElective && <Badge size="sm" variant="info">Elective</Badge>}
                    </div>
                    <p className="mt-1 flex items-center gap-3 text-sm text-foreground-secondary">
                        <span>Year {year}</span>
                        <span>Semester {semester}</span>
                    </p>
                </div>
                <Button href={browseResourcesHref} variant="secondary" size="sm" icon={<NotebookPen className="size-4" />} className="shrink-0">
                    Browse Resources
                </Button>
            </div>
        </div>
    );
}

export default AcademicTermInfo;
