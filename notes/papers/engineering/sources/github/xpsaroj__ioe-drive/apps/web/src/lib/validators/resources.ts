import { z } from "zod";

import { ModerationReason, ResourceType } from "@/types/entities";

export const createResourceSchema = z.object({
    title: z.string().min(1, "Title is required").max(255, "Title must be at most 255 characters"),
    description: z.string().max(1000, "Description must be at most 1000 characters"),
    type: z.enum(ResourceType),
    offeringId: z.number().int().positive("Subject ID must be a positive integer"),
})

export type CreateResourceInput = z.infer<typeof createResourceSchema>;
export type UpdateResourceInput = Partial<CreateResourceInput>;

// Shared by moderator reject/remove and report - same shape as the backend's ModerateResourceDto/ReportResourceDto.
export const moderationReasonSchema = z.object({
    reason: z.enum(ModerationReason),
    note: z.string().max(1000, "Note must be at most 1000 characters").optional(),
});

export type ModerationReasonInput = z.infer<typeof moderationReasonSchema>;
