"use client";
import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { useForm, Controller, useWatch } from "react-hook-form";
import { toast } from "sonner";
import { CloudUpload, ImageIcon, Send, X } from "lucide-react";

import Select from "@/components/ui/Select";
import Input from "@/components/ui/Input";
import Textarea from "@/components/ui/Textarea";
import Button from "@/components/ui/Button";
import { getErrorMessage } from "@/lib/errors";
import { cn } from "@/utils/cn";
import { formatFileSize } from "@/utils/file";
import {
    partitionUploadablePhotos,
    MAX_LISTING_PHOTOS,
    ACCEPTED_LISTING_PHOTO_EXTENSIONS,
} from "@/utils/marketplace-file";
import { usePrograms, useSubjectsForUpload } from "@/hooks/queries/use-academics";
import { useCreateListing } from "@/hooks/queries/use-marketplace";
import {
    Semester,
    SemesterLabel,
    MarketplaceListingType,
    MarketplaceListingTypeLabel,
    MarketplaceCategory,
    MarketplaceCategoryLabel,
} from "@/types/entities";

type FormValues = {
    title: string;
    description: string;
    type: MarketplaceListingType | "";
    category: MarketplaceCategory | "";
    price: string;
    linkToSubject: boolean;
    programId: string;
    semester: Semester | "";
    offeringId: string;
    photos: File[];
};

const PhotoQueueRow = ({ file, onRemove }: { file: File; onRemove: () => void }) => {
    const previewUrl = useMemo(() => URL.createObjectURL(file), [file]);
    useEffect(() => () => URL.revokeObjectURL(previewUrl), [previewUrl]);

    return (
        <div className="flex items-center gap-2.5 rounded-lg border border-border p-2">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={previewUrl} alt={file.name} className="size-9 shrink-0 rounded-md object-cover" />
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

export const ListingUploadForm: React.FC = () => {
    const router = useRouter();

    const { mutate, isPending: isSubmitting } = useCreateListing();

    const [isDragging, setIsDragging] = useState(false);

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
            type: "",
            category: "",
            price: "",
            linkToSubject: false,
            programId: "",
            semester: "",
            offeringId: "",
            photos: [],
        },
    });

    const photos = useWatch({ control, name: "photos" });
    const linkToSubject = useWatch({ control, name: "linkToSubject" });
    const selectedProgramId = useWatch({ control, name: "programId" });
    const selectedSemester = useWatch({ control, name: "semester" });

    const { data: programs, isPending: programsPending } = usePrograms();
    const { data: subjects, isFetching: subjectsFetching } = useSubjectsForUpload(
        selectedProgramId ? Number(selectedProgramId) : undefined,
        selectedSemester || undefined,
    );

    const addPhotos = (incoming: File[]) => {
        if (isSubmitting || incoming.length === 0) return;

        const newFiles = incoming.filter(
            (file) => !photos.some((existing) => existing.name === file.name && existing.size === file.size)
        );
        const { accepted, rejected } = partitionUploadablePhotos(newFiles, photos.length);

        if (rejected.length > 0) {
            toast.error(`Couldn't add ${rejected.join(", ")}`);
        }

        if (accepted.length === 0) return;

        const combined = [...photos, ...accepted];
        setValue("photos", combined, { shouldValidate: true });
        clearErrors("photos");
    };

    const removePhoto = (index: number) => {
        const next = [...photos];
        next.splice(index, 1);
        setValue("photos", next, { shouldValidate: true });
    };

    const handlePhotoDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(false);
        addPhotos(Array.from(e.dataTransfer.files ?? []));
    };

    const handlePhotoSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        addPhotos(Array.from(e.target.files ?? []));
        e.target.value = "";
    };

    const onSubmit = (data: FormValues) => {
        if (data.photos.length === 0) {
            setError("photos", { type: "manual", message: "Add at least one photo." });
            return;
        }

        const formData = new FormData();
        formData.append("title", data.title);
        formData.append("description", data.description);
        formData.append("type", data.type);
        formData.append("category", data.category);
        if (data.price.trim()) formData.append("price", data.price.trim());
        if (data.linkToSubject && data.offeringId) formData.append("offeringId", data.offeringId);
        data.photos.forEach((file) => formData.append("listingPhoto", file));

        mutate(formData, {
            onSuccess: (response) => {
                toast.success("Listing submitted! It's pending review and will go live once a moderator approves it.");
                reset();
                router.push(`/market/${response.data.id}`);
            },
            onError: (error) => {
                toast.error(getErrorMessage(error, "Couldn't post the listing. Please try again."));
            },
        });
    };

    const bothSelected = !!(selectedProgramId && selectedSemester);

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6" noValidate>
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 lg:items-start">
                <div className="space-y-4 rounded-lg md:border border-border md:p-6">
                    <h2 className="text-lg font-semibold text-foreground">Listing Details</h2>

                    <Input
                        label="Title"
                        placeholder="e.g. Drafter Set, barely used"
                        required
                        error={errors.title?.message}
                        disabled={isSubmitting}
                        {...register("title", {
                            required: "Title is required",
                            minLength: { value: 3, message: "Title must be at least 3 characters" },
                            maxLength: { value: 255, message: "Title must be less than 255 characters" },
                        })}
                    />

                    <div className="grid gap-4">
                        <Controller
                            control={control}
                            name="type"
                            rules={{ required: "Type is required" }}
                            render={({ field }) => (
                                <Select
                                    label="Type"
                                    placeholder="Select Type"
                                    required
                                    value={field.value}
                                    error={errors.type?.message}
                                    disabled={isSubmitting}
                                    onChange={field.onChange}
                                    options={Object.values(MarketplaceListingType).map((type) => ({
                                        value: type,
                                        label: MarketplaceListingTypeLabel[type],
                                    }))}
                                />
                            )}
                        />

                        <Controller
                            control={control}
                            name="category"
                            rules={{ required: "Category is required" }}
                            render={({ field }) => (
                                <Select
                                    label="Category"
                                    placeholder="Select Category"
                                    required
                                    value={field.value}
                                    error={errors.category?.message}
                                    disabled={isSubmitting}
                                    onChange={field.onChange}
                                    options={Object.values(MarketplaceCategory).map((category) => ({
                                        value: category,
                                        label: MarketplaceCategoryLabel[category],
                                    }))}
                                />
                            )}
                        />
                    </div>

                    <Input
                        label="Price (Rs.)"
                        type="number"
                        min={0}
                        placeholder="Leave blank for &quot;Contact for price&quot;"
                        error={errors.price?.message}
                        disabled={isSubmitting}
                        {...register("price", {
                            validate: (value) =>
                                value.trim() === "" || Number(value) >= 0 || "Price can't be negative",
                        })}
                    />

                    <Textarea
                        label="Description"
                        placeholder="Condition, why you're selling/looking for it, any other details..."
                        required
                        rows={3}
                        error={errors.description?.message}
                        disabled={isSubmitting}
                        {...register("description", {
                            required: "Description is required",
                            minLength: { value: 10, message: "Description must be at least 10 characters" },
                            maxLength: { value: 1000, message: "Description must be less than 1000 characters" },
                        })}
                    />

                    <div className="space-y-4 rounded-lg border border-border bg-background-secondary p-4">
                        <label className="flex items-center gap-2 text-sm font-medium text-foreground">
                            <input
                                type="checkbox"
                                className="size-4 rounded border-border accent-accent"
                                disabled={isSubmitting}
                                {...register("linkToSubject")}
                            />
                            Link to a subject (optional)
                        </label>

                        {linkToSubject && (
                            <>
                                <Controller
                                    control={control}
                                    name="programId"
                                    render={({ field }) => (
                                        <Select
                                            label="Program"
                                            placeholder="Select Program"
                                            value={field.value}
                                            disabled={isSubmitting || programsPending || !programs}
                                            onChange={(e) => {
                                                field.onChange(e);
                                                setValue("semester", "");
                                                setValue("offeringId", "");
                                            }}
                                            options={(programs ?? []).map((prog) => ({
                                                value: String(prog.id),
                                                label: `${prog.code} - ${prog.name}`,
                                            }))}
                                        />
                                    )}
                                />

                                <Controller
                                    control={control}
                                    name="semester"
                                    render={({ field }) => (
                                        <Select
                                            label="Semester"
                                            placeholder="Select Semester"
                                            value={field.value}
                                            disabled={!selectedProgramId || isSubmitting}
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
                                            value={field.value}
                                            disabled={!bothSelected || subjectsFetching || isSubmitting}
                                            onChange={field.onChange}
                                            options={
                                                subjects?.map((offering) => ({
                                                    value: String(offering.id),
                                                    label: `${offering.subject.code} - ${offering.subject.name}`,
                                                })) ?? []
                                            }
                                        />
                                    )}
                                />
                            </>
                        )}
                    </div>
                </div>

                <div className="space-y-4">
                    <div
                        onDragOver={(e) => {
                            e.preventDefault();
                            if (!isSubmitting) setIsDragging(true);
                        }}
                        onDragLeave={() => setIsDragging(false)}
                        onDrop={handlePhotoDrop}
                        onClick={() => !isSubmitting && document.getElementById("listingPhotoInput")?.click()}
                        className={cn(
                            "rounded-lg border-2 border-dashed p-8 text-center transition-colors",
                            isSubmitting ? "cursor-not-allowed opacity-60" : "cursor-pointer hover:border-foreground-tertiary",
                            isDragging ? "border-accent bg-accent/5" : "border-border",
                        )}
                    >
                        <span className="mx-auto mb-4 flex size-12 items-center justify-center rounded-full bg-accent text-accent-foreground">
                            <CloudUpload className="size-6" />
                        </span>
                        <p className="font-semibold text-foreground">Drag & Drop photos here</p>
                        <p className="mt-1 text-sm text-foreground-secondary">or click to browse from your computer</p>
                        <p className="mt-4 inline-block rounded-md bg-background-tertiary px-3 py-1.5 font-display text-[11px] uppercase tracking-wide text-foreground-tertiary">
                            JPG, PNG, WEBP | up to 10 MB | max {MAX_LISTING_PHOTOS} photos
                        </p>
                        <input
                            id="listingPhotoInput"
                            type="file"
                            multiple
                            accept={ACCEPTED_LISTING_PHOTO_EXTENSIONS}
                            onChange={handlePhotoSelect}
                            disabled={isSubmitting}
                            className="hidden"
                        />
                    </div>
                    {errors.photos && <p className="text-xs text-error">{errors.photos.message}</p>}

                    {photos.length > 0 ? (
                        <div className="rounded-lg border border-border p-4">
                            <div className="mb-3 flex items-center justify-between gap-4">
                                <p className="font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                                    Photos ({photos.length})
                                </p>
                                <button
                                    type="button"
                                    onClick={() => setValue("photos", [], { shouldValidate: true })}
                                    disabled={isSubmitting}
                                    className="text-xs font-medium text-error hover:underline disabled:cursor-not-allowed disabled:opacity-60"
                                >
                                    Clear All
                                </button>
                            </div>
                            <div className="flex flex-col gap-2">
                                {photos.map((file, index) => (
                                    <PhotoQueueRow
                                        key={`${file.name}-${file.size}-${index}`}
                                        file={file}
                                        onRemove={() => removePhoto(index)}
                                    />
                                ))}
                            </div>
                        </div>
                    ) : (
                        <div className="flex items-center gap-2 rounded-lg border border-border p-4 text-sm text-foreground-tertiary">
                            <ImageIcon className="size-4 shrink-0" />
                            At least one photo is required.
                        </div>
                    )}
                </div>
            </div>

            <div className="flex flex-col gap-4 border-t border-border pt-6 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-sm leading-relaxed text-foreground-secondary sm:max-w-md">
                    You&apos;re responsible for what you post here. Listings that are misleading,
                    inappropriate, or prohibited will be removed.
                </p>
                <Button
                    type="submit"
                    icon={<Send className="size-4" />}
                    disabled={isSubmitting}
                    className="shrink-0"
                >
                    {isSubmitting ? "Posting..." : "Post Listing"}
                </Button>
            </div>
        </form>
    );
};
