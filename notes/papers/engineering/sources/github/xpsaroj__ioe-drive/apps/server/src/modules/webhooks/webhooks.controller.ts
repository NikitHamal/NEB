import { BadRequestException, Controller, Logger, Post, Req, type RawBodyRequest } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { SkipThrottle } from "@nestjs/throttler";
import { verifyWebhook } from "@clerk/backend/webhooks";
import type { Request } from "express";

import { toFetchRequest } from "../../common/utils/fetch-request";
import { WebhooksService } from "./webhooks.service";

@Controller("webhooks")
@SkipThrottle()
export class WebhooksController {
  private readonly logger = new Logger(WebhooksController.name);

  constructor(
    private readonly webhooksService: WebhooksService,
    private readonly configService: ConfigService,
  ) {}

  // Needs the untouched raw body for signature verification (see main.ts's rawBody: true option).
  @Post("clerk")
  async handleClerkWebhook(@Req() req: RawBodyRequest<Request>): Promise<void> {
    if (!req.rawBody) {
      throw new BadRequestException("Missing request body");
    }

    let event;
    try {
      event = await verifyWebhook(toFetchRequest(req, req.rawBody), {
        signingSecret: this.configService.getOrThrow<string>("CLERK_WEBHOOK_SIGNING_SECRET"),
      });
    } catch (error) {
      this.logger.warn(`Webhook verification failed: ${error instanceof Error ? error.message : error}`);
      throw new BadRequestException("Webhook verification failed");
    }

    const svixId = req.get("svix-id");
    if (!svixId) {
      throw new BadRequestException("Missing svix-id header");
    }

    this.logger.log(`Received event: ${event.type} (ID: ${event.data.id ?? "N/A"})`);

    switch (event.type) {
      case "user.created":
        await this.webhooksService.handleUserCreated(svixId, event);
        break;
      case "user.updated":
        await this.webhooksService.handleUserUpdated(svixId, event);
        break;
      case "user.deleted":
        await this.webhooksService.handleUserDeleted(svixId, event);
        break;
      default:
        this.logger.warn(`Unhandled event type: ${event.type}`);
    }
  }
}
