import { Module } from "@nestjs/common";

import { MarketplaceModule } from "../marketplace/marketplace.module";
import { ProgramsModule } from "../programs/programs.module";
import { ResourcesModule } from "../resources/resources.module";
import { UsersModule } from "../users/users.module";
import { MeController } from "./me.controller";
import { MeRepository } from "./me.repository";
import { MeService } from "./me.service";

@Module({
  imports: [UsersModule, ResourcesModule, MarketplaceModule, ProgramsModule],
  controllers: [MeController],
  providers: [MeService, MeRepository],
})
export class MeModule {}
