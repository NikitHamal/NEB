"use client";
import { useState } from "react";
import { Trash2 } from "lucide-react";
import { toast } from "sonner";

import Button from "@/components/ui/Button";
import Modal from "@/components/ui/Modal";
import { useDeleteListing } from "@/hooks/queries/use-marketplace";
import { getErrorMessage } from "@/lib/errors";

interface DeleteListingButtonProps {
    listingId: number;
    /** Called after a successful deletion, e.g. to redirect away from a now-empty page. */
    onDeleted?: () => void;
}

const DeleteListingButton = ({ listingId, onDeleted }: DeleteListingButtonProps) => {
    const [isConfirmOpen, setIsConfirmOpen] = useState(false);
    const { mutate, isPending } = useDeleteListing();

    const handleConfirm = () => {
        mutate(listingId, {
            onSuccess: () => {
                toast.success("Listing deleted successfully.");
                setIsConfirmOpen(false);
                onDeleted?.();
            },
            onError: (error) => {
                toast.error(getErrorMessage(error, "Couldn't delete the listing. Please try again."));
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
                aria-label="Delete listing"
            />

            {isConfirmOpen && (
                <Modal
                    isOpen={isConfirmOpen}
                    onClose={() => setIsConfirmOpen(false)}
                    title="Delete Listing"
                    size="sm"
                >
                    <div className="flex flex-col gap-4">
                        <p className="text-sm text-foreground-secondary">
                            Are you sure you want to delete this listing? This will also remove all
                            of its photos. This action cannot be undone.
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

export default DeleteListingButton;
