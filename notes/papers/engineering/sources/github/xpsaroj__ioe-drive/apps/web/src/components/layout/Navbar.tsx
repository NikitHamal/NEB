"use client"
import { usePathname } from "next/navigation"
import { useState } from "react"
import Link from "next/link"
import { PanelLeftClose, PanelLeftOpen } from "lucide-react";

import { SearchBar } from "@/components/layout"
import NavItem from "./NavItem"
import NotificationsBell from "./NotificationsBell"
import Button from "@/components/ui/Button"
import ThemeToggle from "@/components/ui/ThemeToggle"
import Logo from "./Logo"
import WordmarkText from "./WordmarkText"
import { UserMenu } from "./UserMenu"
import { useMe } from "@/hooks/queries/use-me"
import { useUnreadCount } from "@/hooks/queries/use-messaging"

import { getVisibleNavigationGroups, isNavItemActive } from "@/constants/navigations"

export default function Navbar() {
  const pathname = usePathname()
  const { data: userData } = useMe()
  const { data: unreadData } = useUnreadCount()

  const [showDesktopNav, setShowDesktopNav] = useState(true)

  if (!showDesktopNav) {
    return (
      <div className="hidden md:block">
        <Button
          variant="secondary"
          size="sm"
          iconOnly
          className="fixed top-4 left-3 z-30 shadow-sm"
          onClick={() => setShowDesktopNav(true)}
          aria-label="Open navigation"
          icon={<PanelLeftOpen className="size-5" />}
        />
      </div>
    )
  }

  return (
    <div className="hidden md:flex md:flex-col w-64 h-screen overflow-hidden">
      <div className="pt-5 px-4 pb-4 flex flex-col gap-4 border-b border-border">
        <div className="flex items-center justify-between gap-2">
          <Link href="/dashboard" className="flex items-center gap-2 min-w-0">
            <Logo size={2} bg={false} disableLink />
            <WordmarkText size="md" />
          </Link>
          <div className="flex items-center gap-0.5 shrink-0">
            <ThemeToggle />
            <NotificationsBell />
            <Button
              variant="ghost"
              size="sm"
              iconOnly
              onClick={() => setShowDesktopNav(false)}
              aria-label="Collapse navigation"
              icon={<PanelLeftClose className="size-5" />}
            />
          </div>
        </div>

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
                  badgeCount={href === "/messages" ? unreadData?.unreadCount : undefined}
                />
              ))}
            </nav>
          </div>
        ))}
      </div>

      <div className="border-t border-border px-3 py-3 hover:bg-background-hover transition-colors cursor-pointer">
        <UserMenu />
      </div>
    </div>
  )
}
