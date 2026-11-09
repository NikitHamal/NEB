"use client";
import { useForm, Controller } from "react-hook-form";

import Modal from "@/components/ui/Modal";
import Select from "@/components/ui/Select";
import Textarea from "@/components/ui/Textarea";
import Button from "@/components/ui/Button";

interface ModerationActionModalProps {
    isOpen: boolean;
    onClose: () => void;
    title: string;
    description?: string;
    submitLabel: string;
    isSubmitting: boolean;
    /** The caller's own reason enum, as {value, label} pairs - resources and marketplace listings each have their own. */
    reasonOptions: { value: string; label: string }[];
    onSubmit: (data: { reason: string; note?: string }) => void;
}

interface FormValues {
    reason: string;
    note: string;
}

// Shared by moderator reject/remove and visitor report (both resources and marketplace listings) - same { reason, note? } shape.
const ModerationActionModal = ({
    isOpen,
    onClose,
    title,
    description,
    submitLabel,
    isSubmitting,
    reasonOptions,
    onSubmit,
}: ModerationActionModalProps) => {
    const {
        handleSubmit,
        control,
        register,
        reset,
        formState: { errors },
    } = useForm<FormValues>({ defaultValues: { reason: "", note: "" } });

    const handleClose = () => {
        reset();
        onClose();
    };

    const submit = (data: FormValues) => {
        onSubmit({ reason: data.reason, note: data.note.trim() || undefined });
    };

    return (
        <Modal isOpen={isOpen} onClose={handleClose} title={title}>
            <form onSubmit={handleSubmit(submit)} className="space-y-4" noValidate>
                {description && <p className="text-sm text-foreground-secondary">{description}</p>}

                <Controller
                    control={control}
                    name="reason"
                    rules={{ required: "A reason is required" }}
                    render={({ field }) => (
                        <Select
                            label="Reason"
                            placeholder="Select a reason"
                            required
                            value={field.value}
                            error={errors.reason?.message}
                            disabled={isSubmitting}
                            onChange={field.onChange}
                            options={reasonOptions}
                        />
                    )}
                />

                <Textarea
                    label="Additional details"
                    placeholder="Optional context (not required)"
                    rows={3}
                    disabled={isSubmitting}
                    error={errors.note?.message}
                    {...register("note", {
                        maxLength: { value: 1000, message: "Must be at most 1000 characters" },
                    })}
                />

                <div className="flex justify-end gap-3 pt-2">
                    <Button type="button" variant="secondary" onClick={handleClose} disabled={isSubmitting}>
                        Cancel
                    </Button>
                    <Button type="submit" disabled={isSubmitting}>
                        {isSubmitting ? "Submitting..." : submitLabel}
                    </Button>
                </div>
            </form>
        </Modal>
    );
};

export default ModerationActionModal;
