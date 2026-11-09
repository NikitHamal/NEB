import { Inject, Injectable } from "@nestjs/common";
import { asc, count, ilike, inArray, or } from "drizzle-orm";

import { DRIZZLE } from "../../database/database.constants";
import type { DrizzleDb } from "../../database/database.types";
import { subjectOfferingsTable, subjectsTable, type Semester } from "../../database/schema";

@Injectable()
export class SubjectsRepository {
  constructor(@Inject(DRIZZLE) private readonly db: DrizzleDb) {}

  findByProgramAndSemester(programId: number, semester?: Semester) {
    return this.db.query.subjectOfferingsTable.findMany({
      where: (fields, { eq, and }) =>
        and(eq(fields.programId, programId), semester ? eq(fields.semester, semester) : undefined),
      columns: {
        id: true,
        subjectId: true,
        semester: true,
        programId: true,
        year: true,
      },
      with: {
        subject: {
          with: {
            program: true,
            marks: true,
          },
        },
        program: true,
      },
      orderBy: (fields) => asc(fields.semester),
    });
  }

  // `subjectId` here is actually a subject *offering* id.
  findById(subjectId: number) {
    return this.db.query.subjectOfferingsTable.findFirst({
      where: (fields, { eq }) => eq(fields.id, subjectId),
      columns: {
        id: true,
        subjectId: true,
        semester: true,
        programId: true,
        year: true,
      },
      with: {
        subject: {
          with: {
            program: true,
            marks: true,
          },
        },
        program: true,
      },
    });
  }

  // Flat ids only, no joins - backs the sitemap, which never needs the full offering shape.
  async findOfferingIdsByProgram(programId: number): Promise<number[]> {
    const rows = await this.db.query.subjectOfferingsTable.findMany({
      where: (fields, { eq }) => eq(fields.programId, programId),
      columns: { id: true },
    });

    return rows.map((row) => row.id);
  }

  findForUpload(programId: number, semester: Semester) {
    return this.db.query.subjectOfferingsTable.findMany({
      where: (fields, { eq, and }) => and(eq(fields.programId, programId), eq(fields.semester, semester)),
      columns: {
        id: true,
        isElective: true,
      },
      with: {
        subject: {
          columns: {
            id: true,
            code: true,
            name: true,
          },
        },
      },
      orderBy: (fields) => asc(fields.id),
    });
  }

  // Two-step: find matching subjects first, then their offerings - the relational query API can't filter by a joined column directly.
  async searchByNameOrCode(q: string, pagination: { limit: number; offset: number }) {
    const matchingSubjects = await this.db
      .select({ id: subjectsTable.id })
      .from(subjectsTable)
      .where(or(ilike(subjectsTable.name, `%${q}%`), ilike(subjectsTable.code, `%${q}%`)));

    const subjectIds = matchingSubjects.map((s) => s.id);
    if (subjectIds.length === 0) {
      return { items: [], total: 0 };
    }

    const whereClause = inArray(subjectOfferingsTable.subjectId, subjectIds);

    const [items, totalResult] = await Promise.all([
      this.db.query.subjectOfferingsTable.findMany({
        where: whereClause,
        columns: {
          id: true,
          semester: true,
        },
        with: {
          subject: {
            columns: { id: true, code: true, name: true },
          },
          program: {
            columns: { id: true, code: true, name: true },
          },
        },
        orderBy: (fields) => asc(fields.id),
        limit: pagination.limit,
        offset: pagination.offset,
      }),
      this.db.select({ total: count() }).from(subjectOfferingsTable).where(whereClause),
    ]);

    return { items, total: totalResult[0]?.total ?? 0 };
  }
}
