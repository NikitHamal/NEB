import { Module } from "@nestjs/common";

import { UsersModule } from "../users/users.module";
import { WebhookEventsRepository } from "./webhook-events.repository";
import { WebhooksController } from "./webhooks.controller";
import { WebhooksService } from "./webhooks.service";

@Module({
  imports: [UsersModule],
  controllers: [WebhooksController],
  providers: [WebhooksService, WebhookEventsRepository],
})
export class WebhooksModule {}
