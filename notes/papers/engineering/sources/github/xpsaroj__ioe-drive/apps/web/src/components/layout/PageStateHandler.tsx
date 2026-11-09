"use client";
import { AlertCircle, Inbox } from "lucide-react";

import { getErrorMessage } from "@/lib/errors";
import Loader from "@/components/ui/Loader";

interface PageStateHandlerProps {
    isPending: boolean;
    error: Error | null | undefined;
    isEmpty: boolean;
    loaderText?: string;
    errorContent?: React.ReactNode;
    emptyContent?: React.ReactNode;
    children: React.ReactNode;
    containerClassName?: string;
    stateContainerClassName?: string;
    /** Rendered at the top of the page in every state - usually a title and back button. */
    header?: React.ReactNode;
}

const PageStateHandler = ({
    isPending,
    error,
    isEmpty,
    loaderText = "Loading. Please wait.",
    errorContent,
    emptyContent,
    children,
    header,
    containerClassName = "min-h-screen flex flex-col bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto",
    stateContainerClassName = "flex-1 flex items-center justify-center border rounded-lg",
}: PageStateHandlerProps) => {
    if (isPending) {
        return (
            <div className={containerClassName}>
                {header}
                <div className={stateContainerClassName}>
                    <Loader text={loaderText} />
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className={containerClassName}>
                {header}
                <div className={stateContainerClassName}>
                    {errorContent || (
                        <div className="flex flex-col items-center gap-2">
                            <AlertCircle className="size-5 text-error" />
                            <p className="text-sm text-error">
                                {getErrorMessage(error, "Something went wrong. Please try again later.")}
                            </p>
                        </div>
                    )}
                </div>
            </div>
        );
    }

    if (isEmpty) {
        return (
            <div className={containerClassName}>
                {header}
                <div className={stateContainerClassName}>
                    {emptyContent || (
                        <div className="flex flex-col items-center gap-3">
                            <Inbox className="size-6 text-foreground-tertiary" />
                            <p className="text-foreground-secondary">No data found.</p>
                        </div>
                    )}
                </div>
            </div>
        );
    }

    return (
        <div className={containerClassName}>
            {header}
            {children}
        </div>
    );
};

export default PageStateHandler;
