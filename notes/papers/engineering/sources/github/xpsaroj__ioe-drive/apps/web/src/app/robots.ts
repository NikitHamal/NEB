import type { MetadataRoute } from "next";

import { SITE_URL } from "@/lib/site";

export default function robots(): MetadataRoute.Robots {
    return {
        rules: {
            userAgent: "*",
            allow: "/",
            disallow: [
                "/dashboard",
                "/library",
                "/profile",
                "/onboarding",
                "/resources/share",
                "/resources/r/*/edit",
                "/resources/r/*/files/*",
                "/community",
                "/alumni",
                "/messages",
                "/market/create",
                "/market/*/edit",
                "/sign-in",
                "/sign-up",
            ],
        },
        sitemap: `${SITE_URL}/sitemap.xml`,
    };
}
