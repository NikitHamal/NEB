import { ClerkLoaded, ClerkLoading, ClerkFailed } from "@clerk/nextjs"

export default function GlobalLoader({
    children
}: {
    children: React.ReactNode
}) {
    return (
        <>
            <ClerkLoading>
                <div className="fixed inset-0 flex items-center justify-center bg-background z-9999">
                    <div className="animate-spin rounded-full h-12 w-12 border-4 border-foreground-secondary border-t-foreground"></div>
                </div>
            </ClerkLoading>

            <ClerkFailed>
                <div className="fixed inset-0 flex items-center justify-center bg-background z-50">
                    <div className="text-error">Something went wrong. Please refresh the page.</div>
                </div>
            </ClerkFailed>

            <ClerkLoaded>
                {children}
            </ClerkLoaded>
        </>
    )
}