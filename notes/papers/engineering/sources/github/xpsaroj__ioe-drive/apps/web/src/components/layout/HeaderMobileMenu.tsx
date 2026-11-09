"use client"
import { usePathname } from "next/navigation"
import { useEffect } from "react"
import Link from "next/link"
import clsx from "clsx"
import { X, Github, Heart } from "lucide-react"

import NavItem from "./NavItem"
import Logo from "./Logo"
import WordmarkText from "./WordmarkText"
import Button from "@/components/ui/Button"
import ThemeToggle from "@/components/ui/ThemeToggle"

import { PUBLIC_NAV_LINKS } from "@/constants/navigations"

interface HeaderMobileMenuProps {
    open: boolean
    onClose: () => void
}

// Mobile counterpart to Header's desktop nav row - same slide-in-drawer pattern as MobileNav,
// but with public links + sign-in/up instead of the authenticated nav groups. Controlled by
// Header (which owns the trigger button) and rendered as Header's sibling, not its child - see
// the comment where Header renders this.
export default function HeaderMobileMenu({ open, onClose }: HeaderMobileMenuProps) {
    const pathname = usePathname()

    useEffect(() => {
        document.body.style.overflow = open ? "hidden" : "unset"
        return () => {
            document.body.style.overflow = "unset"
        }
    }, [open])

    return (
        <div className="lg:hidden">
            <div
                className={clsx(
                    "fixed top-0 left-0 h-full w-[80%] max-w-xs flex flex-col bg-background shadow-xl z-70 transform transition-transform duration-300 ease-out",
                    open ? "translate-x-0" : "-translate-x-full"
                )}
            >
                <div className="flex items-center justify-between px-4 py-4 border-b border-border">
                    <Link href="/" className="flex items-center gap-2 min-w-0" onClick={onClose}>
                        <Logo size={2} bg={false} disableLink />
                        <WordmarkText size="sm" />
                    </Link>
                    <div className="flex items-center gap-0.5">
                        <ThemeToggle />
                        <button onClick={onClose} aria-label="Close menu" className="rounded-full border-none py-2 px-1">
                            <X className="w-5 h-5" />
                        </button>
                    </div>
                </div>

                <nav className="px-3 py-4 flex flex-col gap-0.5 overflow-y-auto" aria-label="Public navigation">
                    {PUBLIC_NAV_LINKS.map(({ href, icon, name }) => (
                        <NavItem
                            key={href}
                            href={href}
                            icon={icon}
                            name={name}
                            active={pathname === href || pathname.startsWith(`${href}/`)}
                            onClick={onClose}
                        />
                    ))}
                </nav>

                <div className="mt-auto border-t border-border p-4 flex flex-col gap-3">
                    <div className="flex gap-2">
                        <Button href="/sign-in" variant="secondary" className="flex-1" onClick={onClose}>
                            Sign In
                        </Button>
                        <Button href="/sign-up" variant="primary" className="flex-1" onClick={onClose}>
                            Sign Up
                        </Button>
                    </div>
                    <div className="flex gap-2">
                        <Button
                            href="https://github.com/xpsaroj/ioe-drive/"
                            variant="ghost"
                            className="flex-1"
                            icon={<Github className="size-4" />}
                        >
                            Contribute
                        </Button>
                        <Button variant="ghost" className="flex-1" icon={<Heart className="size-4" />}>
                            Donate
                        </Button>
                    </div>
                </div>
            </div>

            {open && (
                <div
                    className="fixed inset-0 bg-black/40 z-65 transition-opacity duration-300"
                    onClick={onClose}
                />
            )}
        </div>
    )
}
