"use client"
import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Github, Heart, Menu } from "lucide-react";

import Logo from "./Logo";
import WordmarkText from "./WordmarkText";
import HeaderMobileMenu from "./HeaderMobileMenu";
import Button from "@/components/ui/Button";
import ThemeToggle from "@/components/ui/ThemeToggle";
import { cn } from "@/utils/cn";

import { PUBLIC_NAV_LINKS } from "@/constants/navigations";

// Signed-out top bar - LayoutWrapper renders this instead of Navbar/MobileNav until sign-in.
export default function Header() {
    const pathname = usePathname();
    const [menuOpen, setMenuOpen] = useState(false);

    return (
        <>
            <header className="bg-header-background backdrop-blur-md border-b border-header-border">
                <div className="container mx-auto flex items-center justify-between gap-3 py-4 px-6">
                    <Link href="/" className="flex items-center gap-2.5 min-w-0 shrink-0">
                        <Logo size={3} bg={false} disableLink />
                        <WordmarkText size="lg" />
                    </Link>

                    <nav className="hidden lg:flex items-center gap-6" aria-label="Primary">
                        {PUBLIC_NAV_LINKS.map(({ href, name }) => {
                            const active = pathname === href || pathname.startsWith(`${href}/`);
                            return (
                                <Link
                                    key={href}
                                    href={href}
                                    className={cn(
                                        "text-sm font-medium transition-colors",
                                        active ? "text-foreground" : "text-foreground-secondary hover:text-foreground"
                                    )}
                                >
                                    {name}
                                </Link>
                            );
                        })}
                    </nav>

                    <div className="flex items-center gap-2 shrink-0">
                        <ThemeToggle />

                        <div className="hidden lg:flex items-center gap-2">
                            <Button
                                variant="secondary"
                                size="md"
                                iconOnly
                                aria-label="Contribute on GitHub"
                                icon={<Github className="size-4" />}
                                href="https://github.com/xpsaroj/ioe-drive/"
                            />
                            <Button variant="secondary" size="md" href="/sign-in">
                                Sign In
                            </Button>
                            <Button variant="primary" size="md" icon={<Heart className="size-4" />}>
                                Donate
                            </Button>
                        </div>

                        <button
                            className="lg:hidden p-2.5 text-foreground bg-button-secondary rounded-md border border-border transition-colors"
                            onClick={() => setMenuOpen(true)}
                            aria-label="Open menu"
                        >
                            <Menu className="w-5 h-5" />
                        </button>
                    </div>
                </div>
            </header>

            {/* Rendered outside <header> on purpose - header's backdrop-blur creates a containing
                block for `fixed` descendants, which would trap this drawer inside header's own
                (short) box instead of overlaying the viewport. */}
            <HeaderMobileMenu open={menuOpen} onClose={() => setMenuOpen(false)} />
        </>
    );
}
