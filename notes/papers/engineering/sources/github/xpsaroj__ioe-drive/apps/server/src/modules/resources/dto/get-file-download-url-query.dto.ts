import { IsIn, IsOptional } from "class-validator";

export class GetFileDownloadUrlQueryDto {
  // Not boolean-coerced - "false" as a string is still truthy if naively coerced.
  @IsOptional()
  @IsIn(["true", "false"])
  download?: "true" | "false";
}
