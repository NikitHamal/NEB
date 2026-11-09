"use client";

import { MotionConfig } from "motion/react";

// Every animation in the app automatically respects the OS "reduce motion" preference.
export function MotionProvider({ children }: { children: React.ReactNode }) {
    return <MotionConfig reducedMotion="user">{children}</MotionConfig>;
}
