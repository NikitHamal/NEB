import { Type } from "class-transformer";
import { IsInt, IsOptional, IsPositive, IsString, Max, MinLength } from "class-validator";

export class SearchSuggestionsQueryDto {
  @IsString()
  @MinLength(2, { message: "Search query must be at least 2 characters" })
  q!: string;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @IsPositive()
  @Max(20)
  limit?: number;
}
