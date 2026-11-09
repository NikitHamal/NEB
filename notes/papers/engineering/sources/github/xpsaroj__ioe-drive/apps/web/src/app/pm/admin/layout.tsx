import type { Metadata } from "next";

import AdminGate from "./AdminGate";

// Only keeps this out of search results - real access control is the server-side @Roles("ADMIN") guard.
export const metadata: Metadata = {
    robots: { index: false, follow: false },
};

const AdminLayout = ({ children }: { children: React.ReactNode }) => (
    <AdminGate>{children}</AdminGate>
);

export default AdminLayout;
