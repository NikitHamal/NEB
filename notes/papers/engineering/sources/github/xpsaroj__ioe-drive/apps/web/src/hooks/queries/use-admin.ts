import { useMutation } from '@tanstack/react-query';

import { adminApi, type ChangeUserRoleInput } from '@/lib/api/admin-api';

// Nothing to invalidate - no query currently reads another user's role by email.
export function useChangeUserRole() {
    return useMutation({
        mutationFn: async (data: ChangeUserRoleInput) => {
            const response = await adminApi.changeUserRole(data);
            if (!response.success) {
                throw new Error(response.error || 'Failed to update role');
            }
            return response.data;
        },
    });
}
