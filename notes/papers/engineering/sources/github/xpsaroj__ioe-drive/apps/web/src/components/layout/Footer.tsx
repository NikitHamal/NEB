import Link from "next/link";
import { Github } from "lucide-react";

import Logo from "./Logo";
import WordmarkText from "./WordmarkText";
import { DISCORD_CONTACTS } from "@/lib/site";

interface FooterLink {
    name: string;
    href: string;
}

// Only public routes
const FOOTER_LINK_GROUPS: { title: string; links: FooterLink[] }[] = [
    {
        title: "Explore",
        links: [
            { name: "Browse Resources", href: "/resources" },
            { name: "Curriculum", href: "/offerings" },
            { name: "Programs", href: "/programs" },
            { name: "Marketplace", href: "/market" },
        ],
    },
    {
        title: "Account",
        links: [
            { name: "Sign In", href: "/sign-in" },
            { name: "Sign Up", href: "/sign-up" },
        ],
    },
    {
        title: "About",
        links: [
            { name: "About Us", href: "/about" },
            { name: "Contact", href: "/contact" },
            { name: "Privacy Policy", href: "/privacy" },
            { name: "Terms of Service", href: "/terms" },
        ],
    },
];

const FooterLinkGroup = ({ title, links }: { title: string; links: FooterLink[] }) => (
    <div>
        <p className="font-display text-xs font-semibold uppercase tracking-wide text-foreground-tertiary">
            {title}
        </p>
        <ul className="mt-3 space-y-2">
            {links.map((link) => (
                <li key={link.href}>
                    <Link href={link.href} className="text-sm text-foreground-secondary hover:text-foreground transition-colors">
                        {link.name}
                    </Link>
                </li>
            ))}
        </ul>
    </div>
);

export default function Footer() {
    return (
        <footer className="bg-background-secondary border-t border-border">
            <div className="container mx-auto px-6 py-10">
                <div className="flex flex-col gap-10 md:flex-row md:items-start md:justify-between">
                    <div className="flex shrink-0 flex-col items-center gap-3 text-center md:items-start md:text-left">
                        <Link href="/" className="flex items-center gap-2.5 shrink-0">
                            <Logo size={2} bg={false} disableLink />
                            <WordmarkText size="sm" />
                        </Link>

                        <p className="text-sm text-foreground-secondary sm:max-w-sm">
                            This website is still being built. To contribute, message us on
                            discord at{" "}
                            {DISCORD_CONTACTS.map((contact, index) => (
                                <span key={contact.username}>
                                    {index > 0 && " or "}
                                    <Link
                                        href={contact.href}
                                        className="font-semibold text-foreground hover:text-accent transition-colors"
                                    >
                                        {contact.username}
                                    </Link>
                                </span>
                            ))}
                            .
                        </p>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-8 text-center sm:text-left">
                        {FOOTER_LINK_GROUPS.map((group) => (
                            <FooterLinkGroup key={group.title} title={group.title} links={group.links} />
                        ))}
                    </div>
                </div>

                <div className="mt-8 pt-6 border-t border-border flex flex-col-reverse sm:flex-row items-center justify-between gap-3">
                    <p className="text-xs text-foreground-tertiary">
                        &copy; {new Date().getFullYear()} SS Dev Core. All rights reserved.
                    </p>

                    <Link
                        href="https://github.com/xpsaroj/ioe-drive/"
                        className="flex items-center gap-1.5 text-xs text-foreground-tertiary hover:text-foreground transition-colors"
                    >
                        <Github className="size-3.5" />
                        View source
                    </Link>
                </div>
            </div>
        </footer>
    );
}
