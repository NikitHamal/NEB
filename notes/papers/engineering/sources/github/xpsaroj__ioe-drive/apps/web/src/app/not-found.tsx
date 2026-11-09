"use client"
import { useAuth } from "@clerk/nextjs";
import { motion } from "motion/react";

import { ScatteredCodeTiles, type ScatteredTile } from "@/components/decor";

/** Kept clear of the center ~70% where the "404" text sits. */
const SCATTERED_CODES: ScatteredTile[] = [
    { code: "BCT", top: "10%", left: "8%", rotate: -6, size: "size-12 text-sm", solid: true, float: true },
    { code: "BEE", top: "14%", left: "84%", rotate: 5, size: "size-11 text-xs", float: true },
    { code: "BEX", top: "80%", left: "10%", rotate: 4, size: "size-11 text-xs", float: true },
    { code: "BCE", top: "76%", left: "84%", rotate: -4, size: "size-12 text-sm", solid: true, float: true },
    { code: "BME", top: "48%", left: "4%", rotate: 7, size: "size-10 text-xs", float: true },
    { code: "BAR", top: "46%", left: "92%", rotate: 3, size: "size-10 text-xs", float: true },
];

export default function NotFound() {
    const { isSignedIn } = useAuth();

    return (
        <div
            className={`relative overflow-hidden ${isSignedIn ? "min-h-screen" : "min-h-[calc(100vh-13rem)]"} flex flex-col items-center justify-center bg-background px-6 py-12 text-center`}
        >
            <ScatteredCodeTiles tiles={SCATTERED_CODES} />

            <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, ease: "easeOut" }}
                className="relative z-10"
            >
                <h1 className="text-8xl font-bold text-foreground">404</h1>
                <p className="mt-4 text-xl text-foreground-secondary">
                    Oops! The page you are looking for does not exist.
                </p>
            </motion.div>
        </div>
    );
}
