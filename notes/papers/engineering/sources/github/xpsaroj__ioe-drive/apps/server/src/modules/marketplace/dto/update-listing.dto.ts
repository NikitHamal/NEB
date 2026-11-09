import { Type } from "class-transformer";
import { IsIn, IsInt, IsOptional, IsPositive, Min, MinLength } from "class-validator";

import { MarketplaceCategoryEnum, MarketplaceListingTypeEnum, type MarketplaceCategory, type MarketplaceListingType } from "../../../database/schema";

export class UpdateListingDto {
  @IsOptional()
  @MinLength(3, { message: "Title must be at least 3 characters long" })
  title?: string;

  @IsOptional()
  @MinLength(10, { message: "Description must be at least 10 characters long" })
  description?: string;

  @IsOptional()
  @IsIn(MarketplaceListingTypeEnum.enumValues)
  type?: MarketplaceListingType;

  @IsOptional()
  @IsIn(MarketplaceCategoryEnum.enumValues)
  category?: MarketplaceCategory;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(0)
  price?: number;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @IsPositive()
  offeringId?: number;
}
