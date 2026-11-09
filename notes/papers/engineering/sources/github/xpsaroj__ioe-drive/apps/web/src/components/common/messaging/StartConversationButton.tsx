"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { MessageCircle } from "lucide-react";

import Modal from "@/components/ui/Modal";
import Textarea from "@/components/ui/Textarea";
import Button from "@/components/ui/Button";
import { useStartConversation } from "@/hooks/queries/use-messaging";
import { getErrorMessage } from "@/lib/errors";

interface StartConversationButtonProps {
    listingId: number;
    /** "Message Seller" for a SELLING listing, "Message" for a WANTED one (matches the poster's role). */
    label?: string;
}

const StartConversationButton = ({ listingId, label = "Message Seller" }: StartConversationButtonProps) => {
    const router = useRouter();
    const [isOpen, setIsOpen] = useState(false);
    const [message, setMessage] = useState("");
    const { mutate, isPending } = useStartConversation();

    const handleClose = () => {
        setIsOpen(false);
        setMessage("");
    };

    const handleSend = () => {
        if (!message.trim()) return;

        mutate(
            { listingId, message: message.trim() },
            {
                onSuccess: (data) => {
                    handleClose();
                    router.push(`/messages/${data.conversationId}`);
                },
                onError: (error) => {
                    toast.error(getErrorMessage(error, "Couldn't send your message. Please try again."));
                },
            }
        );
    };

    return (
        <>
            <Button icon={<MessageCircle className="size-4" />} onClick={() => setIsOpen(true)} className="w-full">
                {label}
            </Button>

            <Modal isOpen={isOpen} onClose={handleClose} title={label} size="sm">
                <div className="flex flex-col gap-4">
                    <Textarea
                        label="Your message"
                        placeholder="Hi, is this still available?"
                        rows={4}
                        maxLength={2000}
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        disabled={isPending}
                    />
                    <div className="flex justify-end gap-3">
                        <Button variant="secondary" onClick={handleClose} disabled={isPending}>
                            Cancel
                        </Button>
                        <Button onClick={handleSend} disabled={isPending || !message.trim()}>
                            {isPending ? "Sending..." : "Send"}
                        </Button>
                    </div>
                </div>
            </Modal>
        </>
    );
};

export default StartConversationButton;
