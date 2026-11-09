import { Pencil } from "lucide-react";

import Button from "@/components/ui/Button";
import type { ResourceSummary } from "@/types/api";
import { ResourceStatus } from "@/types/entities";

interface EditResourceButtonProps {
    resource: ResourceSummary;
}

const EditResourceButton = ({ resource }: EditResourceButtonProps) => {
    // A REMOVED resource's files were already purged by moderation - it's terminal, no editing.
    if (resource.status === ResourceStatus.REMOVED) return null;

    return (
        <Button
            href={`/resources/r/${resource.id}/edit`}
            variant="ghost"
            size="xs"
            iconOnly
            icon={<Pencil className="size-4" />}
            className="text-foreground-secondary hover:text-info hover:bg-info/10"
            aria-label="Edit resource"
        />
    );
};

export default EditResourceButton;
