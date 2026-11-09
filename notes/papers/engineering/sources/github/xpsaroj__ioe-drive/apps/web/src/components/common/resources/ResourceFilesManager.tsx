"use client";
import { useState } from "react";
import { CloudUpload, File as FileIcon, Trash2 } from "lucide-react";
import { toast } from "sonner";

import { cn } from "@/utils/cn";
import { formatFileSize, partitionUploadableFiles, MAX_FILES_PER_UPLOAD, ACCEPTED_UPLOAD_FILE_EXTENSIONS } from "@/utils/file";
import { useAddResourceFiles, useRemoveResourceFile } from "@/hooks/queries/use-resources";
import { getErrorMessage } from "@/lib/errors";
import { FILE_TYPE_META, DEFAULT_FILE_TYPE_META } from "./ResourceFileItem";
import { getMimeKey } from "./MimeTypeBadge";
import type { ResourceFileSummary, ResourceSummary } from "@/types/api";

interface ResourceFilesManagerProps {
    resource: ResourceSummary;
}

const ExistingFileRow = ({
    file,
    onRemove,
    disabled,
}: {
    file: ResourceFileSummary;
    onRemove: () => void;
    disabled: boolean;
}) => {
    const { icon: Icon, className } = FILE_TYPE_META[getMimeKey(file.mimeType)] ?? DEFAULT_FILE_TYPE_META;

    return (
        <div className="flex items-center gap-2.5 rounded-lg border border-border p-2">
            <span className={cn("flex size-9 shrink-0 items-center justify-center rounded-md", className)}>
                <Icon className="size-4" />
            </span>
            <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-foreground">{file.originalFileName}</p>
                <p className="font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">{formatFileSize(file.fileSize)}</p>
            </div>
            <button
                type="button"
                onClick={onRemove}
                disabled={disabled}
                aria-label={`Remove ${file.originalFileName}`}
                className="shrink-0 rounded-md p-1 text-foreground-tertiary transition-colors hover:bg-background-tertiary hover:text-error disabled:cursor-not-allowed disabled:opacity-60"
            >
                <Trash2 className="size-4" />
            </button>
        </div>
    );
};

// Unlike the upload form's staged queue, add/remove here applies immediately - no confirm step.
const ResourceFilesManager = ({ resource }: ResourceFilesManagerProps) => {
    const [isDragging, setIsDragging] = useState(false);
    const { mutate: addFiles, isPending: isAdding } = useAddResourceFiles(resource.id);
    const { mutate: removeFile, isPending: isRemoving } = useRemoveResourceFile(resource.id);
    const files = resource.files ?? [];

    const uploadFiles = (incoming: File[]) => {
        if (isAdding || incoming.length === 0) return;

        const alreadyQueuedBytes = files.reduce((total, file) => total + file.fileSize, 0);
        const { accepted, rejected } = partitionUploadableFiles(incoming, files.length, alreadyQueuedBytes);

        if (rejected.length > 0) {
            toast.error(`Couldn't add ${rejected.join(", ")}`);
        }
        if (accepted.length === 0) return;

        const formData = new FormData();
        accepted.forEach((file) => formData.append("resourceFile", file));

        addFiles(formData, {
            onSuccess: () => {
                toast.success(accepted.length > 1 ? "Files added successfully." : "File added successfully.");
            },
            onError: (error) => {
                toast.error(getErrorMessage(error, "Couldn't add the file. Please try again."));
            },
        });
    };

    const handleFilesSelected = (e: React.ChangeEvent<HTMLInputElement>) => {
        uploadFiles(Array.from(e.target.files ?? []));
        e.target.value = "";
    };

    const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(false);
        uploadFiles(Array.from(e.dataTransfer.files ?? []));
    };

    const handleRemove = (fileId: number, fileName: string) => {
        removeFile(fileId, {
            onSuccess: () => {
                toast.success(`Removed "${fileName}".`);
            },
            onError: (error) => {
                toast.error(getErrorMessage(error, "Couldn't remove the file. Please try again."));
            },
        });
    };

    return (
        <div className="space-y-4">
            {/* <div>
                <h2 className="text-lg font-semibold text-foreground">Files</h2>
                <p className="mt-0.5 text-xs text-foreground-tertiary">
                    Changes here save instantly &mdash; no need to hit Save Changes.
                </p>
            </div> */}

            <div
                onDragOver={(e) => {
                    e.preventDefault();
                    if (!isAdding) setIsDragging(true);
                }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
                onClick={() => !isAdding && document.getElementById("resourceFilesManagerInput")?.click()}
                className={cn(
                    "rounded-lg border-2 border-dashed p-8 text-center transition-colors",
                    isAdding ? "cursor-not-allowed opacity-60" : "cursor-pointer hover:border-foreground-tertiary",
                    isDragging ? "border-accent bg-accent/5" : "border-border",
                )}
            >
                <span className="mx-auto mb-4 flex size-12 items-center justify-center rounded-full bg-accent text-accent-foreground">
                    <CloudUpload className="size-6" />
                </span>
                <p className="font-semibold text-foreground">Drag & Drop files here</p>
                <p className="mt-1 text-sm text-foreground-secondary">or click to browse from your computer</p>
                <p className="mt-4 inline-block rounded-md bg-background-tertiary px-3 py-1.5 font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">
                    PDF, DOCX, JPG, PNG | up to 50 MB total | max {MAX_FILES_PER_UPLOAD} files
                </p>
                <input
                    id="resourceFilesManagerInput"
                    type="file"
                    multiple
                    accept={ACCEPTED_UPLOAD_FILE_EXTENSIONS}
                    onChange={handleFilesSelected}
                    disabled={isAdding}
                    className="hidden"
                />
            </div>

            <p className="text-sm text-foreground-tertiary">
                Changes here save instantly, no need to hit Save Changes.
            </p>

            {files.length === 0 ? (
                <div className="flex items-center gap-2 rounded-lg border border-border p-4 text-sm text-foreground-tertiary">
                    <FileIcon className="size-4 shrink-0" />
                    No files attached to this resource.
                </div>
            ) : (
                <div className="rounded-lg border border-border p-4">
                    <div className="mb-3 flex items-center justify-between gap-4">
                        <p className="font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                            Files ({files.length})
                        </p>
                    </div>
                    <div className="flex flex-col gap-2">
                        {files.map((file) => (
                            <ExistingFileRow
                                key={file.id}
                                file={file}
                                disabled={isRemoving}
                                onRemove={() => handleRemove(file.id, file.originalFileName)}
                            />
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ResourceFilesManager;
