import { Module } from "@nestjs/common";

import { SubjectsController } from "./subjects.controller";
import { SubjectsRepository } from "./subjects.repository";
import { SubjectsService } from "./subjects.service";

@Module({
  controllers: [SubjectsController],
  providers: [SubjectsService, SubjectsRepository],
})
export class SubjectsModule {}
