import SubjectDetails from "./SubjectDetails";
import AcademicTermInfo from "./AcademicTermInfo";

import type { SubjectOfferingWithSubject } from "@/types/entities";

const SubjectOfferingDetails = ({ offering }: { offering: SubjectOfferingWithSubject }) => {
    const { id, subject, year, semester, isElective, programId } = offering;

    // Deliberately the *offering's* program, not subject.program - the two can differ (e.g. SH-owned subjects taught to BCT students).
    const browseResourcesHref = `/resources?programId=${programId}&semester=${semester}&offeringId=${id}`;

    return (
        <div className="space-y-6">
            <AcademicTermInfo
                year={year}
                semester={semester}
                isElective={isElective}
                browseResourcesHref={browseResourcesHref}
            />

            <SubjectDetails
                subject={subject}
            />

            <p className="text-center text-sm text-foreground-tertiary">
                (The information provided above may not always be accurate. Please verify it with official sources if anything seems incorrect.)
            </p>
        </div>
    )
}

export default SubjectOfferingDetails;