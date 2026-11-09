import { apiClient } from "./api-client";
import { appendPaginationParams, type PaginationParams } from "./pagination";
import type { Program, Semester, SubjectOfferingWithSubject, SubjectForUploadForm } from "@/types/entities";
import type { ApiResponse, PaginatedApiResponse, SubjectSearchResult } from "@/types/api";

export interface SubjectsFilters {
    programId: number;
    semester?: Semester;
}

export interface ResourceUploadFormFilters {
    programId: number;
    semester: Semester;
}

export const academicsApi = {
    async getAllPrograms(): Promise<ApiResponse<Program[]>> {
        return apiClient.get<ApiResponse<Program[]>>("/programs");
    },

    // Fetches all subjects for the program if semester is omitted.
    async getSubjectsByProgramAndSemester(filters: SubjectsFilters): Promise<ApiResponse<SubjectOfferingWithSubject[]>> {
        const params = new URLSearchParams({
            programId: filters.programId.toString(),
        });
        if (filters.semester) {
            params.append("semester", filters.semester);
        }

        return apiClient.get<ApiResponse<SubjectOfferingWithSubject[]>>(`/subjects?${params.toString()}`);
    },

    async getSubjectDetails(subjectId: number): Promise<ApiResponse<SubjectOfferingWithSubject>> {
        return apiClient.get<ApiResponse<SubjectOfferingWithSubject>>(`/subjects/${subjectId}`);
    },

    async getSubjectsForUpload(filters: ResourceUploadFormFilters): Promise<ApiResponse<SubjectForUploadForm[]>> {
        const params = new URLSearchParams({
            programId: filters.programId.toString(),
            semester: filters.semester,
        })
        return apiClient.get<ApiResponse<SubjectForUploadForm[]>>(`/subjects/upload/?${params.toString()}`);
    },

    async searchSubjects(q: string, pagination?: PaginationParams): Promise<PaginatedApiResponse<SubjectSearchResult>> {
        const params = new URLSearchParams({ q });
        appendPaginationParams(params, pagination);
        return apiClient.get<PaginatedApiResponse<SubjectSearchResult>>(`/subjects/search?${params.toString()}`);
    },
}