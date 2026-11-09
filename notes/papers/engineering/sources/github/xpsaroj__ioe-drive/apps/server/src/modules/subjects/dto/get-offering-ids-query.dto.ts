import { Type } from "class-transformer";
import { IsInt, IsPositive } from "class-validator";

export class GetOfferingIdsQueryDto {
  @Type(() => Number)
  @IsInt()
  @IsPositive({ message: "Program ID is required and it must be a positive integer" })
  programId!: number;
}
