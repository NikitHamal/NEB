import { useAuth } from "@clerk/nextjs";
import { useQuery, keepPreviousData } from "@tanstack/react-query";

import { academicsApi } from "@/lib/api/academics-api";
import type { Semester } from "@/types/entities";

export const academicsKeys = {
    all: ["academics"] as const,
    programs: ["academics", "programs"] as const,
    subjectOfferings: (programId?: number, semester?: Semester) => [...academicsKeys.all, "subject-offerings", programId, semester] as const,
    subjectDetails: (offeringId: number) => [...academicsKeys.all, "subject-details", offeringId] as const,
    subjectsForUpload: (programId?: number, semester?: Semester) => [...academicsKeys.all, "subjects-for-upload", programId, semester] as const,
    search: (q: string, page?: number) => [...academicsKeys.all, "search", q, page] as const,
};

// `semester` is optional - omit it to get every semester's offerings for the program, already
// ordered by semester on the backend.
export function useSubjectOfferings(programId?: number, semester?: Semester) {
    return useQuery({
        queryKey: academicsKeys.subjectOfferings(programId, semester),
        queryFn: async () => {
            if (!programId) {
                throw new Error("Program ID is required");
            }
            const response = await academicsApi.getSubjectsByProgramAndSemester({ programId, semester })
            if (!response.success) {
                throw new Error(response.error || "Failed to fetch subject offerings");
            }
            return response.data;
        },
        enabled: !!programId,
        staleTime: 20 * 60 * 1000,
        gcTime: 30 * 60 * 1000,
    });
}

export function usePrograms() {
    return useQuery({
        queryKey: academicsKeys.programs,
        queryFn: async () => {
            const response = await academicsApi.getAllPrograms();
            if (!response.success) {
                throw new Error(response.error || "Failed to fetch programs");
            }
            return response.data;
        },
        staleTime: Infinity,    // Cache indefinitely since programs do not change
        gcTime: Infinity,
    });
}

export function useSubjectDetails(offeringId: number) {
    return useQuery({
        queryKey: academicsKeys.subjectDetails(offeringId),
        queryFn: async () => {
            const response = await academicsApi.getSubjectDetails(offeringId);
            if (!response.success) {
                throw new Error(response.error || "Failed to fetch subject details");
            }
            return response.data;
        },
        enabled: !!offeringId,
        staleTime: 2 * 60 * 1000,
        gcTime: 3 * 60 * 1000,
    });
}

export function useSubjectsForUpload(programId?: number, semester?: Semester) {
    const { isSignedIn } = useAuth();

    return useQuery({
        queryKey: academicsKeys.subjectsForUpload(programId, semester),
        queryFn: async () => {
            if (!programId || !semester) {
                throw new Error("Program ID and semester are required");
            }
            const response = await academicsApi.getSubjectsForUpload({ programId, semester });
            if (!response.success) {
                throw new Error(response.error || "Failed to fetch subjects");
            }
            return response.data;
        },
        enabled: !!(isSignedIn && programId && semester),
        staleTime: 20 * 60 * 1000,
        gcTime: 30 * 60 * 1000,
    });
}

// Matches the backend's own minimum length validation (see `q` on SearchSubjectsQueryDto).
export const MIN_SEARCH_QUERY_LENGTH = 1;

export function useSearchSubjects(q: string, page: number = 1, limit?: number) {
    const trimmed = q.trim();

    return useQuery({
        queryKey: academicsKeys.search(trimmed, page),
        queryFn: async () => {
            const response = await academicsApi.searchSubjects(trimmed, { page, limit });
            if (!response.success) {
                throw new Error(response.error || "Failed to search subjects");
            }
            return { items: response.data, meta: response.meta };
        },
        enabled: trimmed.length >= MIN_SEARCH_QUERY_LENGTH,
        placeholderData: keepPreviousData,
    });
}