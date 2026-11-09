"use client"
import { useEffect, useState } from "react";
import { UserProfile } from "@clerk/nextjs";
import { useForm, Controller } from "react-hook-form";
import { Pencil } from "lucide-react";
import { toast } from "sonner";

import { useMe, useUpdateProfile } from "@/hooks/queries/use-me";
import { getErrorMessage } from "@/lib/errors";
import { usePrograms } from "@/hooks/queries/use-academics";
import Select from "@/components/ui/Select";
import Input from "@/components/ui/Input";
import Textarea from "@/components/ui/Textarea";
import Button from "@/components/ui/Button";
import Loader from "@/components/ui/Loader";
import { Semester, SemesterLabel } from "@/types/entities";

type FormValues = {
    bio: string;
    programId: string;
    semester: Semester | "";
    college: string;
};

const ProfilePage = () => {
    const { data: userData, isPending: userPending } = useMe();
    const profile = userData?.profile;

    const { data: programs, isPending: programsPending } = usePrograms();
    const { mutateAsync: updateProfile, isPending: isSaving } = useUpdateProfile();

    const [isEditing, setIsEditing] = useState(false);

    const {
        handleSubmit,
        control,
        register,
        reset,
    } = useForm<FormValues>({
        defaultValues: { bio: "", programId: "", semester: "", college: "" },
    });

    // Keep the form in sync with the latest profile data, so re-opening Edit always reflects what's saved.
    useEffect(() => {
        if (!profile) return;
        reset({
            bio: profile.bio ?? "",
            programId: profile.programId ? String(profile.programId) : "",
            semester: profile.semester ?? "",
            college: profile.college ?? "",
        });
    }, [profile, reset]);

    const onSubmit = async (data: FormValues) => {
        try {
            await updateProfile({
                bio: data.bio,
                programId: data.programId ? Number(data.programId) : undefined,
                semester: data.semester || undefined,
                college: data.college,
            });
            toast.success("Profile updated successfully.");
            setIsEditing(false);
        } catch (err) {
            toast.error(getErrorMessage(err, "Couldn't update your profile. Please try again."));
        }
    };

    return (
        <div className="min-h-screen bg-background text-foreground max-w-7xl mx-auto md:p-8 p-6 space-y-6 md:space-y-8">
            {/* Title and both sections below are direct children of this one shared,
                narrower, centered wrapper - that's what keeps the title aligned with the
                cards below it, and what guarantees the two cards end up the same width
                as each other (and Clerk's own UserProfile, whatever it renders at)
                rather than each being sized independently. */}
            <div className="mx-auto w-full max-w-4xl space-y-6 md:space-y-8">
            <div>
                <h1 className="text-2xl md:text-3xl font-bold text-foreground">Profile</h1>
                <p className="mt-1 text-foreground-secondary">Manage your personal details and account settings.</p>
            </div>

            <div className="rounded-lg border border-border p-6">
                <div className="mb-4 flex items-center justify-between gap-4">
                    <h2 className="text-lg font-semibold text-foreground">Profile Details</h2>
                    {!isEditing && (
                        <Button
                            variant="secondary"
                            size="sm"
                            icon={<Pencil className="size-4" />}
                            onClick={() => setIsEditing(true)}
                        >
                            Edit
                        </Button>
                    )}
                </div>

                {userPending || programsPending ? (
                    <Loader text="Loading profile..." />
                ) : isEditing ? (
                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
                        <Textarea
                            label="Bio"
                            rows={3}
                            placeholder="Tell others a bit about yourself..."
                            disabled={isSaving}
                            {...register("bio")}
                        />

                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                            <Controller
                                control={control}
                                name="programId"
                                render={({ field }) => (
                                    <Select
                                        label="Program"
                                        placeholder="Select Program"
                                        value={field.value}
                                        disabled={isSaving}
                                        onChange={field.onChange}
                                        options={(programs ?? []).map((prog) => ({
                                            value: String(prog.id),
                                            label: `${prog.code} - ${prog.name}`,
                                        }))}
                                    />
                                )}
                            />

                            <Controller
                                control={control}
                                name="semester"
                                render={({ field }) => (
                                    <Select
                                        label="Semester"
                                        placeholder="Select Semester"
                                        value={field.value}
                                        disabled={isSaving}
                                        onChange={field.onChange}
                                        options={Object.keys(SemesterLabel).map((sem) => ({
                                            value: sem,
                                            label: `${SemesterLabel[sem as Semester]} ${+sem > 8 ? "(Architecture)" : ""}`,
                                        }))}
                                    />
                                )}
                            />
                        </div>

                        <Input
                            label="College"
                            placeholder="e.g. Pulchowk Campus"
                            disabled={isSaving}
                            {...register("college")}
                        />

                        <div className="flex justify-end gap-3 border-t border-border pt-4">
                            <Button
                                type="button"
                                variant="secondary"
                                disabled={isSaving}
                                onClick={() => {
                                    if (profile) {
                                        reset({
                                            bio: profile.bio ?? "",
                                            programId: profile.programId ? String(profile.programId) : "",
                                            semester: profile.semester ?? "",
                                            college: profile.college ?? "",
                                        });
                                    }
                                    setIsEditing(false);
                                }}
                            >
                                Cancel
                            </Button>
                            <Button type="submit" disabled={isSaving}>
                                {isSaving ? "Saving..." : "Save Changes"}
                            </Button>
                        </div>
                    </form>
                ) : (
                    <div className="space-y-4">
                        <div>
                            <p className="mb-1 font-display text-xs font-medium uppercase tracking-wide text-foreground-tertiary">
                                Bio
                            </p>
                            <p className="text-sm text-foreground-secondary">
                                {profile?.bio || "No bio set yet."}
                            </p>
                        </div>

                        <div className="border-t border-border pt-2">
                            <div className="flex items-center justify-between py-2">
                                <span className="text-sm text-foreground-secondary">Program</span>
                                <span className="text-sm font-medium text-foreground">
                                    {profile?.program?.name ?? "Not set"}
                                </span>
                            </div>
                            <div className="flex items-center justify-between py-2">
                                <span className="text-sm text-foreground-secondary">Semester</span>
                                <span className="text-sm font-medium text-foreground">
                                    {profile?.semester ? SemesterLabel[profile.semester] : "Not set"}
                                </span>
                            </div>
                            <div className="flex items-center justify-between py-2">
                                <span className="text-sm text-foreground-secondary">College</span>
                                <span className="text-sm font-medium text-foreground">
                                    {profile?.college ?? "Not set"}
                                </span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <div>
                <h2 className="mb-4 text-lg font-semibold text-foreground">Account Details</h2>
                <UserProfile />
            </div>
            </div>
        </div>
    )
}

export default ProfilePage;
