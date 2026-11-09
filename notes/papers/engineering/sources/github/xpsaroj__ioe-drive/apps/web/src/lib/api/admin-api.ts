import { apiClient } from "./api-client";
import type { ApiResponse, UserSummary } from "@/types/api";

const ADMIN_API_BASE_URL = "/admin";

export interface ChangeUserRoleInput {
    email: string;
    role: "USER" | "MODERATOR";
}

export const adminApi = {
    async changeUserRole(data: ChangeUserRoleInput): Promise<ApiResponse<UserSummary>> {
        return apiClient.patch<ApiResponse<UserSummary>>(`${ADMIN_API_BASE_URL}/users/role`, data);
    },
}
