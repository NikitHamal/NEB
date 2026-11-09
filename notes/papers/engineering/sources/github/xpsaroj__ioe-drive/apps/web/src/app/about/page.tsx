import type { Metadata } from "next";
import Image from "next/image";
import { Github, GraduationCap, NotebookPen, ShieldCheck, Heart, Code2, Server, Database, Cloud, Users } from "lucide-react";

import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import FeatureList from "@/components/ui/FeatureList";
import { ScatteredCodeTiles, type ScatteredTile } from "@/components/decor";

export const metadata: Metadata = {
    title: "About",
    description: "Why IOE Drive exists, what it does, and who's building it.",
};

// Kept clear of the centered hero text.
const HERO_TILES: ScatteredTile[] = [
    { code: "BCT", top: "12%", left: "6%", rotate: -6, size: "size-11 text-xs", solid: true, float: true },
    { code: "BEX", top: "78%", left: "10%", rotate: 4, size: "size-10 text-xs", float: true },
    { code: "BEE", top: "16%", left: "88%", rotate: 5, size: "size-10 text-xs", float: true },
    { code: "BCE", top: "76%", left: "86%", rotate: -4, size: "size-11 text-xs", solid: true, float: true },
    { code: "BME", top: "46%", left: "3%", rotate: 7, size: "size-9 text-[10px]", float: true },
    { code: "BAR", top: "44%", left: "94%", rotate: 3, size: "size-9 text-[10px]", float: true },
];

const HOW_IT_WORKS = [
    {
        icon: GraduationCap,
        title: "Pick your program & semester",
        description: "The curriculum is organized exactly the way IOE teaches it - by program, year, and semester, not a flat file dump.",
    },
    {
        icon: NotebookPen,
        title: "Browse, download, or share",
        description: "Notes, past questions, assessments, lab sheets, and books, all searchable by subject.",
    },
    {
        icon: Heart,
        title: "Give back when you can",
        description: "Sign in to upload your own notes and past questions, so the next batch has it a little easier too.",
    },
];

const TECH_STACK = [
    { name: "Next.js", icon: Code2 },
    { name: "NestJS", icon: Server },
    { name: "PostgreSQL", icon: Database },
    { name: "Clerk", icon: ShieldCheck },
    { name: "Azure Blob Storage", icon: Cloud },
];

const AboutPage = () => (
    <div>
        <section className="relative overflow-hidden bg-background-secondary border-b border-border">
            <ScatteredCodeTiles tiles={HERO_TILES} />
            <div className="container relative z-10 mx-auto px-6 py-20 text-center">
                <p className="font-display text-xs sm:text-sm tracking-[0.2em] uppercase text-accent font-medium mb-4">
                    Open source &middot; Student-run
                </p>
                <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-foreground mb-5 text-balance">
                    A shared library, built by the students who use it
                </h1>
                <p className="text-lg text-foreground-secondary max-w-2xl mx-auto mb-10 text-balance">
                    IOE Drive is a free platform for Institute of Engineering (IOE), Tribhuvan
                    University students to find and share notes, past questions, and study
                    materials - organized the way the curriculum actually works, not scattered
                    across group chats.
                </p>
                <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
                    <Button variant="primary" size="lg" className="w-full sm:w-auto" href="/resources">
                        Browse Resources
                    </Button>
                    <Button
                        variant="secondary"
                        size="lg"
                        className="w-full sm:w-auto"
                        href="https://github.com/xpsaroj/ioe-drive/"
                        icon={<Github className="size-4" />}
                    >
                        View on GitHub
                    </Button>
                </div>
            </div>
        </section>

        <section className="container max-w-6xl mx-auto px-6 py-20">
            <div className="flex flex-col gap-10 lg:flex-row lg:items-center lg:gap-16">
                <div className="max-w-2xl flex-1">
                    <h2 className="text-3xl font-bold text-foreground mb-4">Why we built this</h2>
                    <p className="text-foreground-secondary leading-relaxed mb-4">
                        Notes and past questions used to live scattered across different platforms.
                    </p>
                    <p className="text-foreground-secondary leading-relaxed">
                        Every program had its own scattered pile, nothing organized and nothing
                        easy to find once a batch moved on. IOE Drive started as a small project
                        among friends to fix that, one place for every program, organized by
                        IOE&apos;s actual curriculum, that any student can browse for free and
                        contribute back to. It&apos;s not an official IOE or Tribhuvan University
                        service, just students building the tool we wished we&apos;d had.
                    </p>
                </div>

                <div className="flex-1">
                    <div className="overflow-hidden rounded-lg border border-border shadow-lg">
                        <div className="flex items-center gap-1.5 border-b border-border bg-background-secondary px-3 py-2">
                            <span className="size-2.5 rounded-full bg-foreground/15" />
                            <span className="size-2.5 rounded-full bg-foreground/15" />
                            <span className="size-2.5 rounded-full bg-foreground/15" />
                            <span className="ml-2 truncate rounded-md bg-background px-2 py-0.5 text-[11px] text-foreground-tertiary">
                                ioedrive.vercel.app/resources
                            </span>
                        </div>
                        <Image
                            src="/images/about/resources-preview.png"
                            alt="The IOE Drive resource browser, showing program/semester/subject filters and a shared resource"
                            width={1920}
                            height={1080}
                            className="h-auto w-full"
                        />
                    </div>
                </div>
            </div>
        </section>

        <section className="bg-background-secondary border-y border-border py-20">
            <div className="container mx-auto px-6">
                <h2 className="text-3xl font-bold text-foreground text-center mb-12">How it works</h2>
            </div>
            <div className="container max-w-4xl mx-auto px-6">
                <FeatureList items={HOW_IT_WORKS} />
            </div>
        </section>

        <section className="container max-w-6xl mx-auto px-6 py-20">
            <div className="max-w-2xl">
                <h2 className="text-3xl font-bold text-foreground mb-4">Built in the open</h2>
                <p className="text-foreground-secondary leading-relaxed mb-6">
                    The entire codebase is public and MIT-licensed - anyone can read it, run it
                    locally, or send a pull request. It&apos;s maintained by me and my friends, in
                    the open, on GitHub and Discord.
                </p>
                <div className="flex flex-wrap gap-2 mb-8">
                    {TECH_STACK.map(({ name, icon: Icon }) => (
                        <Badge key={name} variant="secondary" icon={<Icon className="size-3.5" />}>
                            {name}
                        </Badge>
                    ))}
                </div>
                <div className="flex flex-wrap gap-4">
                    <Button
                        variant="secondary"
                        href="https://github.com/xpsaroj/ioe-drive/"
                        icon={<Github className="size-4" />}
                    >
                        Star on GitHub
                    </Button>
                    <Button variant="ghost" href="/contact" icon={<Users className="size-4" />}>
                        Get in touch
                    </Button>
                </div>
            </div>
        </section>

        <section className="bg-accent-soft border-t border-border py-16">
            <div className="container mx-auto px-6 text-center">
                <h2 className="text-3xl font-bold text-foreground mb-4">Ready to find your notes?</h2>
                <p className="text-foreground-secondary leading-relaxed mb-8 max-w-xl mx-auto">
                    Browse without an account, or sign in to upload your own and build your
                    library.
                </p>
                <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
                    <Button variant="primary" size="lg" className="w-full sm:w-auto" href="/resources">
                        Browse Resources
                    </Button>
                    <Button variant="secondary" size="lg" className="w-full sm:w-auto" href="/sign-up">
                        Sign up
                    </Button>
                </div>
            </div>
        </section>
    </div>
);

export default AboutPage;
