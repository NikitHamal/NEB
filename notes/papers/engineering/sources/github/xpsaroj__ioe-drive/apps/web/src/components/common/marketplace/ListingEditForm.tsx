"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useForm, Controller, useWatch } from "react-hook-form";
import { toast } from "sonner";

import Select from "@/components/ui/Select";
import Input from "@/components/ui/Input";
import Textarea from "@/components/ui/Textarea";
import Button from "@/components/ui/Button";
import Loader from "@/components/ui/Loader";
import { usePrograms, useSubjectsForUpload, useSubjectDetails } from "@/hooks/queries/use-academics";
import { useUpdateListing } from "@/hooks/queries/use-marketplace";
import { getErrorMessage } from "@/lib/errors";
import {
    Semester,
    SemesterLabel,
    MarketplaceListingType,
    MarketplaceListingTypeLabel,
    MarketplaceCategory,
    MarketplaceCategoryLabel,
} from "@/types/entities";
import type { ListingSummary } from "@/types/api";

interface ListingEditFormProps {
    listing: ListingSummary;
    /** Rendered beside Listing Details - a slot since photo add/remove isn't part of this form's submission. */
    photosPanel?: React.ReactNode;
}

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
};

// Prefills Program/Semester via useSubjectDetails, since ListingSummary itself doesn't carry them.
export const ListingEditForm = ({ listing, photosPanel }: ListingEditFormProps) => {
    const router = useRouter();

    const { data: offeringDetails, isPending: offeringPending } = useSubjectDetails(listing.offeringId ?? 0);
    const { data: programs, isPending: programsPending } = usePrograms();
    const { mutate, isPending: isSaving } = useUpdateListing(listing.id);

    const {
        handleSubmit,
        control,
        register,
        setValue,
        reset,
        formState: { errors },
    } = useForm<FormValues>({
        defaultValues: {
            title: listing.title,
            description: listing.description,
            type: listing.type,
            category: listing.category,
            price: listing.price != null ? String(listing.price) : "",
            linkToSubject: !!listing.offeringId,
            programId: "",
            semester: "",
            offeringId: listing.offeringId ? String(listing.offeringId) : "",
        },
    });

    // Cascading selects start empty until the current offering's details load.
    useEffect(() => {
        if (!offeringDetails) return;

        reset({
            title: listing.title,
            description: listing.description,
            type: listing.type,
            category: listing.category,
            price: listing.price != null ? String(listing.price) : "",
            linkToSubject: true,
            programId: String(offeringDetails.programId),
            semester: offeringDetails.semester,
            offeringId: String(listing.offeringId),
        });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [offeringDetails]);

    const linkToSubject = useWatch({ control, name: "linkToSubject" });
    const selectedProgramId = useWatch({ control, name: "programId" });
    const selectedSemester = useWatch({ control, name: "semester" });

    const { data: subjects, isFetching: subjectsFetching } = useSubjectsForUpload(
        selectedProgramId ? Number(selectedProgramId) : undefined,
        selectedSemester || undefined,
    );

    const bothSelected = !!(selectedProgramId && selectedSemester);

    const onSubmit = (data: FormValues) => {
        mutate(
            {
                title: data.title,
                description: data.description,
                type: data.type as MarketplaceListingType,
                category: data.category as MarketplaceCategory,
                price: data.price.trim() ? Number(data.price) : undefined,
                offeringId: data.linkToSubject && data.offeringId ? Number(data.offeringId) : undefined,
            },
            {
                onSuccess: () => {
                    toast.success("Listing updated successfully.");
                    router.back();
                },
                onError: (error) => {
                    toast.error(getErrorMessage(error, "Couldn't update the listing. Please try again."));
                },
            }
        );
    };

    const isLoadingInitialData = (!!listing.offeringId && offeringPending) || programsPending || !programs;

    if (isLoadingInitialData) {
        return <Loader text="Loading listing details..." />;
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6" noValidate>
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 lg:items-start">
                <div className="space-y-4 rounded-lg md:border border-border md:p-6">
                    <h2 className="text-lg font-semibold text-foreground">Listing Details</h2>

                    <Input
                        label="Title"
                        required
                        error={errors.title?.message}
                        disabled={isSaving}
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
                                    required
                                    value={field.value}
                                    error={errors.type?.message}
                                    disabled={isSaving}
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
                                    required
                                    value={field.value}
                                    error={errors.category?.message}
                                    disabled={isSaving}
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
                        disabled={isSaving}
                        {...register("price", {
                            validate: (value) =>
                                value.trim() === "" || Number(value) >= 0 || "Price can't be negative",
                        })}
                    />

                    <Textarea
                        label="Description"
                        required
                        rows={3}
                        error={errors.description?.message}
                        disabled={isSaving}
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
                                disabled={isSaving}
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
                                            disabled={isSaving}
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
                                    render={({ field }) => (
                                        <Select
                                            label="Semester"
                                            placeholder="Select Semester"
                                            value={field.value}
                                            disabled={!selectedProgramId || isSaving}
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
                                            disabled={!bothSelected || subjectsFetching || isSaving}
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

                {photosPanel}
            </div>

            <div className="flex justify-end gap-3 border-t border-border pt-6">
                <Button type="button" variant="secondary" onClick={() => router.back()} disabled={isSaving}>
                    Cancel
                </Button>
                <Button type="submit" disabled={isSaving}>
                    {isSaving ? "Saving..." : "Save Changes"}
                </Button>
            </div>
        </form>
    );
};
