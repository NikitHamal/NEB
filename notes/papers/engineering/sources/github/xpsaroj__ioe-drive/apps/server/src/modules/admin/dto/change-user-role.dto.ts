import { IsEmail, IsIn } from "class-validator";

export class ChangeUserRoleDto {
  @IsEmail()
  email!: string;

  // ADMIN is deliberately not an allowed value - granting/revoking it always stays a direct database change.
  @IsIn(["USER", "MODERATOR"])
  role!: "USER" | "MODERATOR";
}
