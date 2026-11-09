import type { ModerationReason, ResourceType } from "../entities";

export interface ReportResourcePreview {
    id: number;
    title: string;
    type: ResourceType;
    subjectOffering: {
        id: number;
        subject: { code: string };
    };
}

export interface ReportReporterSummary {
    id: number;
    fullName: string;
}

// Reporter's identity is only ever exposed here, never on any uploader- or public-facing response.
export interface ReportItem {
    id: number;
    resourceId: number;
    reportedBy: number;
    reason: ModerationReason;
    note: string | null;
    status: "OPEN" | "RESOLVED";
    createdAt: string;
    resolvedAt: string | null;
    resource: ReportResourcePreview;
    reporter: ReportReporterSummary;
}
