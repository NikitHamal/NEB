import type { ModerationReason, ResourceStatus, ResourceType } from "../../database/schema";

// Count-only cap (links don't cost storage/bandwidth like files do) - a separate pool from MAX_RESOURCE_FILES.
export const MAX_RESOURCE_LINKS = 5;

export interface CreateResourceData {
  title: string;
  description: string;
  type: ResourceType;
  offeringId: number;
  uploadedBy: number;
  status: ResourceStatus;
}

export interface UpdateResourceData {
  title?: string;
  description?: string;
  type?: ResourceType;
  offeringId?: number;
  // Not client-settable via UpdateResourceDto - only ResourcesService sets these (implicit resubmission).
  status?: ResourceStatus;
  moderatedBy?: number | null;
  moderationReason?: ModerationReason | null;
  moderationNote?: string | null;
  moderatedAt?: Date | null;
}

export interface ModerateResourceData {
  status: ResourceStatus;
  moderatedBy: number;
  moderationReason: ModerationReason | null;
  moderationNote: string | null;
  moderatedAt: Date;
}
