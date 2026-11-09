import type { Metadata } from "next";

import { SERVER_API_BASE_URL } from "@/lib/server-api-url";
import ProgramPageClient from "./ProgramPageClient";

interface ProgramPageProps {
    params: Promise<{ programId: string }>;
}

export async function generateMetadata({ params }: ProgramPageProps): Promise<Metadata> {
    const { programId } = await params;

    const response = await fetch(`${SERVER_API_BASE_URL}/programs`, {
        next: { revalidate: 3600 },
    });

    if (!response.ok) {
        return { title: "Program Not Found" };
    }

    const body = await response.json();
    if (!body.success) {
        return { title: "Program Not Found" };
    }

    const program = (body.data as { id: number }[]).find((p) => p.id === Number(programId)) as
        | { code: string; name: string; totalYears: number }
        | undefined;

    if (!program) {
        return { title: "Program Not Found" };
    }

    const title = program.code !== "SH" ? `Bachelor in ${program.name} (${program.code})` : program.name;
    const description = `${program.name} (${program.code}) - full ${program.totalYears}-year curriculum, grouped by semester, with links to shared resources.`;

    return {
        title,
        description,
        openGraph: { title, description, type: "website" },
    };
}

const ProgramPage = (props: ProgramPageProps) => {
    return <ProgramPageClient {...props} />;
};

export default ProgramPage;
