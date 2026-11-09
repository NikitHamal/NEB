import { SignUp } from '@clerk/nextjs'
import { UserPlus } from 'lucide-react'

import { Loader } from '@/components/ui/Loader'
import { AuthBrandPanel } from '@/components/auth'

interface SignUpPageProps {
    // Set by Clerk itself (via auth.protect() in proxy.ts, or by the SignIn widget's own
    // "sign up instead" link) when the user is here to get back to a specific page.
    searchParams: Promise<{ redirect_url?: string }>;
}

export default async function SignUpPage({ searchParams }: SignUpPageProps) {
    const { redirect_url: redirectUrl } = await searchParams;

    return (
        <main className="grid lg:grid-cols-2 min-h-[calc(100vh-4.5rem)] bg-background">
            <AuthBrandPanel variant="sign-up" />

            <div className="flex flex-col justify-center items-center p-6 sm:p-10">
                {redirectUrl && (
                    <div className="mb-4 flex items-center gap-2 rounded-full bg-accent-soft px-4 py-2 text-sm font-semibold text-accent">
                        <UserPlus className="size-4 shrink-0" />
                        Create an account to continue
                    </div>
                )}
                <SignUp
                    path="/sign-up"
                    routing="path"
                    signInUrl="/sign-in"
                    appearance={{
                        elements: {
                            card: "shadow-lg/30",
                        },
                        layout: {
                            socialButtonsPlacement: "bottom",
                        },
                    }}
                    fallback={<SignUpFallback />}
                />
            </div>
        </main>
    );
}

const SignUpFallback = () => {
    return (
        <div className="w-full max-w-md min-h-[calc(100vh-13rem)] flex items-center justify-center">
            <Loader />
        </div>
    );
};