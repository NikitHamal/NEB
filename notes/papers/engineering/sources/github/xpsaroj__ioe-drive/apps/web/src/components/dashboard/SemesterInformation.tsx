"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Table, { Column } from "@/components/ui/Table";
import { SubjectHardnessBadge } from "@/components/common/offering";
import { SubjectOfferingWithSubject } from "@/types/entities/academics";

import { useMe } from "@/hooks/queries/use-me";
import { useSubjectOfferings } from "@/hooks/queries/use-academics";

const MarksCell = ({ final, assessment }: { final: number; assessment: number }) => (
  <span className="tabular-nums">
    <span className="font-semibold text-foreground">{final}</span>
    <span className="text-foreground-tertiary"> + {assessment}</span>
  </span>
);

const SemesterInformation = () => {
  const router = useRouter();
  const { data: userData, isLoading: userLoading } = useMe();
  const profile = userData?.profile;

  const { data: subjectOfferings, isLoading } = useSubjectOfferings(profile?.programId, profile?.semester);

  const columns: Column<SubjectOfferingWithSubject>[] = [
    {
      key: "subject",
      label: "SUBJECT",
      render: (item) => (
        <div>
          <Link
            href={`/offerings/${item.id}`}
            // Stop bubbling to the row, which navigates to the resources list instead.
            onClick={(e) => e.stopPropagation()}
          >
            <span className="font-medium cursor-pointer hover:underline underline-offset-2">
              {item.subject.name}
            </span>
          </Link>
          <p className="font-display text-xs text-foreground-tertiary mt-0.5">{item.subject.code}</p>
        </div>
      ),
    },
    {
      key: "difficulty",
      label: "DIFFICULTY",
      render: (item) => (
        <SubjectHardnessBadge level={item.subject.hardnessLevel} size="sm" />
      ),
    },
    {
      key: "marks-theory",
      label: "MARKS (TH)",
      render: (item) => (
        <MarksCell final={item.subject.marks.theoryFinal} assessment={item.subject.marks.theoryAssessment} />
      ),
    },
    {
      key: "marks-practical",
      label: "MARKS (PR)",
      render: (item) => (
        <MarksCell final={item.subject.marks.practicalFinal} assessment={item.subject.marks.practicalAssessment} />
      ),
    },
  ];

  const subjectCount = subjectOfferings?.length ?? 0;

  return (
    <div>
      <h2 className="text-lg font-semibold text-foreground">Subjects this semester</h2>
      <p className="text-sm text-foreground-secondary mt-0.5 mb-6">
        {subjectCount > 0
          ? `${subjectCount} subject${subjectCount === 1 ? "" : "s"} - click a row to browse its resources, or its name for full details.`
          : "Tip: click a subject's row to browse its resources, or its name for full details."}
      </p>
      <Table
        columns={columns}
        loading={isLoading || userLoading}
        data={subjectOfferings || []}
        striped
        onRowClick={(item) => {
          const params = new URLSearchParams({
            programId: String(item.programId),
            semester: item.semester,
            offeringId: String(item.id),
          });
          router.push(`/resources?${params.toString()}`);
        }}
        emptyMessage="No semester information available. Make sure you've added your semester and program in your profile settings."
      />
    </div>
  );
};

export default SemesterInformation;
