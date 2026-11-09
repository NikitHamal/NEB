import type { Metadata } from "next";
import Link from "next/link";
import { Github, MessageCircle } from "lucide-react";

import Button from "@/components/ui/Button";
import { DISCORD_CONTACTS } from "@/lib/site";

export const metadata: Metadata = {
    title: "Contact",
    description: "Get in touch with the students building and maintaining IOE Drive.",
};

const ContactPage = () => (
    <div className="container mx-auto max-w-5xl px-6 py-16 md:py-20">
        <div className="max-w-2xl">
            <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">Contact & Support</h1>
            <p className="mt-4 text-foreground-secondary">
                IOE Drive is built and maintained by a small group of student developers, not a
                support department - so reach out directly and a real person will get back to
                you.
            </p>
        </div>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-5 gap-6">
            <div className="md:col-span-3 flex flex-col rounded-lg border border-border bg-accent-soft p-8">
                <div className="size-12 rounded-md bg-accent flex items-center justify-center mb-4">
                    <MessageCircle className="size-6 text-accent-foreground" />
                </div>
                <h2 className="text-xl font-semibold text-foreground">Talk to us on Discord</h2>
                <p className="mt-2 text-sm text-foreground-secondary flex-1">
                    The fastest way to reach the team - DM either of us directly to ask questions,
                    report something broken, or just say hi.
                </p>
                <div className="mt-6 flex flex-wrap gap-2">
                    {DISCORD_CONTACTS.map((contact) => (
                        <Button key={contact.href} href={contact.href} variant="primary" size="sm">
                            Message {contact.username}
                        </Button>
                    ))}
                </div>
            </div>

            <div className="md:col-span-2 flex flex-col rounded-lg border border-border p-8">
                <div className="size-10 rounded-md bg-accent-soft flex items-center justify-center mb-4">
                    <Github className="size-5 text-accent" />
                </div>
                <h2 className="text-xl font-semibold text-foreground">Find us on GitHub</h2>
                <p className="mt-2 text-sm text-foreground-secondary flex-1">
                    IOE Drive is fully open source - browse an issue if something&apos;s broken, or
                    send a pull request if you&apos;d like to help build it.
                </p>
                <div className="mt-6 flex flex-col gap-2">
                    <Button href="https://github.com/xpsaroj/ioe-drive/issues" variant="secondary" size="sm">
                        Open an issue
                    </Button>
                    <Button href="https://github.com/xpsaroj/ioe-drive/" variant="secondary" size="sm">
                        View the repo
                    </Button>
                </div>
            </div>
        </div>

        <p className="mt-10 text-sm text-foreground-secondary">
            Have a question about your data, or a privacy request? The same Discord and GitHub
            channels above reach us fastest - see our{" "}
            <Link href="/privacy" className="text-accent hover:text-accent-hover underline underline-offset-2">
                Privacy Policy
            </Link>{" "}
            for details.
        </p>
    </div>
);

export default ContactPage;
