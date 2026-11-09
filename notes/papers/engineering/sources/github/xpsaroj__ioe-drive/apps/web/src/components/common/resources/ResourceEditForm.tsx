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
import { useUpdateResource } from "@/hooks/queries/use-resources";
import { getErrorMessage } from "@/lib/errors";
import { Semester, SemesterLabel, ResourceType, ResourceTypeLabel } from "@/types/entities";
import type { ResourceSummary } from "@/types/api";

interface ResourceEditFormProps {
    resource: ResourceSummary;
    /** Rendered beside Resource Details - a slot since file/link add/remove isn't part of this form's submission. */
    contentPanel?: React.ReactNode;
}

type FormValues = {
    title: string;
    description: string;
    programId: string;
    type: ResourceType | "";
    semester: Semester | "";
    offeringId: string;
};

// Prefills Program/Semester/Subject via useSubjectDetails, since ResourceSummary itself doesn't carry them.
export const ResourceEditForm = ({ resource, contentPanel }: ResourceEditFormProps) => {
    const router = useRouter();

    const { data: offeringDetails, isPending: offeringPending } = useSubjectDetails(resource.offeringId);
    const { data: programs, isPending: programsPending } = usePrograms();
    const { mutate, isPending: isSaving } = useUpdateResource(resource.id);

    const {
        handleSubmit,
        control,
        register,
        setValue,
        reset,
        formState: { errors },
    } = useForm<FormValues>({
        defaultValues: {
            title: resource.title,
            description: resource.description,
            programId: "",
            type: resource.type,
            semester: "",
            offeringId: "",
        },
    });

    // Cascading selects start empty until the current offering's details load.
    useEffect(() => {
        if (!offeringDetails) return;

        reset({
            title: resource.title,
            description: resource.description,
            programId: String(offeringDetails.programId),
            type: resource.type,
            semester: offeringDetails.semester,
            offeringId: String(resource.offeringId),
        });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [offeringDetails]);

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
                type: data.type as ResourceType,
                offeringId: Number(data.offeringId),
            },
            {
                onSuccess: () => {
                    toast.success("Resource updated successfully.");
                    router.back();
                },
                onError: (error) => {
                    toast.error(getErrorMessage(error, "Couldn't update the resource. Please try again."));
                },
            }
        );
    };

    const isLoadingInitialData = offeringPending || programsPending || !programs;

    if (isLoadingInitialData) {
        return <Loader text="Loading resource details..." />;
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6" noValidate>
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 lg:items-start">
                <div className="space-y-4 rounded-lg md:border border-border md:p-6">
                    <h2 className="text-lg font-semibold text-foreground">Resource Details</h2>

                    <Input
                        label="Document Title"
                        required
                        error={errors.title?.message}
                        disabled={isSaving}
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
                                disabled={isSaving}
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
                        required
                        rows={3}
                        error={errors.description?.message}
                        disabled={isSaving}
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
                            rules={{ required: "Semester is required" }}
                            render={({ field }) => (
                                <Select
                                    label="Semester"
                                    placeholder="Select Semester"
                                    required
                                    value={field.value}
                                    error={errors.semester?.message}
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
                                    disabled={!bothSelected || subjectsFetching || isSaving}
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

                {contentPanel}
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
