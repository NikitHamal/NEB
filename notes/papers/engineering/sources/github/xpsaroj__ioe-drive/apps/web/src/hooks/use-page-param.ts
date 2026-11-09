"use client";

import { useCallback } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

const DEFAULT_PAGE = 1;

// Must be used in a component wrapped in <Suspense>, since useSearchParams requires it.
export const usePageParam = (paramName: string = "page") => {
    const router = useRouter();
    const pathname = usePathname();
    const searchParams = useSearchParams();

    const rawPage = Number(searchParams.get(paramName));
    const page = Number.isInteger(rawPage) && rawPage > 0 ? rawPage : DEFAULT_PAGE;

    const setPage = useCallback((nextPage: number) => {
        const params = new URLSearchParams(searchParams.toString());

        if (nextPage <= DEFAULT_PAGE) {
            params.delete(paramName);
        } else {
            params.set(paramName, String(nextPage));
        }

        const query = params.toString();
        router.replace(`${pathname}${query ? `?${query}` : ""}`);
    }, [router, pathname, searchParams, paramName]);

    return { page, setPage };
};
