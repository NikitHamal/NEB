"use client";
import { Download } from "lucide-react";

import VoteButtons from "./VoteButtons";
import { useMe } from "@/hooks/queries/use-me";
import type { ResourceStatus } from "@/types/entities";

interface ResourceEngagementRowProps {
    resourceId: number;
    upvoteCount: number;
    downvoteCount: number;
    downloadCount: number;
    uploadedBy?: number;
    status: ResourceStatus;
    className?: string;
}

const ResourceEngagementRow = ({ resourceId, upvoteCount, downvoteCount, downloadCount, uploadedBy, status, className = "" }: ResourceEngagementRowProps) => {
    const { data: userData } = useMe();

    return (
        <div className={`flex items-center gap-3 ${className}`}>
            {!!userData && (
                <VoteButtons resourceId={resourceId} upvoteCount={upvoteCount} downvoteCount={downvoteCount} uploadedBy={uploadedBy} status={status} />
            )}

            <span className="ms-auto flex items-center gap-1 shrink-0 text-xs text-foreground-tertiary" title={`${downloadCount} download${downloadCount === 1 ? "" : "s"}`}>
                <Download className="size-3.5" />
                {downloadCount}
            </span>
        </div>
    );
};

export default ResourceEngagementRow;
