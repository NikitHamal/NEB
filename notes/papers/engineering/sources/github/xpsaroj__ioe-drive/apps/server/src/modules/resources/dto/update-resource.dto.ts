import { Type } from "class-transformer";
import { IsIn, IsInt, IsOptional, IsPositive, MinLength } from "class-validator";

import { ResourceTypeEnum, type ResourceType } from "../../../database/schema";

export class UpdateResourceDto {
  @IsOptional()
  @MinLength(3, { message: "Title must be at least 3 characters long" })
  title?: string;

  @IsOptional()
  @MinLength(10, { message: "Description must be at least 10 characters long" })
  description?: string;

  @IsOptional()
  @IsIn(ResourceTypeEnum.enumValues)
  type?: ResourceType;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @IsPositive()
  offeringId?: number;
}
