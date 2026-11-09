import { Type } from "class-transformer";
import { IsIn, IsInt, IsPositive } from "class-validator";

import { SemesterEnum, type Semester } from "../../../database/schema";

export class GetSubjectsForUploadQueryDto {
  @Type(() => Number)
  @IsInt()
  @IsPositive({ message: "Program ID is required and it must be a positive integer" })
  programId!: number;

  @IsIn(SemesterEnum.enumValues)
  semester!: Semester;
}
