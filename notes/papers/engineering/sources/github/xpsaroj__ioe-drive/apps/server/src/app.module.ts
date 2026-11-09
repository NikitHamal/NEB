import { Module } from "@nestjs/common";
import { ConfigModule } from "@nestjs/config";
import { APP_GUARD } from "@nestjs/core";
import { ThrottlerGuard, ThrottlerModule } from "@nestjs/throttler";

import { ClerkModule } from "./clerk/clerk.module";
import { resolveEnvFilePath, validate } from "./config/env.validation";
import { DatabaseModule } from "./database/database.module";
import { AdminModule } from "./modules/admin/admin.module";
import { HealthModule } from "./modules/health/health.module";
import { MarketplaceModule } from "./modules/marketplace/marketplace.module";
import { MeModule } from "./modules/me/me.module";
import { MessagingModule } from "./modules/messaging/messaging.module";
import { ModerationModule } from "./modules/moderation/moderation.module";
import { NotificationsModule } from "./modules/notifications/notifications.module";
import { ProgramsModule } from "./modules/programs/programs.module";
import { ResourcesModule } from "./modules/resources/resources.module";
import { SubjectsModule } from "./modules/subjects/subjects.module";
import { UsersModule } from "./modules/users/users.module";
import { WebhooksModule } from "./modules/webhooks/webhooks.module";
import { AzureBlobModule } from "./storage/azure-blob.module";

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: resolveEnvFilePath(),
      validate,
    }),
    // 500 requests / 15 minutes per IP - health and the Clerk webhook opt out via @SkipThrottle().
    ThrottlerModule.forRoot([
      {
        ttl: 15 * 60 * 1000,
        limit: 500,
      },
    ]),
    DatabaseModule,
    ClerkModule,
    AzureBlobModule,
    HealthModule,
    ProgramsModule,
    SubjectsModule,
    UsersModule,
    MeModule,
    ResourcesModule,
    MarketplaceModule,
    MessagingModule,
    ModerationModule,
    NotificationsModule,
    AdminModule,
    WebhooksModule,
  ],
  providers: [
    {
      provide: APP_GUARD,
      useClass: ThrottlerGuard,
    },
  ],
})
export class AppModule {}
