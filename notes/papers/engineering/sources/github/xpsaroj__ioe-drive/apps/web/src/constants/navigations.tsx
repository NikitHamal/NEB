import { LayoutDashboard, NotebookPen, Library, UsersRound, Store, GraduationCap, CloudUpload, BookOpen, UserCircle, ShieldCheck, UserCog, MessageCircle, Info, LucideIcon } from "lucide-react";

import { UserRole } from "@/types/entities";

export interface NavigationItem {
    name: string;
    href: string;
    icon: LucideIcon;
    /** Filtered out entirely (not just hidden) for anyone without one of these roles. */
    allowedRoles?: UserRole[];
}

export interface NavigationGroup {
    label: string;
    items: NavigationItem[];
}

// Shared by the desktop sidebar (Navbar) and mobile drawer (MobileNav) so both stay in sync.
export const NAVIGATION_GROUPS: NavigationGroup[] = [
    {
        label: "Personal",
        items: [
            { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
            { name: 'My Library', href: '/library', icon: Library },
        ],
    },
    {
        label: "Resources",
        items: [
            { name: 'Browse Resources', href: '/resources', icon: NotebookPen },
            { name: 'Share a Resource', href: '/resources/share', icon: CloudUpload },
            { name: 'Curriculum', href: '/offerings', icon: BookOpen },
        ],
    },
    {
        label: "Community",
        items: [
            { name: 'Community', href: '/community', icon: UsersRound },
            { name: 'Market', href: '/market', icon: Store },
            { name: 'Messages', href: '/messages', icon: MessageCircle },
            { name: 'Alumni', href: '/alumni', icon: GraduationCap },
        ],
    },
    {
        label: "Account",
        items: [
            { name: 'Profile', href: '/profile', icon: UserCircle },
        ],
    },
    {
        label: "Moderation",
        items: [
            {
                name: 'Moderation',
                href: '/pm/moderation',
                icon: ShieldCheck,
                allowedRoles: [UserRole.MODERATOR, UserRole.ADMIN],
            },
            {
                name: 'Admin',
                href: '/pm/admin',
                icon: UserCog,
                allowedRoles: [UserRole.ADMIN],
            },
        ],
    },
];

// Drops role-gated items the given role can't see, and the whole group if that empties it.
export const getVisibleNavigationGroups = (role?: UserRole): NavigationGroup[] =>
    NAVIGATION_GROUPS
        .map((group) => ({
            ...group,
            items: group.items.filter((item) => !item.allowedRoles || (!!role && item.allowedRoles.includes(role))),
        }))
        .filter((group) => group.items.length > 0);

// Public routes shown in the signed-out Header/its mobile drawer - none require auth (see proxy.ts).
export const PUBLIC_NAV_LINKS: NavigationItem[] = [
    { name: 'Browse Resources', href: '/resources', icon: NotebookPen },
    { name: 'Curriculum', href: '/offerings', icon: BookOpen },
    { name: 'Programs', href: '/programs', icon: GraduationCap },
    { name: 'Market', href: '/market', icon: Store },
    { name: 'About', href: '/about', icon: Info },
];

// Used to resolve which item wins when a pathname is nested under more than one.
const ALL_NAV_HREFS: string[] = NAVIGATION_GROUPS.flatMap((group) => group.items.map((item) => item.href));

const matchesRoute = (pathname: string, href: string): boolean =>
    pathname === href || pathname.startsWith(`${href}/`);

// Only the longest matching href wins, so a parent route doesn't light up alongside a nested sibling (e.g. /resources vs /resources/share).
export const isNavItemActive = (pathname: string, href: string, allHrefs: string[] = ALL_NAV_HREFS): boolean => {
    if (!matchesRoute(pathname, href)) return false;

    return !allHrefs.some(
        (other) => other !== href && other.length > href.length && matchesRoute(pathname, other)
    );
};
