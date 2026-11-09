"use client";
import { useState } from "react";

import Badge from "@/components/ui/Badge";

const NEW_RESOURCE_MAX_AGE_MS = 3 * 24 * 60 * 60 * 1000;

interface NewBadgeProps {
    createdAt: string;
}

const NewBadge = ({ createdAt }: NewBadgeProps) => {
    // Lazy initializer runs once at mount, not on every render - keeps this pure per React's render rules.
    const [now] = useState(() => Date.now());
    const isNew = now - new Date(createdAt).getTime() < NEW_RESOURCE_MAX_AGE_MS;

    if (!isNew) return null;

    return <Badge size="sm" variant="info">New</Badge>;
};

export default NewBadge;
