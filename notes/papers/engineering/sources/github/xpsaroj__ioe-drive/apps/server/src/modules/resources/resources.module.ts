import { Module } from "@nestjs/common";

import { ModerationModule } from "../moderation/moderation.module";
import { ResourcesController } from "./resources.controller";
import { ResourcesRepository } from "./resources.repository";
import { ResourcesService } from "./resources.service";

@Module({
  imports: [ModerationModule],
  controllers: [ResourcesController],
  providers: [ResourcesService, ResourcesRepository],
  exports: [ResourcesService, ResourcesRepository],
})
export class ResourcesModule {}
