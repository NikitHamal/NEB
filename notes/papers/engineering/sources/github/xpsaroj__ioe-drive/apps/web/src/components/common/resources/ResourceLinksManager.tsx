"use client";
import { useState } from "react";
import { ExternalLink, Link as LinkIcon, Plus, Trash2 } from "lucide-react";
import { toast } from "sonner";

import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { getHostname } from "./ResourceLinkItem";
import { useAddResourceLinks, useRemoveResourceLink } from "@/hooks/queries/use-resources";
import { resourceLinkSchema, MAX_RESOURCE_LINKS } from "@/lib/validators/resource-links";
import { getErrorMessage } from "@/lib/errors";
import type { ResourceLinkSummary, ResourceSummary } from "@/types/api";

interface ResourceLinksManagerProps {
    resource: ResourceSummary;
}

const ExistingLinkRow = ({
    link,
    onRemove,
    disabled,
}: {
    link: ResourceLinkSummary;
    onRemove: () => void;
    disabled: boolean;
}) => (
    <div className="flex items-center gap-2.5 rounded-lg border border-border p-2">
        <span className="flex size-9 shrink-0 items-center justify-center rounded-md bg-background-tertiary text-foreground-secondary">
            <ExternalLink className="size-4" />
        </span>
        <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium text-foreground">{link.label}</p>
            <p className="truncate font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">{getHostname(link.url)}</p>
        </div>
        <button
            type="button"
            onClick={onRemove}
            disabled={disabled}
            aria-label={`Remove ${link.label}`}
            className="shrink-0 rounded-md p-1 text-foreground-tertiary transition-colors hover:bg-background-tertiary hover:text-error disabled:cursor-not-allowed disabled:opacity-60"
        >
            <Trash2 className="size-4" />
        </button>
    </div>
);

// Unlike the upload form's staged queue, add/remove here applies immediately - no confirm step.
const ResourceLinksManager = ({ resource }: ResourceLinksManagerProps) => {
    const [url, setUrl] = useState("");
    const [label, setLabel] = useState("");
    const [fieldError, setFieldError] = useState<string | null>(null);

    const { mutate: addLinks, isPending: isAdding } = useAddResourceLinks(resource.id);
    const { mutate: removeLink, isPending: isRemoving } = useRemoveResourceLink(resource.id);
    const links = resource.links ?? [];

    const handleAdd = () => {
        if (links.length >= MAX_RESOURCE_LINKS) {
            setFieldError(`A resource can have at most ${MAX_RESOURCE_LINKS} links.`);
            return;
        }

        const result = resourceLinkSchema.safeParse({ url, label });
        if (!result.success) {
            setFieldError(result.error.issues[0]?.message ?? "Enter a valid link.");
            return;
        }

        setFieldError(null);
        addLinks([result.data], {
            onSuccess: () => {
                toast.success("Link added successfully.");
                setUrl("");
                setLabel("");
            },
            onError: (error) => {
                toast.error(getErrorMessage(error, "Couldn't add the link. Please try again."));
            },
        });
    };

    const handleRemove = (linkId: number, linkLabel: string) => {
        removeLink(linkId, {
            onSuccess: () => {
                toast.success(`Removed "${linkLabel}".`);
            },
            onError: (error) => {
                toast.error(getErrorMessage(error, "Couldn't remove the link. Please try again."));
            },
        });
    };

    return (
        <div className="space-y-4">
            <div className="space-y-3 rounded-lg border border-border p-4">
                <Input
                    label="Link URL"
                    placeholder="https://..."
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    disabled={isAdding}
                />
                <Input
                    label="Label"
                    placeholder="e.g. Recommended lecture playlist"
                    value={label}
                    onChange={(e) => setLabel(e.target.value)}
                    disabled={isAdding}
                />
                {fieldError && <p className="text-xs text-error">{fieldError}</p>}
                <Button
                    type="button"
                    variant="secondary"
                    size="sm"
                    icon={<Plus className="size-4" />}
                    onClick={handleAdd}
                    disabled={isAdding}
                    className="w-full"
                >
                    {isAdding ? "Adding..." : "Add Link"}
                </Button>
            </div>

            <p className="text-sm text-foreground-tertiary">
                Changes here save instantly, no need to hit Save Changes.
            </p>

            {links.length === 0 ? (
                <div className="flex items-center gap-2 rounded-lg border border-border p-4 text-sm text-foreground-tertiary">
                    <LinkIcon className="size-4 shrink-0" />
                    No links attached to this resource.
                </div>
            ) : (
                <div className="rounded-lg border border-border p-4">
                    <div className="mb-3 flex items-center justify-between gap-4">
                        <p className="font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                            Links ({links.length})
                        </p>
                    </div>
                    <div className="flex flex-col gap-2">
                        {links.map((link) => (
                            <ExistingLinkRow
                                key={link.id}
                                link={link}
                                disabled={isRemoving}
                                onRemove={() => handleRemove(link.id, link.label)}
                            />
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ResourceLinksManager;
