import { Type } from "class-transformer";
import { IsIn, IsInt, IsOptional, IsPositive, IsString, Min, MinLength } from "class-validator";

import { MarketplaceCategoryEnum, MarketplaceListingTypeEnum, type MarketplaceCategory, type MarketplaceListingType } from "../../../database/schema";

export class CreateListingDto {
  @IsString()
  @MinLength(3, { message: "Title must be at least 3 characters long" })
  title!: string;

  @IsString()
  @MinLength(10, { message: "Description must be at least 10 characters long" })
  description!: string;

  @IsIn(MarketplaceListingTypeEnum.enumValues)
  type!: MarketplaceListingType;

  @IsIn(MarketplaceCategoryEnum.enumValues)
  category!: MarketplaceCategory;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(0)
  price?: number;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @IsPositive({ message: "Subject Offering ID must be a positive integer" })
  offeringId?: number;
}
