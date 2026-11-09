import { Type } from "class-transformer";
import { IsInt, IsOptional, IsPositive, Max } from "class-validator";

export const DEFAULT_PAGE = 1;
export const DEFAULT_LIMIT = 10;
export const MAX_LIMIT = 100;

// Extend this in a route's own query DTO, e.g. `class GetResourcesQueryDto extends PaginationQueryDto`.
export class PaginationQueryDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @IsPositive()
  page: number = DEFAULT_PAGE;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @IsPositive()
  @Max(MAX_LIMIT)
  limit: number = DEFAULT_LIMIT;
}
