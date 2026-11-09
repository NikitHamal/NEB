import { Type } from "class-transformer";
import { IsInt, IsOptional, IsPositive, Max } from "class-validator";

export class GetSimilarResourcesQueryDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @IsPositive()
  @Max(20)
  limit?: number;
}
