import { IsIn, IsOptional, IsString, MaxLength } from "class-validator";

import { ModerationReasonEnum, type ModerationReason } from "../../../database/schema";

export class ModerateResourceDto {
  @IsIn(ModerationReasonEnum.enumValues)
  reason!: ModerationReason;

  @IsOptional()
  @IsString()
  @MaxLength(1000, { message: "Note must be at most 1000 characters long" })
  note?: string;
}
