import { randomUUID } from "node:crypto";

import { eq, ne } from "drizzle-orm";

import { ResourcesRepository } from "../../modules/resources/resources.repository";
import type { FileMetadata } from "../../storage/file-metadata.interface";
import { db } from "../seed-db";
import { ResourceTypeEnum, programsTable, subjectOfferingsTable, subjectsTable, usersTable, type ResourceType } from "../schema";

/** How many resources to create for the one chosen subject in each program/semester. */
const RESOURCES_PER_SUBJECT = 5;

/** How many (fake) files to attach to each seeded resource. */
const FILES_PER_RESOURCE = 5;

const RESOURCE_TYPE_LABEL: Record<ResourceType, string> = {
  NOTE: "Notes",
  PAST_QUESTION: "Past Question",
  ASSESSMENT: "Assessment",
  LAB_SHEET: "Lab Sheet",
  BOOK: "Reference Book",
  OTHER: "Resource",
};

// Not uploaded anywhere - the URL below is a placeholder, not a real blob.
const FAKE_FILE_TYPES: { mimeType: string; ext: string }[] = [
  { mimeType: "application/pdf", ext: "pdf" },
  { mimeType: "image/jpeg", ext: "jpg" },
  { mimeType: "image/png", ext: "png" },
  { mimeType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document", ext: "docx" },
];

interface OfferingWithSubject {
  id: number;
  programId: number;
  semester: string;
  subjectCode: string;
  subjectName: string;
}

function createFakeFile(subjectCode: string, resourceIndex: number, fileIndex: number): FileMetadata {
  const fileType = FAKE_FILE_TYPES[fileIndex % FAKE_FILE_TYPES.length]!;
  const blobName = `${randomUUID()}.${fileType.ext}`;

  return {
    blobName,
    url: `https://placeholder.local/resources/${blobName}`,
    originalName: `${subjectCode}-${resourceIndex + 1}-${fileIndex + 1}.${fileType.ext}`,
    mimeType: fileType.mimeType,
    size: (fileIndex + 1) * 128 * 1024,
  };
}

// Not idempotent - assumes a clean `resources` table. No Azure calls; files get placeholder blob data.
async function seedResources() {
  const resourcesRepository = new ResourcesRepository(db);

  const users = await db.select().from(usersTable);
  if (users.length === 0) {
    console.log("No users found. Run db:sync-clerk-users first, or sign up a user. Skipping resource seeding.");
    return;
  }

  const programs = await db
    .select({ id: programsTable.id, code: programsTable.code })
    .from(programsTable)
    .where(ne(programsTable.code, "SH"));

  if (programs.length === 0) {
    console.log("No programs found. Run db:seed-programs first. Skipping resource seeding.");
    return;
  }

  const programIds = new Set(programs.map((program) => program.id));

  const allOfferings: OfferingWithSubject[] = await db
    .select({
      id: subjectOfferingsTable.id,
      programId: subjectOfferingsTable.programId,
      semester: subjectOfferingsTable.semester,
      subjectCode: subjectsTable.code,
      subjectName: subjectsTable.name,
    })
    .from(subjectOfferingsTable)
    .innerJoin(subjectsTable, eq(subjectOfferingsTable.subjectId, subjectsTable.id))
    .orderBy(subjectOfferingsTable.id);

  if (allOfferings.length === 0) {
    console.log("No subject offerings found. Run db:seed-subjects first. Skipping resource seeding.");
    return;
  }

  const chosenOfferings = new Map<string, OfferingWithSubject>();
  for (const offering of allOfferings) {
    if (!programIds.has(offering.programId)) continue;

    const key = `${offering.programId}-${offering.semester}`;
    if (!chosenOfferings.has(key)) {
      chosenOfferings.set(key, offering);
    }
  }

  let uploaderCursor = 0;

  for (const offering of chosenOfferings.values()) {
    for (let i = 0; i < RESOURCES_PER_SUBJECT; i++) {
      const uploader = users[uploaderCursor % users.length]!;
      uploaderCursor++;

      const type = ResourceTypeEnum.enumValues[i % ResourceTypeEnum.enumValues.length]!;
      const typeLabel = RESOURCE_TYPE_LABEL[type];

      const files = Array.from({ length: FILES_PER_RESOURCE }, (_, fileIndex) =>
        createFakeFile(offering.subjectCode, i, fileIndex),
      );

      await resourcesRepository.create(
        {
          title: `${offering.subjectCode} ${typeLabel}`,
          description: `Sample ${typeLabel.toLowerCase()} for ${offering.subjectName}, shared by ${uploader.fullName}.`,
          type,
          offeringId: offering.id,
          uploadedBy: uploader.id,
          status: "APPROVED",
        },
        files,
      );
    }

    console.log(
      `Seeded ${RESOURCES_PER_SUBJECT} resource(s) for ${offering.subjectCode} (program ${offering.programId}, semester ${offering.semester}).`,
    );
  }

  console.log("Resources seeded successfully.");
}

seedResources()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Error seeding resources:", error);
    process.exit(1);
  });
