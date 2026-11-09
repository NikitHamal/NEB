import { IsIn, IsNumber, IsOptional, IsString } from "class-validator";

// Full 1-10 range (matches SemesterEnum) - MeService.updateProfile enforces that only
// Architecture (BAR) students can actually submit 9 or 10.
const UPDATABLE_SEMESTERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] as const;
type UpdatableSemester = (typeof UPDATABLE_SEMESTERS)[number];

export class UpdateProfileDto {
  @IsOptional()
  @IsString()
  bio?: string;

  @IsOptional()
  @IsNumber()
  programId?: number;

  @IsOptional()
  @IsIn(UPDATABLE_SEMESTERS)
  semester?: UpdatableSemester;

  @IsOptional()
  @IsString()
  college?: string;
}
