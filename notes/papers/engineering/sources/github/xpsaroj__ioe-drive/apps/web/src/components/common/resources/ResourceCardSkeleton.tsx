const ResourceCardSkeleton = () => {
    return (
        <div className="flex animate-pulse flex-col gap-4 rounded-lg border border-border p-4 sm:p-5">
            <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-2">
                    <div className="h-5 w-40 rounded bg-background-tertiary" />
                    <div className="h-5 w-14 rounded-md bg-background-tertiary" />
                </div>
                <div className="h-7 w-16 rounded-lg bg-background-tertiary" />
            </div>

            <div className="flex flex-col gap-2">
                <div className="h-3 w-full rounded bg-background-tertiary" />
                <div className="h-3 w-2/3 rounded bg-background-tertiary" />
            </div>

            <div className="flex flex-row gap-2">
                <div className="h-11 w-40 rounded-lg bg-background-tertiary" />
                <div className="h-11 w-40 rounded-lg bg-background-tertiary" />
            </div>

            <div className="flex items-center justify-between gap-3 pt-3 border-t border-border">
                <div className="flex items-center gap-2">
                    <div className="size-8 rounded-full bg-background-tertiary" />
                    <div className="flex flex-col gap-1">
                        <div className="h-3 w-20 rounded bg-background-tertiary" />
                        <div className="h-2 w-14 rounded bg-background-tertiary" />
                    </div>
                </div>
                <div className="h-6 w-24 rounded-lg bg-background-tertiary" />
            </div>
        </div>
    );
}

export default ResourceCardSkeleton;
