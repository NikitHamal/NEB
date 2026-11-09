import { Controller, Get } from "@nestjs/common";

import { ProgramsService } from "./programs.service";

@Controller("programs")
export class ProgramsController {
  constructor(private readonly programsService: ProgramsService) {}

  /** GET /api/programs - list all programs. */
  @Get()
  findAll() {
    return this.programsService.findAll();
  }
}
