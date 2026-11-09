import { Injectable, NotFoundException } from "@nestjs/common";

import type { Semester } from "../../database/schema";
import { SubjectsRepository } from "./subjects.repository";

@Injectable()
export class SubjectsService {
  constructor(private readonly subjectsRepository: SubjectsRepository) {}

  findByProgramAndSemester(programId: number, semester?: Semester) {
    return this.subjectsRepository.findByProgramAndSemester(programId, semester);
  }

  async findById(subjectId: number) {
    const subject = await this.subjectsRepository.findById(subjectId);

    if (!subject) {
      throw new NotFoundException("Subject not found");
    }

    return subject;
  }

  findForUpload(programId: number, semester: Semester) {
    return this.subjectsRepository.findForUpload(programId, semester);
  }

  findOfferingIdsByProgram(programId: number) {
    return this.subjectsRepository.findOfferingIdsByProgram(programId);
  }

  searchSubjects(q: string, pagination: { limit: number; offset: number }) {
    return this.subjectsRepository.searchByNameOrCode(q, pagination);
  }
}
