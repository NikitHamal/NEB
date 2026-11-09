import { Injectable } from "@nestjs/common";

import { ProgramsRepository } from "./programs.repository";

@Injectable()
export class ProgramsService {
  constructor(private readonly programsRepository: ProgramsRepository) {}

  findAll() {
    return this.programsRepository.findAll();
  }
}
