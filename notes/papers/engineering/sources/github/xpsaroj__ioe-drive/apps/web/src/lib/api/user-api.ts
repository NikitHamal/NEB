import { apiClient } from "./api-client";
import { UserProfileSummary } from "@/types/api";
import { ApiResponse } from "@/types/api";

const USER_API_BASE_URL = "/users";

export const userApi = {
    async getUserById(userId: number): Promise<ApiResponse<UserProfileSummary>> {
        return apiClient.get<ApiResponse<UserProfileSummary>>(`${USER_API_BASE_URL}/${userId}`);
    }
}