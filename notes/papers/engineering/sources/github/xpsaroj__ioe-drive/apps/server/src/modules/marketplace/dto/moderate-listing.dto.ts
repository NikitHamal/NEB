import { IsIn, IsOptional, IsString, MaxLength } from "class-validator";

import { MarketplaceReportReasonEnum, type MarketplaceReportReason } from "../../../database/schema";

export class ModerateListingDto {
  @IsIn(MarketplaceReportReasonEnum.enumValues)
  reason!: MarketplaceReportReason;

  @IsOptional()
  @IsString()
  @MaxLength(1000, { message: "Note must be at most 1000 characters long" })
  note?: string;
}
