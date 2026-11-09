import { Inject, Injectable } from "@nestjs/common";

import { DRIZZLE } from "../../database/database.constants";
import type { DrizzleDb } from "../../database/database.types";

@Injectable()
export class ProgramsRepository {
  constructor(@Inject(DRIZZLE) private readonly db: DrizzleDb) {}

  findAll() {
    return this.db.query.programsTable.findMany();
  }

  findById(id: number) {
    return this.db.query.programsTable.findFirst({ where: (programs, { eq }) => eq(programs.id, id) });
  }
}
