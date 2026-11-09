import { readFileSync } from "node:fs";

import { db } from "../seed-db";
import { marksTable, programsTable, subjectOfferingsTable, subjectsTable, type Semester, type Year } from "../schema";

interface SubjectsJsonEntry {
  code: string;
  name: string;
  programCode: string;
  syllabusUrl?: string;
  marks: {
    theoryAssessment?: number;
    theoryFinal?: number;
    practicalAssessment?: number;
    practicalFinal?: number;
  };
}

interface SubjectOfferingsJson {
  [programCode: string]: {
    name: string;
    subjects: {
      code: string;
      name: string;
      year: Year;
      semester: Semester;
      programCode: string;
      isElective?: boolean;
    }[];
  };
}

async function seedSubjectsAndOfferings() {
  const subjectsJson: SubjectsJsonEntry[] = JSON.parse(readFileSync("data/subjects.json", "utf-8"));
  const offeringsJson: SubjectOfferingsJson = JSON.parse(readFileSync("data/subject-offerings.json", "utf-8"));

  const programs = await db.select().from(programsTable);
  const programCodeToId = new Map<string, number>();
  programs.forEach((program) => programCodeToId.set(program.code, program.id));

  const subjectCodeToId = new Map<string, number>();

  for (const subject of subjectsJson) {
    const programId = programCodeToId.get(subject.programCode);

    if (!programId) {
      console.warn(`Program not found for ${subject.programCode}`);
      continue;
    }

    const inserted = await db
      .insert(subjectsTable)
      .values({
        code: subject.code,
        name: subject.name,
        programId,
        syllabusUrl: subject.syllabusUrl ?? null,
        hardnessLevel: "MEDIUM",
      })
      .onConflictDoNothing()
      .returning({ id: subjectsTable.id, code: subjectsTable.code });

    if (inserted.length > 0 && inserted[0]) {
      subjectCodeToId.set(inserted[0].code, inserted[0].id);
    }
  }

  // Fetch all subjects again to ensure we have IDs for subjects skipped above due to conflicts.
  const allSubjects = await db.select().from(subjectsTable);
  allSubjects.forEach((subject) => subjectCodeToId.set(subject.code, subject.id));

  for (const subject of subjectsJson) {
    const subjectId = subjectCodeToId.get(subject.code);
    if (!subjectId) continue;

    await db
      .insert(marksTable)
      .values({
        subjectId,
        theoryAssessment: subject.marks.theoryAssessment ?? 0,
        theoryFinal: subject.marks.theoryFinal ?? 0,
        practicalAssessment: subject.marks.practicalAssessment ?? 0,
        practicalFinal: subject.marks.practicalFinal ?? 0,
      })
      .onConflictDoNothing();
  }

  for (const programCode in offeringsJson) {
    const programData = offeringsJson[programCode];
    const programId = programCodeToId.get(programCode);
    if (!programId) continue;

    const subjectsForProgram = programData?.subjects ?? [];
    for (const offering of subjectsForProgram) {
      const subjectId = subjectCodeToId.get(offering.code);

      if (!subjectId) {
        console.warn(`Subject not found for offering: ${offering.code}`);
        continue;
      }

      await db
        .insert(subjectOfferingsTable)
        .values({
          subjectId,
          programId,
          semester: offering.semester,
          year: offering.year,
          isElective: offering.isElective ?? false,
        })
        .onConflictDoNothing();
    }
  }

  console.log("Subjects, marks and offerings seeded successfully.");
}

seedSubjectsAndOfferings()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Seeding failed:", error);
    process.exit(1);
  });
