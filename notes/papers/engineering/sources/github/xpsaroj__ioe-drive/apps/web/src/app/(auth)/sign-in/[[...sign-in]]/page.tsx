import { SignIn } from '@clerk/nextjs'
import { LogIn } from 'lucide-react'

import { Loader } from '@/components/ui/Loader'
import { AuthBrandPanel } from '@/components/auth'

interface SignInPageProps {
    // Set by Clerk itself (via auth.protect() in proxy.ts) when redirecting a signed-out
    // user away from a protected page - absent when the user navigated here directly.
    searchParams: Promise<{ redirect_url?: string }>;
}

export default async function SignInPage({ searchParams }: SignInPageProps) {
    const { redirect_url: redirectUrl } = await searchParams;

    return (
        <main className="grid lg:grid-cols-2 min-h-[calc(100vh-4.5rem)] bg-background">
            <AuthBrandPanel variant="sign-in" />

            <div className="flex flex-col justify-center items-center p-6 sm:p-10">
                {redirectUrl && (
                    <div className="mb-4 flex items-center gap-2 rounded-full bg-accent-soft px-4 py-2 text-sm font-semibold text-accent">
                        <LogIn className="size-4 shrink-0" />
                        Sign in to continue
                    </div>
                )}
                <SignIn
                    path="/sign-in"
                    routing="path"
                    signUpUrl="/sign-up"
                    appearance={{
                        elements: {
                            card: "shadow-lg/30",
                        },
                        layout: {
                            socialButtonsPlacement: "bottom",
                        },
                    }}
                    fallback={<SignInFallback />}
                />
            </div>
        </main>
    );
}

const SignInFallback = () => {
    return (
        <div className="w-full max-w-md min-h-[calc(100vh-13rem)] flex items-center justify-center">
            <Loader />
        </div>
    );
};