"use client";
import { useState } from "react";
import { Trash2 } from "lucide-react";
import { toast } from "sonner";

import Button from "@/components/ui/Button";
import Modal from "@/components/ui/Modal";
import { useDeleteResource } from "@/hooks/queries/use-resources";
import { getErrorMessage } from "@/lib/errors";

interface DeleteResourceButtonProps {
    resourceId: number;
    /** Called after a successful deletion, e.g. to redirect away from a now-empty page. */
    onDeleted?: () => void;
}

const DeleteResourceButton = ({ resourceId, onDeleted }: DeleteResourceButtonProps) => {
    const [isConfirmOpen, setIsConfirmOpen] = useState(false);
    const { mutate, isPending } = useDeleteResource();

    const handleConfirm = () => {
        mutate(resourceId, {
            onSuccess: () => {
                toast.success("Resource deleted successfully.");
                setIsConfirmOpen(false);
                onDeleted?.();
            },
            onError: (error) => {
                toast.error(getErrorMessage(error, "Couldn't delete the resource. Please try again."));
            },
        });
    };

    return (
        <>
            <Button
                variant="ghost"
                size="xs"
                iconOnly
                icon={<Trash2 className="size-4" />}
                onClick={() => setIsConfirmOpen(true)}
                className="text-error/80 hover:text-error hover:bg-error/10"
                aria-label="Delete resource"
            />

            {isConfirmOpen && (
                <Modal
                    isOpen={isConfirmOpen}
                    onClose={() => setIsConfirmOpen(false)}
                    title="Delete Resource"
                    size="sm"
                >
                    <div className="flex flex-col gap-4">
                        <p className="text-sm text-foreground-secondary">
                            Are you sure you want to delete this resource? This will also remove all
                            of its attached files. This action cannot be undone.
                        </p>
                        <div className="flex justify-end gap-3">
                            <Button
                                variant="secondary"
                                onClick={() => setIsConfirmOpen(false)}
                                disabled={isPending}
                            >
                                Cancel
                            </Button>
                            <Button
                                variant="destructive"
                                onClick={handleConfirm}
                                disabled={isPending}
                            >
                                {isPending ? "Deleting..." : "Delete"}
                            </Button>
                        </div>
                    </div>
                </Modal>
            )}
        </>
    );
};

export default DeleteResourceButton;
