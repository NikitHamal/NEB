import { Injectable, Logger } from "@nestjs/common";
import type { UserJSON, UserWebhookEvent } from "@clerk/backend";

import { UsersRepository, type WebhookProfileData, type WebhookUserData } from "../users/users.repository";
import { WebhookEventsRepository } from "./webhook-events.repository";

@Injectable()
export class WebhooksService {
  private readonly logger = new Logger(WebhooksService.name);

  constructor(
    private readonly usersRepository: UsersRepository,
    private readonly webhookEventsRepository: WebhookEventsRepository,
  ) {}

  private getFullName(firstName: string | null, lastName: string | null): string {
    const first = firstName?.trim() || "";
    const last = lastName?.trim() || "";
    return `${first} ${last}`.trim() || "User";
  }

  private getPrimaryEmail(data: UserJSON): string | null {
    if (data.primary_email_address_id) {
      const primaryEmail = data.email_addresses.find((email) => email.id === data.primary_email_address_id);
      if (primaryEmail) {
        return primaryEmail.email_address;
      }
    }

    return data.email_addresses[0]?.email_address ?? null;
  }

  async handleUserCreated(svixId: string, event: UserWebhookEvent): Promise<void> {
    if (await this.webhookEventsRepository.alreadyProcessed(svixId)) {
      this.logger.log("Duplicate webhook skipped");
      return;
    }

    const data = event.data as UserJSON;
    const userData: WebhookUserData = {
      clerkUserId: data.id,
      fullName: this.getFullName(data.first_name, data.last_name),
      email: this.getPrimaryEmail(data),
    };
    const profileData: WebhookProfileData = { profilePictureUrl: data.image_url };

    await this.usersRepository.createFromWebhook(userData, profileData);
    await this.webhookEventsRepository.markProcessed(svixId, event.type);
  }

  async handleUserUpdated(svixId: string, event: UserWebhookEvent): Promise<void> {
    if (await this.webhookEventsRepository.alreadyProcessed(svixId)) {
      this.logger.log("Duplicate webhook skipped");
      return;
    }

    const data = event.data as UserJSON;
    const userData: WebhookUserData = {
      clerkUserId: data.id,
      fullName: this.getFullName(data.first_name, data.last_name),
      email: this.getPrimaryEmail(data),
    };
    const profileData: WebhookProfileData = { profilePictureUrl: data.image_url };

    const updatedUser = await this.usersRepository.updateFromWebhook(userData, profileData);

    if (!updatedUser) {
      this.logger.warn(`User to update not found: ${data.id}`);
      await this.usersRepository.createFromWebhook(userData, profileData);
      this.logger.log(`User created during update: ${data.id}`);
    }

    await this.webhookEventsRepository.markProcessed(svixId, event.type);
  }

  async handleUserDeleted(svixId: string, event: UserWebhookEvent): Promise<void> {
    if (await this.webhookEventsRepository.alreadyProcessed(svixId)) {
      this.logger.log("Duplicate webhook skipped");
      return;
    }

    const clerkUserId = event.data.id;
    if (clerkUserId) {
      await this.usersRepository.deleteByClerkUserId(clerkUserId);
    }

    await this.webhookEventsRepository.markProcessed(svixId, event.type);
  }
}
