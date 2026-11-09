import { Module } from "@nestjs/common";

import { ResourcesModule } from "../resources/resources.module";
import { UsersController } from "./users.controller";
import { UsersRepository } from "./users.repository";
import { UsersService } from "./users.service";

@Module({
  imports: [ResourcesModule],
  controllers: [UsersController],
  providers: [UsersService, UsersRepository],
  exports: [UsersRepository],
})
export class UsersModule {}
