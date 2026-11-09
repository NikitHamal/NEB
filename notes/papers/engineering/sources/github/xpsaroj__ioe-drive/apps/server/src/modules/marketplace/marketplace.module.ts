import { Module } from "@nestjs/common";

import { ModerationModule } from "../moderation/moderation.module";
import { MarketplaceListingsController } from "./marketplace-listings.controller";
import { MarketplaceListingsRepository } from "./marketplace-listings.repository";
import { MarketplaceListingsService } from "./marketplace-listings.service";

@Module({
  imports: [ModerationModule],
  controllers: [MarketplaceListingsController],
  providers: [MarketplaceListingsService, MarketplaceListingsRepository],
  exports: [MarketplaceListingsService, MarketplaceListingsRepository],
})
export class MarketplaceModule {}
