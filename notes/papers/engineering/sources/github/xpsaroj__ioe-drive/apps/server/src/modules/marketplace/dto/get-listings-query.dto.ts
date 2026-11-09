import { Type } from "class-transformer";
import { IsIn, IsInt, IsOptional, IsPositive, IsString, Min, MinLength } from "class-validator";

import { PaginationQueryDto } from "../../../common/dto/pagination-query.dto";
import { MarketplaceCategoryEnum, MarketplaceListingTypeEnum, type MarketplaceCategory, type MarketplaceListingType } from "../../../database/schema";

export class GetListingsQueryDto extends PaginationQueryDto {
  @IsOptional()
  @IsIn(MarketplaceListingTypeEnum.enumValues)
  type?: MarketplaceListingType;

  @IsOptional()
  @IsIn(MarketplaceCategoryEnum.enumValues)
  category?: MarketplaceCategory;

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
  @Type(() => Number)
  @IsInt()
  @Min(0)
  minPrice?: number;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(0)
  maxPrice?: number;

  @IsOptional()
  @IsString()
  @MinLength(2, { message: "Search query must be at least 2 characters" })
  q?: string;
}
