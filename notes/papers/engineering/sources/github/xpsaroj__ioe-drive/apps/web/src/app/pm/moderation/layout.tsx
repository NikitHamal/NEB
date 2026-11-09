import type { Metadata } from "next";

import ModerationGate from "./ModerationGate";

// Only keeps this out of search results - real access control is the server-side @Roles("MODERATOR") guard.
export const metadata: Metadata = {
    robots: { index: false, follow: false },
};

const ModerationLayout = ({ children }: { children: React.ReactNode }) => (
    <ModerationGate>{children}</ModerationGate>
);

export default ModerationLayout;
