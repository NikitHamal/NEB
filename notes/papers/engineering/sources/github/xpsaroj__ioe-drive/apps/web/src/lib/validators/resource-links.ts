import { z } from "zod";

// Mirrors apps/server's ResourceLinkInput DTO - kept in sync manually.
export const MAX_RESOURCE_LINKS = 5;

export const resourceLinkSchema = z.object({
    url: z.url("Enter a valid URL, including https://"),
    label: z.string().min(1, "Label is required").max(100, "Label must be at most 100 characters"),
});

export type ResourceLinkInput = z.infer<typeof resourceLinkSchema>;
