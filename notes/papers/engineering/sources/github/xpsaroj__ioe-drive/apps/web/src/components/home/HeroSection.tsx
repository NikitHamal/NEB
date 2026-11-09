"use client"
import { useAuth } from "@clerk/nextjs";
import Button from "@/components/ui/Button";

export default function HeroSection() {

    const { isSignedIn } = useAuth();

    return (
        <section className="bg-background-secondary border-b border-border">
            <div className="container mx-auto px-6 py-20 text-center">
                <p className="font-display text-xs sm:text-sm tracking-[0.2em] uppercase text-accent font-medium mb-4">
                    For IOE students, by IOE students
                </p>

                <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-foreground mb-5 text-balance">
                    The shared library for every IOE program
                </h1>

                <p className="text-lg text-foreground-secondary max-w-2xl mx-auto mb-10 text-balance">
                    Notes, past questions, and lab sheets, organized by program, semester, and
                    subject. Browse freely, or sign in to upload your own and build your library.
                </p>

                <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
                    <Button
                        variant="primary"
                        size="lg"
                        className="w-full sm:w-auto"
                        href="/resources"
                    >
                        Browse Resources
                    </Button>

                    <Button
                        variant="secondary"
                        size="lg"
                        className="w-full sm:w-auto"
                        href={isSignedIn ? "/dashboard" : "/sign-in"}
                    >
                        {isSignedIn ? "Continue to Dashboard" : "Sign in"}
                    </Button>
                </div>
            </div>
        </section>
    );
}
