import { useEffect, useState } from "react";

// So a query keyed off a fast-changing value (e.g. search input) doesn't fire on every keystroke.
export function useDebouncedValue<T>(value: T, delayMs: number = 300): T {
    const [debounced, setDebounced] = useState(value);

    useEffect(() => {
        const timeout = setTimeout(() => setDebounced(value), delayMs);
        return () => clearTimeout(timeout);
    }, [value, delayMs]);

    return debounced;
}
