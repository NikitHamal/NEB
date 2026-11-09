"use client"
import { usePathname } from "next/navigation"
import { useState, useEffect } from "react"
import Link from "next/link"
import clsx from "clsx"
import { Menu, X } from "lucide-react"

import { SearchBar } from "@/components/layout"
import NavItem from "./NavItem"
import NotificationsBell from "./NotificationsBell"
import ThemeToggle from "@/components/ui/ThemeToggle"
import Logo from "./Logo"
import WordmarkText from "./WordmarkText"
import { UserMenu } from "./UserMenu"
import { useMe } from "@/hooks/queries/use-me"
import { useUnreadCount } from "@/hooks/queries/use-messaging"

import { getVisibleNavigationGroups, isNavItemActive } from "@/constants/navigations"

export default function MobileNav() {
    const pathname = usePathname()
    const { data: userData } = useMe()
    const { data: unreadData } = useUnreadCount()

    const [menuOpen, setMenuOpen] = useState(false)

    useEffect(() => {
        if (menuOpen) {
            document.body.style.overflow = "hidden"
        } else {
            document.body.style.overflow = "unset"
        }
        return () => {
            document.body.style.overflow = "unset"
        }
    }, [menuOpen])

    return (
        <div>
            <div className="fixed top-3 right-3 md:hidden z-9999">
                <button
                    className="p-3 text-foreground bg-background/80 backdrop-blur-sm rounded-full shadow-lg transition-colors border border-button-primary"
                    onClick={() => setMenuOpen(true)}
                    aria-label="Open menu"
                >
                    <Menu className="w-5 h-5" />
                </button>
            </div>

            <div className="block md:hidden sticky top-0 z-50">
                <div
                    className={clsx(
                        "fixed top-0 left-0 h-full w-[70%] flex flex-col bg-background shadow-xl z-70 transform transition-transform duration-300 ease-out",
                        menuOpen ? "translate-x-0" : "-translate-x-full"
                    )}
                >
                    <div className="flex items-center justify-between px-4 py-4 border-b border-border">
                        <Link
                            href="/dashboard"
                            className="flex items-center gap-2 min-w-0"
                            onClick={() => setMenuOpen(false)}
                        >
                            <Logo size={2} disableLink />
                            <WordmarkText size="sm" />
                        </Link>
                        <div className="flex items-center gap-0.5">
                            <ThemeToggle />
                            <NotificationsBell />
                            <button
                                onClick={() => setMenuOpen(false)}
                                aria-label="Close menu"
                                className="rounded-full border-none py-2 px-1"
                            >
                                <X className="w-5 h-5 rounded-full" />
                            </button>
                        </div>
                    </div>

                    <div className="px-3 pt-3">
                        <SearchBar />
                    </div>

                    <div className="h-full px-3 py-4 flex flex-col gap-6 overflow-y-auto">
                        {getVisibleNavigationGroups(userData?.role).map((group) => (
                            <div key={group.label}>
                                <h3 className="px-1 mb-2 text-[11px] font-display font-medium text-foreground-tertiary uppercase tracking-[0.15em]">
                                    {group.label}
                                </h3>
                                <nav className="flex flex-col gap-0.5" aria-label={group.label}>
                                    {group.items.map(({ href, icon, name }) => (
                                        <NavItem
                                            key={href}
                                            href={href}
                                            icon={icon}
                                            name={name}
                                            active={isNavItemActive(pathname, href)}
                                            onClick={() => setMenuOpen(false)}
                                            badgeCount={href === "/messages" ? unreadData?.unreadCount : undefined}
                                        />
                                    ))}
                                </nav>
                            </div>
                        ))}
                    </div>

                    <div className="border-t border-border pt-4 px-4">
                        <UserMenu />
                    </div>
                </div>

                {menuOpen && (
                    <div
                        className="fixed inset-0 overflow-hidden bg-black/40 z-65 transition-opacity duration-300"
                        onClick={() => setMenuOpen(false)}
                    />
                )}
            </div>
        </div>
    )
}
