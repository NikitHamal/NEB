import { z } from "zod";

import { MarketplaceCategory, MarketplaceListingType, MarketplaceReportReason } from "@/types/entities";

export const createListingSchema = z.object({
    title: z.string().min(3, "Title must be at least 3 characters").max(255, "Title must be at most 255 characters"),
    description: z.string().min(10, "Description must be at least 10 characters").max(1000, "Description must be at most 1000 characters"),
    type: z.enum(MarketplaceListingType),
    category: z.enum(MarketplaceCategory),
    price: z.number().int().min(0, "Price can't be negative").optional(),
    offeringId: z.number().int().positive("Subject ID must be a positive integer").optional(),
});

export type CreateListingInput = z.infer<typeof createListingSchema>;
export type UpdateListingInput = Partial<CreateListingInput>;

// Shared by moderator remove and report - same shape as the backend's ModerateListingDto/ReportListingDto.
export const marketplaceReportReasonSchema = z.object({
    reason: z.enum(MarketplaceReportReason),
    note: z.string().max(1000, "Note must be at most 1000 characters").optional(),
});

export type MarketplaceReportReasonInput = z.infer<typeof marketplaceReportReasonSchema>;
