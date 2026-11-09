import { Type } from "class-transformer";
import { IsInt, IsOptional, IsPositive, IsString, MinLength } from "class-validator";

import { PaginationQueryDto } from "../../../common/dto/pagination-query.dto";

export class GetResourcesQueryDto extends PaginationQueryDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @IsPositive({ message: "Subject Offering ID must be a positive integer" })
  offeringId?: number;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @IsPositive({ message: "User ID must be a positive integer" })
  userId?: number;

  @IsOptional()
  @IsString()
  @MinLength(2, { message: "Search query must be at least 2 characters" })
  q?: string;
}
