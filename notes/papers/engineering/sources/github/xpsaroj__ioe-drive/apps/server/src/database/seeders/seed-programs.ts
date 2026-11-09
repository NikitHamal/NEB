import { readFileSync } from "node:fs";

import { db } from "../seed-db";
import { programsTable } from "../schema";

interface ProgramSeed {
  code: string;
  name: string;
  totalYears: number;
  syllabusUrl?: string;
}

async function seedPrograms() {
  const programs: ProgramSeed[] = JSON.parse(readFileSync("data/programs.json", "utf-8"));

  await db.insert(programsTable).values(programs).onConflictDoNothing();
  console.log("Programs seeded successfully.");
}

seedPrograms()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Error seeding programs:", error);
    process.exit(1);
  });
