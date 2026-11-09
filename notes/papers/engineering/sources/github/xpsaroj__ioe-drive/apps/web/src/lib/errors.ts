// Decides what a page/component actually shows when a request fails.
//
// The backend is the source of truth for domain errors ("You can't vote on your
// own resource") and those are worth surfacing verbatim. But it also has to send
// *something* for unexpected/system failures (masked to "Internal Server Error"
// in production, or its own internal "Failed to create ..." strings in dev), and
// the API client has a last-resort "API request failed". None of those are useful
// to a user - for them we show a contextual fallback supplied by the caller
// ("Couldn't post the listing. Please try again.") instead.

const GENERIC_MESSAGES = new Set([
    "Internal Server Error",
    "API request failed",
    "Unknown error",
    "Something went wrong",
    "Failed to create resource",
    "Failed to create listing",
    "Failed to create conversation",
    "Failed to create message",
    "Failed to create notification",
    "Failed to create user",
]);

// NestJS's default route-not-found response, e.g. "Cannot GET /api/foo".
const NEST_NOT_FOUND_PREFIX = "Cannot ";

// Every hook falls back to a "Failed to ..." string when the server sends no error
// message at all (e.g. `response.error || 'Failed to fetch programs'`). Those are
// placeholders, not server copy - always swap them for the caller's context.
const HOOK_FALLBACK_PREFIX = "Failed to ";

const isMessageUseful = (message: string): boolean => {
    if (!message.trim()) return false;
    if (GENERIC_MESSAGES.has(message)) return false;
    if (message.startsWith(NEST_NOT_FOUND_PREFIX)) return false;
    if (message.startsWith(HOOK_FALLBACK_PREFIX)) return false;
    return true;
};

const isSystemError = (error: unknown): boolean => {
    if (error instanceof Error) {
        const status = (error as Error & { status?: number }).status;
        if (typeof status === "number" && status >= 500) return true;
        return !isMessageUseful(error.message);
    }
    return true;
};

/**
 * Returns the error message to show in the UI.
 *
 * Passes through the backend's message when it's a real, user-facing domain
 * message (i.e. a 4xx with specific copy). Falls back to the caller's contextual
 * message - e.g. "Couldn't load programs. Please try again." - for system errors
 * (5xx, generic/unknown messages) where the raw text is useless or leaking.
 */
export const getErrorMessage = (error: unknown, fallback: string): string => {
    if (error instanceof Error && !isSystemError(error)) {
        return error.message;
    }
    return fallback;
};
