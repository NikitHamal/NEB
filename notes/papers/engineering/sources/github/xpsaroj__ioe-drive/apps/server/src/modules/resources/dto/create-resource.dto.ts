import { plainToInstance, Transform, Type } from "class-transformer";
import { ArrayMaxSize, IsArray, IsIn, IsInt, IsPositive, IsString, MinLength, ValidateNested } from "class-validator";

import { ResourceTypeEnum, type ResourceType } from "../../../database/schema";
import { MAX_RESOURCE_LINKS } from "../resources.types";
import { ResourceLinkInput } from "./resource-link-input.dto";

// Multipart bodies only carry strings, so links travel as a JSON-stringified array field -
// parsed here before validation. Malformed JSON just becomes an empty array rather than a 500.
// Instantiates ResourceLinkInput directly, since a @Transform's return value bypasses the
// automatic nested-instance creation @Type() would otherwise do.
const parseLinksField = ({ value }: { value: unknown }) => {
  if (typeof value !== "string" && !Array.isArray(value)) return [];

  let parsed: unknown = value;
  if (typeof value === "string") {
    try {
      parsed = JSON.parse(value);
    } catch {
      return [];
    }
  }

  return Array.isArray(parsed) ? plainToInstance(ResourceLinkInput, parsed) : [];
};

export class CreateResourceDto {
  @IsString()
  @MinLength(3, { message: "Title must be at least 3 characters long" })
  title!: string;

  @IsString()
  @MinLength(10, { message: "Description must be at least 10 characters long" })
  description!: string;

  @IsIn(ResourceTypeEnum.enumValues)
  type!: ResourceType;

  @Type(() => Number)
  @IsInt()
  @IsPositive({ message: "Subject Offering ID must be a positive integer" })
  offeringId!: number;

  @Transform(parseLinksField)
  @IsArray()
  @ArrayMaxSize(MAX_RESOURCE_LINKS, { message: `A resource can have at most ${MAX_RESOURCE_LINKS} links` })
  @ValidateNested({ each: true })
  links: ResourceLinkInput[] = [];
}
