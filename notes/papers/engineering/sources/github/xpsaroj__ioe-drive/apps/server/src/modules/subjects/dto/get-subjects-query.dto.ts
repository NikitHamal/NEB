import { Type } from "class-transformer";
import { IsIn, IsInt, IsOptional, IsPositive } from "class-validator";

import { SemesterEnum, type Semester } from "../../../database/schema";

export class GetSubjectsQueryDto {
  @Type(() => Number)
  @IsInt()
  @IsPositive({ message: "Program ID is required and it must be a positive integer" })
  programId!: number;

  @IsOptional()
  @IsIn(SemesterEnum.enumValues)
  semester?: Semester;
}
