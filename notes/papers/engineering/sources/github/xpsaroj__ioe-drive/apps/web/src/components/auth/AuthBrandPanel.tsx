"use client";
import { motion } from "motion/react";

import { ScatteredCodeTiles, type ScatteredTile } from "@/components/decor";

interface AuthBrandPanelProps {
    variant: "sign-in" | "sign-up";
}

const COPY: Record<AuthBrandPanelProps["variant"], { title: string; description: string }> = {
    "sign-in": {
        title: "Welcome back to your library.",
        description: "Sign in to get back to your saved resources, bookmarks, and uploads.",
    },
    "sign-up": {
        title: "Join your batch's library.",
        description: "Browse notes, past questions, and lab sheets by program, semester, and subject.",
    },
};

// Real IOE bachelor's program codes, not invented decoration.
const SCATTERED_CODES: ScatteredTile[] = [
    { code: "BCT", top: "8%", left: "8%", rotate: -6, size: "size-14 text-sm", solid: true, float: true },
    { code: "BEX", top: "10%", left: "28%", rotate: 4, size: "size-12 text-xs", float: true },
    { code: "BEE", top: "14%", left: "68%", rotate: 5, size: "size-11 text-xs", float: true },
    { code: "BCE", top: "60%", left: "74%", rotate: -4, size: "size-14 text-sm", solid: true, float: true },
    { code: "BME", top: "76%", left: "20%", rotate: 7, size: "size-11 text-xs", float: true },
    { code: "BAR", top: "86%", left: "52%", rotate: 3, size: "size-12 text-xs", float: true },
    { code: "BIE", top: "28%", left: "88%", rotate: 6, size: "size-11 text-xs", float: true },
];

// Hidden below `lg` so mobile keeps the Clerk widget front and center.
const AuthBrandPanel = ({ variant }: AuthBrandPanelProps) => {
    const { title, description } = COPY[variant];

    return (
        <div className="relative hidden lg:flex flex-col justify-center overflow-hidden border-r border-border bg-background-secondary px-14">
            <ScatteredCodeTiles tiles={SCATTERED_CODES} />

            <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, ease: "easeOut", delay: 0.08 }}
                className="relative z-10 max-w-sm"
            >
                <p className="font-display text-xs tracking-[0.2em] uppercase text-accent font-medium mb-4">
                    For IOE students, by IOE students
                </p>
                <h2 className="text-3xl font-bold tracking-tight text-foreground mb-4 text-balance">
                    {title}
                </h2>
                <p className="text-foreground-secondary text-balance">
                    {description}
                </p>
            </motion.div>
        </div>
    );
};

export default AuthBrandPanel;
