import { useQuery } from "@tanstack/react-query";
import { userApi } from "@/lib/api/user-api";

export const userKeys = {
    all: ["user"] as const,
    byId: (id: number) => ["user", id] as const,
};

export function useUserById(userId: number) {
    return useQuery({
        queryKey: userKeys.byId(userId),
        queryFn: async () => {
            const response = await userApi.getUserById(userId);
            if (!response.success) {
                throw new Error(response.error || "Failed to fetch user");
            }
            return response.data;
        },

        enabled: !!userId && !isNaN(Number(userId)),
    });
}