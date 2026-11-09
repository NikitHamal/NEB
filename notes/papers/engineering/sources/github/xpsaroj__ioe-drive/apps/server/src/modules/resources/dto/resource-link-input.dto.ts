import { IsString, IsUrl, MaxLength, MinLength } from "class-validator";

// A resource link's URL and a short human-readable label - shown on cards instead of the raw URL.
export class ResourceLinkInput {
  @IsUrl({ protocols: ["http", "https"], require_protocol: true })
  url!: string;

  @IsString()
  @MinLength(1, { message: "Link label is required" })
  @MaxLength(100, { message: "Link label must be at most 100 characters long" })
  label!: string;
}
