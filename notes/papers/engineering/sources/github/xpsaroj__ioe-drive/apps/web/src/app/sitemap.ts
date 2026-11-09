import type { MetadataRoute } from "next";

import { SITE_URL } from "@/lib/site";
import { SERVER_API_BASE_URL } from "@/lib/server-api-url";

// Regenerate at most once a day - the curriculum this walks changes rarely.
export const revalidate = 86400;

interface ProgramSummary {
    id: number;
}

async function fetchJson<T>(path: string): Promise<T | null> {
    // Catches connection failures (e.g. no backend reachable at build time), not just non-OK responses - a network error here shouldn't fail the whole build.
    try {
        const response = await fetch(`${SERVER_API_BASE_URL}${path}`);
        if (!response.ok) return null;

        const body = await response.json();
        return body.success ? (body.data as T) : null;
    } catch {
        return null;
    }
}

async function fetchPrograms(): Promise<ProgramSummary[]> {
    return (await fetchJson<ProgramSummary[]>("/programs")) ?? [];
}

async function fetchAllOfferingIds(programs: ProgramSummary[]): Promise<number[]> {
    const offeringLists = await Promise.all(
        programs.map((program) => fetchJson<number[]>(`/subjects/offering-ids?programId=${program.id}`)),
    );

    return offeringLists.flatMap((ids) => ids ?? []);
}

async function fetchAllApprovedResourceIds(): Promise<number[]> {
    return (await fetchJson<number[]>("/resources/approved-ids")) ?? [];
}

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
    const staticEntries: MetadataRoute.Sitemap = [
        { url: SITE_URL, changeFrequency: "weekly", priority: 1 },
        { url: `${SITE_URL}/resources`, changeFrequency: "daily", priority: 0.9 },
        { url: `${SITE_URL}/offerings`, changeFrequency: "monthly", priority: 0.5 },
        { url: `${SITE_URL}/programs`, changeFrequency: "monthly", priority: 0.5 },
        { url: `${SITE_URL}/market`, changeFrequency: "daily", priority: 0.7 },
        { url: `${SITE_URL}/about`, changeFrequency: "monthly", priority: 0.4 },
        { url: `${SITE_URL}/contact`, changeFrequency: "monthly", priority: 0.3 },
        { url: `${SITE_URL}/privacy`, changeFrequency: "yearly", priority: 0.2 },
        { url: `${SITE_URL}/terms`, changeFrequency: "yearly", priority: 0.2 },
    ];

    const programs = await fetchPrograms();
    const [offeringIds, resourceIds] = await Promise.all([
        fetchAllOfferingIds(programs),
        fetchAllApprovedResourceIds(),
    ]);

    const programEntries: MetadataRoute.Sitemap = programs.map((program) => ({
        url: `${SITE_URL}/programs/${program.id}`,
        changeFrequency: "monthly",
        priority: 0.5,
    }));

    const offeringEntries: MetadataRoute.Sitemap = offeringIds.map((id) => ({
        url: `${SITE_URL}/offerings/${id}`,
        changeFrequency: "monthly",
        priority: 0.6,
    }));

    const resourceEntries: MetadataRoute.Sitemap = resourceIds.map((id) => ({
        url: `${SITE_URL}/resources/r/${id}`,
        changeFrequency: "monthly",
        priority: 0.5,
    }));

    return [...staticEntries, ...programEntries, ...offeringEntries, ...resourceEntries];
}
