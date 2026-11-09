"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm, Controller, useWatch } from "react-hook-form";
import { toast } from "sonner";
import { CloudUpload, ExternalLink, File, Link as LinkIcon, Plus, Send, Trash2, X } from "lucide-react";

import Select from "@/components/ui/Select";
import Input from "@/components/ui/Input";
import Textarea from "@/components/ui/Textarea";
import Button from "@/components/ui/Button";
import Loader from "@/components/ui/Loader";
import { getErrorMessage } from "@/lib/errors";
import { cn } from "@/utils/cn";
import {
    formatFileSize,
    partitionUploadableFiles,
    MAX_FILES_PER_UPLOAD,
    ACCEPTED_UPLOAD_FILE_EXTENSIONS,
} from "@/utils/file";
import { resourceLinkSchema, MAX_RESOURCE_LINKS, type ResourceLinkInput } from "@/lib/validators/resource-links";
import { usePrograms, useSubjectsForUpload } from "@/hooks/queries/use-academics";
import { useCreateResource } from "@/hooks/queries/use-resources";
import { FILE_TYPE_META, DEFAULT_FILE_TYPE_META } from "./ResourceFileItem";
import { getHostname } from "./ResourceLinkItem";
import { getMimeKey } from "./MimeTypeBadge";
import { Semester, SemesterLabel, ResourceType, ResourceTypeLabel } from "@/types/entities";

type FormValues = {
    title: string;
    description: string;
    programId: string;
    type: ResourceType | "";
    semester: Semester | "";
    offeringId: string;
    files: File[];
    links: ResourceLinkInput[];
};

const UploadQueueRow = ({ file, onRemove }: { file: File; onRemove: () => void }) => {
    const { icon: Icon, className } = FILE_TYPE_META[getMimeKey(file.type)] ?? DEFAULT_FILE_TYPE_META;

    return (
        <div className="flex items-center gap-2.5 rounded-lg border border-border p-2">
            <span className={cn("flex size-9 shrink-0 items-center justify-center rounded-md", className)}>
                <Icon className="size-4" />
            </span>
            <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-foreground">{file.name}</p>
                <p className="font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">{formatFileSize(file.size)}</p>
            </div>
            <button
                type="button"
                onClick={onRemove}
                aria-label={`Remove ${file.name}`}
                className="shrink-0 rounded-md p-1 text-foreground-tertiary transition-colors hover:bg-background-tertiary hover:text-error"
            >
                <X className="size-4" />
            </button>
        </div>
    );
};

export const ResourceUploadForm: React.FC = () => {
    const router = useRouter();

    const { data: programs, isPending: programsPending, error: programsLoadError } = usePrograms();
    const { mutate, isPending: isUploading } = useCreateResource();

    const [isDragging, setIsDragging] = useState(false);
    const [linkUrl, setLinkUrl] = useState("");
    const [linkLabel, setLinkLabel] = useState("");
    const [linkError, setLinkError] = useState<string | null>(null);

    const {
        handleSubmit,
        control,
        register,
        setValue,
        setError,
        clearErrors,
        reset,
        formState: { errors },
    } = useForm<FormValues>({
        defaultValues: {
            title: "",
            description: "",
            programId: "",
            type: "",
            semester: "",
            offeringId: "",
            files: [],
            links: [],
        },
    });

    const files = useWatch({ control, name: "files" });
    const links = useWatch({ control, name: "links" });

    const selectedProgramId = useWatch({
        control,
        name: "programId",
    });

    const selectedSemester = useWatch({
        control,
        name: "semester",
    });

    const {
        data: subjects,
        isFetching: subjectsFetching,
    } = useSubjectsForUpload(
        selectedProgramId ? Number(selectedProgramId) : undefined,
        selectedSemester || undefined,
    );

    const addFiles = (incoming: File[]) => {
        if (isUploading || incoming.length === 0) return;

        // Silently drop exact duplicates (same name+size already queued).
        const newFiles = incoming.filter(
            (file) => !files.some((existing) => existing.name === file.name && existing.size === file.size)
        );
        const alreadyQueuedBytes = files.reduce((total, file) => total + file.size, 0);
        const { accepted, rejected } = partitionUploadableFiles(newFiles, files.length, alreadyQueuedBytes);

        if (rejected.length > 0) {
            toast.error(`Couldn't add ${rejected.join(", ")}`);
        }

        if (accepted.length === 0) return;

        const combined = [...files, ...accepted];
        setValue("files", combined, { shouldValidate: true });
        clearErrors("files");
    };

    const removeFile = (index: number) => {
        const next = [...files];
        next.splice(index, 1);
        setValue("files", next, { shouldValidate: true });
    };

    const clearAllFiles = () => setValue("files", [], { shouldValidate: true });

    const addLink = () => {
        if (links.length >= MAX_RESOURCE_LINKS) {
            setLinkError(`A resource can have at most ${MAX_RESOURCE_LINKS} links.`);
            return;
        }

        const result = resourceLinkSchema.safeParse({ url: linkUrl, label: linkLabel });
        if (!result.success) {
            setLinkError(result.error.issues[0]?.message ?? "Enter a valid link.");
            return;
        }

        setLinkError(null);
        setValue("links", [...links, result.data], { shouldValidate: true });
        clearErrors("files");
        setLinkUrl("");
        setLinkLabel("");
    };

    const removeLink = (index: number) => {
        const next = [...links];
        next.splice(index, 1);
        setValue("links", next, { shouldValidate: true });
    };

    const handleFileDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(false);
        addFiles(Array.from(e.dataTransfer.files ?? []));
    };

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        addFiles(Array.from(e.target.files ?? []));
        e.target.value = "";
    };

    const onSubmit = (data: FormValues) => {
        if (data.files.length === 0 && data.links.length === 0) {
            setError("files", { type: "manual", message: "Add at least one file or link." });
            return;
        }

        const formData = new FormData();
        formData.append("title", data.title);
        formData.append("description", data.description);
        formData.append("offeringId", data.offeringId);
        formData.append("type", data.type);
        data.files.forEach((file) => formData.append("resourceFile", file));
        if (data.links.length > 0) {
            formData.append("links", JSON.stringify(data.links));
        }

        mutate(formData, {
            onSuccess: () => {
                toast.success("Resource submitted! It's pending review and will go live once a moderator approves it.");
                reset();
            },
            onError: (error) => {
                toast.error(getErrorMessage(error, "Couldn't upload the resource. Please try again."));
            },
        });
    };

    if (programsPending) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <div className="flex flex-col items-center justify-center">
                    <Loader text="Loading. Please wait." />
                </div>
            </div>
        );
    }

    if (programsLoadError || !programs) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
                <div className="flex flex-col items-center justify-center">
                    <p className="text-error">{getErrorMessage(programsLoadError, "Couldn't load the page. Please try again.")}</p>
                    <div className="flex space-x-4">
                        <Button variant="primary" className="mt-4" onClick={() => router.back()}>
                            Go Back
                        </Button>
                    </div>
                </div>
            </div>
        );
    }

    const bothSelected = !!(selectedProgramId && selectedSemester);

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6" noValidate>
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 lg:items-start">
                {/* Resource Details */}
                <div className="space-y-4 rounded-lg md:border border-border md:p-6">
                    <h2 className="text-lg font-semibold text-foreground">Resource Details</h2>

                    <Input
                        label="Document Title"
                        placeholder="e.g. Midterm Study Guide"
                        required
                        error={errors.title?.message}
                        disabled={isUploading}
                        {...register("title", {
                            required: "Document title is required",
                            minLength: { value: 3, message: "Title must be at least 3 characters" },
                            maxLength: { value: 100, message: "Title must be less than 100 characters" },
                        })}
                    />

                    <Controller
                        control={control}
                        name="type"
                        rules={{ required: "Resource type is required" }}
                        render={({ field }) => (
                            <Select
                                label="Resource Type"
                                placeholder="Select Type"
                                required
                                value={field.value}
                                error={errors.type?.message}
                                disabled={isUploading}
                                onChange={field.onChange}
                                options={Object.values(ResourceType).map((type) => ({
                                    value: type,
                                    label: ResourceTypeLabel[type],
                                }))}
                            />
                        )}
                    />

                    <Textarea
                        label="Description"
                        placeholder="Brief details about the content..."
                        required
                        rows={3}
                        error={errors.description?.message}
                        disabled={isUploading}
                        {...register("description", {
                            required: "Description is required",
                            minLength: { value: 10, message: "Description must be at least 10 characters" },
                            maxLength: { value: 200, message: "Description must be less than 200 characters" },
                        })}
                    />

                    <div className="space-y-4 rounded-lg border border-border bg-background-secondary p-4">
                        <p className="font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                            Categorization
                        </p>

                        <Controller
                            control={control}
                            name="programId"
                            rules={{ required: "Program is required" }}
                            render={({ field }) => (
                                <Select
                                    label="Program"
                                    placeholder="Select Program"
                                    required
                                    value={field.value}
                                    error={errors.programId?.message}
                                    disabled={isUploading}
                                    onChange={(e) => {
                                        field.onChange(e);
                                        setValue("semester", "");
                                        setValue("offeringId", "");
                                    }}
                                    options={programs.map((prog) => ({
                                        value: String(prog.id),
                                        label: `${prog.code} - ${prog.name}`,
                                    }))}
                                />
                            )}
                        />

                        <Controller
                            control={control}
                            name="semester"
                            rules={{ required: "Semester is required" }}
                            render={({ field }) => (
                                <Select
                                    label="Semester"
                                    placeholder="Select Semester"
                                    required
                                    value={field.value}
                                    error={errors.semester?.message}
                                    disabled={!selectedProgramId || isUploading}
                                    onChange={(e) => {
                                        field.onChange(e);
                                        setValue("offeringId", "");
                                    }}
                                    options={Object.keys(SemesterLabel).map((sem) => ({
                                        value: sem,
                                        label: `${SemesterLabel[sem as Semester]} ${+sem > 8 ? "(Architecture)" : ""}`,
                                    }))}
                                />
                            )}
                        />

                        <Controller
                            control={control}
                            name="offeringId"
                            rules={{ required: "Subject is required" }}
                            render={({ field }) => (
                                <Select
                                    label="Subject"
                                    placeholder={
                                        !bothSelected
                                            ? "Select program and semester first"
                                            : subjectsFetching
                                                ? "Loading subjects..."
                                                : "Select Subject"
                                    }
                                    required
                                    value={field.value}
                                    error={errors.offeringId?.message}
                                    disabled={!bothSelected || subjectsFetching || isUploading}
                                    onChange={field.onChange}
                                    options={
                                        subjects?.map((offering) => ({
                                            value: String(offering.id),
                                            label: `${offering.subject.code} - ${offering.subject.name}${offering.isElective ? " (Elective)" : ""}`,
                                        })) ?? []
                                    }
                                />
                            )}
                        />
                    </div>
                </div>

                {/* File upload */}
                <div className="space-y-4">
                    <div
                        onDragOver={(e) => {
                            e.preventDefault();
                            if (!isUploading) setIsDragging(true);
                        }}
                        onDragLeave={() => setIsDragging(false)}
                        onDrop={handleFileDrop}
                        onClick={() => !isUploading && document.getElementById("resourceFileInput")?.click()}
                        className={cn(
                            "rounded-lg border-2 border-dashed p-8 text-center transition-colors",
                            isUploading ? "cursor-not-allowed opacity-60" : "cursor-pointer hover:border-foreground-tertiary",
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
                            id="resourceFileInput"
                            type="file"
                            multiple
                            accept={ACCEPTED_UPLOAD_FILE_EXTENSIONS}
                            onChange={handleFileSelect}
                            disabled={isUploading}
                            className="hidden"
                        />
                    </div>
                    {errors.files && <p className="text-xs text-error">{errors.files.message}</p>}

                    {files.length > 0 && (
                        <div className="rounded-lg border border-border p-4">
                            <div className="mb-3 flex items-center justify-between gap-4">
                                <p className="font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                                    Upload Queue ({files.length})
                                </p>
                                <button
                                    type="button"
                                    onClick={clearAllFiles}
                                    disabled={isUploading}
                                    className="text-xs font-medium text-error hover:underline disabled:cursor-not-allowed disabled:opacity-60"
                                >
                                    Clear All
                                </button>
                            </div>
                            <div className="flex flex-col gap-2">
                                {files.map((file, index) => (
                                    <UploadQueueRow
                                        key={`${file.name}-${file.size}-${index}`}
                                        file={file}
                                        onRemove={() => removeFile(index)}
                                    />
                                ))}
                            </div>
                        </div>
                    )}

                    {files.length === 0 && links.length === 0 && (
                        <div className="flex items-center gap-2 rounded-lg border border-border p-4 text-sm text-foreground-tertiary">
                            <File className="size-4 shrink-0" />
                            At least one file or link is required.
                        </div>
                    )}

                    <div className="space-y-3 rounded-lg border border-border p-4">
                        <p className="font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                            Links (optional)
                        </p>
                        <Input
                            placeholder="https://..."
                            value={linkUrl}
                            onChange={(e) => setLinkUrl(e.target.value)}
                            disabled={isUploading}
                        />
                        <Input
                            placeholder="Label, e.g. Recommended lecture playlist"
                            value={linkLabel}
                            onChange={(e) => setLinkLabel(e.target.value)}
                            disabled={isUploading}
                        />
                        {linkError && <p className="text-xs text-error">{linkError}</p>}
                        <Button
                            type="button"
                            variant="secondary"
                            size="sm"
                            icon={<Plus className="size-4" />}
                            onClick={addLink}
                            disabled={isUploading}
                            className="w-full"
                        >
                            Add Link
                        </Button>

                        {links.length > 0 && (
                            <div className="flex flex-col gap-2 pt-1">
                                {links.map((link, index) => (
                                    <div key={`${link.url}-${index}`} className="flex items-center gap-2.5 rounded-lg border border-border p-2">
                                        <span className="flex size-9 shrink-0 items-center justify-center rounded-md bg-background-tertiary text-foreground-secondary">
                                            <ExternalLink className="size-4" />
                                        </span>
                                        <div className="min-w-0 flex-1">
                                            <p className="truncate text-sm font-medium text-foreground">{link.label}</p>
                                            <p className="truncate font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">{getHostname(link.url)}</p>
                                        </div>
                                        <button
                                            type="button"
                                            onClick={() => removeLink(index)}
                                            aria-label={`Remove ${link.label}`}
                                            className="shrink-0 rounded-md p-1 text-foreground-tertiary transition-colors hover:bg-background-tertiary hover:text-error"
                                        >
                                            <Trash2 className="size-4" />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}

                        {links.length === 0 && (
                            <div className="flex items-center gap-2 text-xs text-foreground-tertiary">
                                <LinkIcon className="size-3.5 shrink-0" />
                                No links added yet.
                            </div>
                        )}
                    </div>
                </div>
            </div>

            <div className="flex flex-col gap-4 border-t border-border pt-6 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-sm leading-relaxed text-foreground-secondary sm:max-w-xl">
                    By uploading, you confirm this is your own work or you have permission to share it, and that it
                    doesn&apos;t infringe on anyone&apos;s copyright. You&apos;re responsible for what you share -
                    resources are reviewed before going live, and inappropriate or infringing content may be
                    rejected or removed.
                </p>
                <Button
                    type="submit"
                    icon={<Send className="size-4" />}
                    disabled={isUploading}
                    className="shrink-0"
                >
                    {isUploading ? "Submitting..." : "Submit Resource"}
                </Button>
            </div>
        </form>
    );
};
