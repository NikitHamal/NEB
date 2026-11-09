"use client";
import { useForm, Controller } from "react-hook-form";
import { toast } from "sonner";

import Input from "@/components/ui/Input";
import Select from "@/components/ui/Select";
import Button from "@/components/ui/Button";
import { useChangeUserRole } from "@/hooks/queries/use-admin";
import { getErrorMessage } from "@/lib/errors";

interface FormValues {
    email: string;
    role: "USER" | "MODERATOR" | "";
}

const AdminPage = () => {
    const { mutate, isPending } = useChangeUserRole();

    const {
        handleSubmit,
        control,
        register,
        reset,
        formState: { errors },
    } = useForm<FormValues>({ defaultValues: { email: "", role: "" } });

    const onSubmit = (data: FormValues) => {
        mutate(
            { email: data.email, role: data.role as "USER" | "MODERATOR" },
            {
                onSuccess: (user) => {
                    toast.success(`${user.fullName} is now ${user.role === "MODERATOR" ? "a moderator" : "a regular user"}.`);
                    reset();
                },
                onError: (error) => {
                    toast.error(getErrorMessage(error, "Couldn't update the user's role. Please try again."));
                },
            }
        );
    };

    return (
        <div className="max-w-lg rounded-lg border border-border p-6 space-y-4">
            <div>
                <h2 className="text-lg font-semibold text-foreground">Change a user&apos;s role</h2>
                <p className="text-sm text-foreground-secondary mt-1">
                    Promote a user to moderator, or demote a moderator back to a regular user.
                    Granting admin access isn&apos;t available here.
                </p>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
                <Input
                    label="Email"
                    type="email"
                    required
                    placeholder="user@example.com"
                    error={errors.email?.message}
                    disabled={isPending}
                    {...register("email", { required: "Email is required" })}
                />

                <Controller
                    control={control}
                    name="role"
                    rules={{ required: "Role is required" }}
                    render={({ field }) => (
                        <Select
                            label="New role"
                            placeholder="Select a role"
                            required
                            value={field.value}
                            error={errors.role?.message}
                            disabled={isPending}
                            onChange={field.onChange}
                            options={[
                                { value: "USER", label: "User" },
                                { value: "MODERATOR", label: "Moderator" },
                            ]}
                        />
                    )}
                />

                <Button type="submit" disabled={isPending}>
                    {isPending ? "Updating..." : "Update Role"}
                </Button>
            </form>
        </div>
    );
};

export default AdminPage;
