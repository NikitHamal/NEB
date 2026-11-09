'use client';

import { useAuth } from '@clerk/nextjs';
import { useEffect } from 'react';
import { apiClient } from '@/lib/api/api-client';

export function ClerkApiProvider({ children }: { children: React.ReactNode }) {
    const { getToken } = useAuth();

    useEffect(() => {
        apiClient.setTokenProvider(async () => {
            return await getToken();
        });
    }, [getToken]);

    return <>{children}</>;
}