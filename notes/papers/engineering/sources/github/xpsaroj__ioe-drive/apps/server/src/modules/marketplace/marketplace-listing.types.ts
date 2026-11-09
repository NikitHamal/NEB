import type { MarketplaceCategory, MarketplaceListingStatus, MarketplaceListingType, MarketplaceReportReason } from "../../database/schema";

export interface CreateListingData {
  title: string;
  description: string;
  type: MarketplaceListingType;
  category: MarketplaceCategory;
  price?: number;
  offeringId?: number;
  postedBy: number;
  status: MarketplaceListingStatus;
}

export interface UpdateListingData {
  title?: string;
  description?: string;
  type?: MarketplaceListingType;
  category?: MarketplaceCategory;
  price?: number;
  offeringId?: number;
}

export interface ModerateListingData {
  status: MarketplaceListingStatus;
  moderatedBy: number;
  moderationReason: MarketplaceReportReason | null;
  moderationNote: string | null;
  moderatedAt: Date;
}
