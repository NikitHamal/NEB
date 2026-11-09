import { NextResponse } from 'next/server';
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isProtectedRoute = createRouteMatcher([
    "/dashboard(.*)",
    // "/resources(.*)" is intentionally public - browsing resources doesn't require sign-in
    "/resources/share(.*)",
    "/resources/r/(.*)/edit(.*)",
    "/resources/r/(.*)/files/(.*)",
    "/library(.*)",
    "/community(.*)",
    // "/market(.*)" is intentionally public - browsing listings doesn't require sign-in, same as resources.
    "/market/create(.*)",
    "/market/(.*)/edit(.*)",
    "/messages(.*)",
    "/alumni(.*)",
    "/profile(.*)",
    "/onboarding",
]);

const isAuthPage = createRouteMatcher([
    '/sign-in(.*)',
    '/sign-up(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
    const { isAuthenticated } = await auth();

    if (!isAuthenticated && isProtectedRoute(req)) {
        await auth.protect();
    }

    if (isAuthenticated && isAuthPage(req)) {
        return NextResponse.redirect(new URL('/dashboard', req.url));
    }

    return;
});

export const config = {
    matcher: [
        // Skip Next.js internals and all static files, unless found in search params
        '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',

        // Protect all API routes - Clerk's own routes are automatically excluded by Clerk.
        '/(api|trpc)(.*)',
    ],
};