export interface Program {
    id: number;
    code: string;
    name: string;
    totalYears: number;
    syllabusUrl?: string;
}

export enum SubjectHardnessLevel {
    EASY = "Easy",
    MEDIUM = "Medium",
    HARD = "Hard",
    VERY_HARD = "Very Hard",
}

export type ProgramCode =
    | "BCE"
    | "BCT"
    | "BEL"
    | "BEI"
    | "BME"
    | "BAR"
    | "BGE"
    | "BIE"
    | "BAG"
    | "BAM"
    | "BAS"
    | "BCH"
    | "SH";
export type Semester = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "10";
export type Year = "1" | "2" | "3" | "4" | "5";
export const SemesterLabel: Record<Semester, string> = {
    "1": "1st",
    "2": "2nd",
    "3": "3rd",
    "4": "4th",
    "5": "5th",
    "6": "6th",
    "7": "7th",
    "8": "8th",
    "9": "9th",
    "10": "10th",
};
export const YearLabel: Record<Year, string> = {
    "1": "1st Year",
    "2": "2nd Year",
    "3": "3rd Year",
    "4": "4th Year",
    "5": "5th Year",
};

export interface Subject {
    id: number;
    code: string;
    name: string;
    programId: number;
    hardnessLevel: SubjectHardnessLevel;
    description?: string;
    syllabusUrl?: string;
}

export interface SubjectOffering {
    id: number;
    subjectId: number;
    semester: Semester;
    programId: number;
    year: Year;
    isElective: boolean;
}

export interface SubjectOfferingWithProgram extends SubjectOffering {
    program: Program;
}

export interface Marks {
    id: number;
    subjectId: number;
    theoryAssessment: number;
    theoryFinal: number;
    practicalAssessment: number;
    practicalFinal: number;
}

export interface SubjectWithProgramAndMarks extends Subject {
    program: Program;
    marks: Marks;
}

export interface SubjectOfferingWithSubject extends SubjectOfferingWithProgram {
    subject: SubjectWithProgramAndMarks;
}

export interface SubjectForUploadForm {
    id: number;
    isElective: boolean;
    subject: {
        id: number;
        code: string;
        name: string;
    };
}