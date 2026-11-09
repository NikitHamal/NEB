"use client";
import { useAuth } from "@clerk/nextjs"
import { usePathname } from "next/navigation";
import { useTheme } from "next-themes";
import { Toaster } from "sonner";

import Navbar from "./Navbar";
import MobileNav from "./MobileNav";
import Header from "./Header";
import Footer from "./Footer";

const LayoutWrapper = ({ children }: { children: React.ReactNode }) => {
    const { isSignedIn } = useAuth()
    const pathname = usePathname()
    // sonner defaults to light theme with no `theme` prop - "system" is a safe fallback before the real theme is known.
    const { resolvedTheme } = useTheme();
    const toasterTheme = (resolvedTheme as "light" | "dark") ?? "system";

    const pagesWithFooter = ["/", "/about", "/contact", "/privacy", "/terms"]

    if (!isSignedIn) return (
        <div className="flex-col min-h-screen">
            <Header />
            <div className="flex-1">
                {children}
            </div>
            <Toaster richColors position="top-right" theme={toasterTheme} />
            {pagesWithFooter.includes(pathname) && (
                <Footer />
            )}
        </div>
    )

    return (
        <div className="flex md:flex-row flex-col min-h-screen">
            {/* z-20 so the navbar wins over a page's own sticky elements (e.g. a sticky breadcrumb bar). */}
            <div className="hidden md:block sticky top-0 h-screen border-r z-20">
                <Navbar />
            </div>
            <div className="md:hidden">
                <MobileNav />
            </div>
            <Toaster richColors position="top-right" theme={toasterTheme} />
            <div className="md:flex-1 flex flex-col min-h-screen">
                <div className="flex-1">
                    {children}
                </div>
                {pagesWithFooter.includes(pathname) && (
                    <Footer />
                )}
            </div>
        </div>
    )
}

export default LayoutWrapper