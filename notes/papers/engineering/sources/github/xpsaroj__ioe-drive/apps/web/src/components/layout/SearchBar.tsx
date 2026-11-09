"use client";
import { useEffect, useState } from "react";
import { Search } from "lucide-react";

import SearchDialog from "./SearchDialog";

export default function SearchBar() {
    const [isOpen, setIsOpen] = useState(false);

    // Ctrl/Cmd+K opens search from anywhere, not just via this button.
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
                e.preventDefault();
                setIsOpen(true);
            }
        };

        document.addEventListener("keydown", handleKeyDown);
        return () => document.removeEventListener("keydown", handleKeyDown);
    }, []);

    return (
        <>
            <button
                type="button"
                onClick={() => setIsOpen(true)}
                className="flex items-center gap-2 border border-border rounded-md px-3 py-2 w-full text-left transition-colors hover:bg-background-hover hover:border-border-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-background cursor-pointer"
            >
                <Search className="size-4 text-foreground-tertiary shrink-0" />
                <span className="text-sm text-foreground-tertiary flex-1">Search...</span>
                <span className="hidden sm:inline-flex items-center rounded border border-border px-1.5 py-0.5 font-display text-[10px] text-foreground-tertiary">
                    Ctrl K
                </span>
            </button>

            {isOpen && <SearchDialog isOpen={isOpen} onClose={() => setIsOpen(false)} />}
        </>
    );
}
