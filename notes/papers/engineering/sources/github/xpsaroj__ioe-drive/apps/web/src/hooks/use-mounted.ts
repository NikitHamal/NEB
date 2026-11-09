import { useSyncExternalStore } from "react";

const subscribe = () => () => {};

// False until the first client render, so SSR hydration matches exactly.
export function useMounted(): boolean {
    return useSyncExternalStore(
        subscribe,
        () => true,
        () => false
    );
}
