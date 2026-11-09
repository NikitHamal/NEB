import type { Semester } from "../entities";

export interface SubjectSummary {
    id: number;
    code: string;
    name: string;
}

export interface SubjectOfferingSummary {
    id: number;
    subjectId: number
}

export interface ProgramSummary {
    id: number;
    name: string;
    code: string;
}

// Lean subject-offering search result row - no marks/description/syllabusUrl/hardnessLevel, unlike SubjectOfferingWithSubject.
export interface SubjectSearchResult {
    id: number;
    semester: Semester;
    subject: SubjectSummary;
    program: ProgramSummary;
}