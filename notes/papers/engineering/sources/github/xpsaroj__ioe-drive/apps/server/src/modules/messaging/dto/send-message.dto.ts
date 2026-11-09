import { Type } from "class-transformer";
import { IsInt, IsPositive, IsString, MaxLength, MinLength } from "class-validator";

export class SendMessageDto {
  @Type(() => Number)
  @IsInt()
  @IsPositive()
  conversationId!: number;

  @IsString()
  @MinLength(1, { message: "Message can't be empty" })
  @MaxLength(2000, { message: "Message must be at most 2000 characters long" })
  body!: string;
}
