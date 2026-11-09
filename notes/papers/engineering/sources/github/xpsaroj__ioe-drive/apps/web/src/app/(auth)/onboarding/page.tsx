"use client"

import { useRouter } from "next/navigation"
import { useEffect } from "react"
import { useForm, Controller, useWatch } from "react-hook-form"

import { Semester, SemesterLabel } from "@/types/entities"
import { usePrograms } from "@/hooks/queries/use-academics"
import { useMe } from "@/hooks/queries/use-me"
import { useUpdateProfile } from "@/hooks/queries/use-me"
import { getErrorMessage } from "@/lib/errors"

import Select from "@/components/ui/Select"
import Input from "@/components/ui/Input"
import Button from "@/components/ui/Button"
import Loader from "@/components/ui/Loader"
import { ScatteredCodeTiles, type ScatteredTile } from "@/components/decor"

type FormValues = {
    programId: string
    semester: Semester | ""
    college: string
}

// Only this program's students run to semester 10 - everyone else caps at 8.
const ARCHITECTURE_PROGRAM_CODE = "BAR"

// Scattered around the page, clear of the center ~60% where the card sits.
const ONBOARDING_TILES: ScatteredTile[] = [
    { code: "BCT", top: "10%", left: "8%", rotate: -6, size: "size-11 text-xs", solid: true, float: true },
    { code: "BEX", top: "82%", left: "12%", rotate: 4, size: "size-10 text-xs", float: true },
    { code: "BEE", top: "14%", left: "86%", rotate: 5, size: "size-10 text-xs", float: true },
    { code: "BCE", top: "80%", left: "84%", rotate: -4, size: "size-11 text-xs", solid: true, float: true },
    { code: "BME", top: "46%", left: "4%", rotate: 7, size: "size-9 text-[10px]", float: true },
    { code: "BAR", top: "44%", left: "92%", rotate: 3, size: "size-9 text-[10px]", float: true },
]

const OnBoardingPage = () => {
    const router = useRouter()

    const { data: programs, isPending: programsPending } = usePrograms();

    const { data: userData, isPending: userPending, error } = useMe();
    const profile = userData ? userData?.profile : null;

    const { mutateAsync: updateProfile, isPending } = useUpdateProfile();

    const {
        handleSubmit,
        control,
        register,
        setError,
        setValue,
        formState: { errors }
    } = useForm<FormValues>({
        defaultValues: {
            programId: "",
            semester: "",
            college: ""
        }
    })

    const selectedProgramId = useWatch({ control, name: "programId" })
    const isArchitecture = programs?.find(p => p.id === Number(selectedProgramId))?.code === ARCHITECTURE_PROGRAM_CODE

    // Already onboarded (e.g. revisiting this URL directly) - about to redirect below, so
    // don't flash the form for a frame first.
    const alreadyOnboarded = !!(profile?.semester && profile?.programId)

    useEffect(() => {
        if (alreadyOnboarded) {
            router.push("/dashboard")
        }
    }, [alreadyOnboarded, router])


    const onSubmit = async (data: FormValues) => {
        // react-hook-form's `required` rule guarantees this before onSubmit fires - narrows the type for updateProfile below.
        if (!data.semester) return;

        if (programs?.find(p => p.id === Number(data.programId))?.code !== ARCHITECTURE_PROGRAM_CODE && Number(data.semester) > 8) {
            setError("semester", {
                message: "Only students in the BAR program can select a semester beyond 8."
            })
            return;
        }

        try {
            await updateProfile({
                programId: Number(data.programId),
                semester: data.semester,
                college: data.college,
            });

            router.push("/dashboard")
        } catch (updateError) {
            setError("root", {
                message: getErrorMessage(updateError, "Couldn't update your profile. Please try again.")
            })
        }
    }

    if (programsPending || userPending || alreadyOnboarded) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto">
                <div className="flex flex-col items-center justify-center">
                    <Loader text="Loading. Please wait." />
                </div>
            </div>
        )
    }

    if (error || !programs) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto">
                <div className="flex flex-col items-center justify-center">
                    <p className="text-error">{getErrorMessage(error, "Couldn't load your profile. Please try again.")}</p>
                    <div className="flex space-x-4">
                        <Button variant="secondary" className="mt-4" onClick={() => router.refresh()}>
                            Refresh Page
                        </Button>
                        <Button variant="primary" className="mt-4" onClick={() => router.back()}>
                            Go Back
                        </Button>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="relative overflow-hidden min-h-screen flex justify-center items-center bg-background text-foreground md:p-8 p-6 max-w-7xl mx-auto">
            <ScatteredCodeTiles tiles={ONBOARDING_TILES} />

            <div className="relative z-10 w-full max-w-xl bg-card border rounded-lg md:p-8 p-6 shadow-sm">

                <div className="mb-6">
                    <h1 className="text-2xl font-semibold">One last step.</h1>
                    <p className="text-foreground-secondary text-sm mt-1">
                        Tell us your program and semester so we can show you the right resources by default. You can skip this if you want.
                    </p>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">

                    <Controller
                        control={control}
                        name="programId"
                        rules={{
                            required: "Program is required"
                        }}
                        render={({ field }) => (
                            <Select
                                label="Program"
                                placeholder="Select program"
                                value={field.value}
                                error={errors.programId?.message}
                                onChange={(e) => {
                                    field.onChange(e);
                                    // Clear a semester beyond 8 if it's no longer valid for the newly picked program.
                                    const newIsArchitecture = programs.find(p => String(p.id) === e.target.value)?.code === ARCHITECTURE_PROGRAM_CODE;
                                    if (!newIsArchitecture) setValue("semester", "");
                                }}
                                options={programs.map((prog) => ({
                                    value: String(prog.id),
                                    label: `${prog.code} - ${prog.name}`,
                                }))}
                                helperText="Select the program you are currently enrolled in."
                            />
                        )}
                    />

                    <Controller
                        control={control}
                        name="semester"
                        rules={{
                            required: "Semester is required"
                        }}
                        render={({ field }) => (
                            <Select
                                label="Semester"
                                placeholder="Select semester"
                                value={field.value}
                                error={errors.semester?.message}
                                disabled={!selectedProgramId}
                                onChange={field.onChange}
                                options={Object.keys(SemesterLabel)
                                    .filter((sem) => isArchitecture || +sem <= 8)
                                    .map((sem) => ({
                                        value: String(sem),
                                        label: `${SemesterLabel[sem as Semester]} ${+sem > 8 ? "(Architecture)" : ""}`,
                                    }))}
                                helperText={
                                    selectedProgramId
                                        ? "Select the semester you are currently in."
                                        : "Select a program first to see valid semesters."
                                }
                            />
                        )}
                    />

                    <Input
                        label="College"
                        placeholder="XYZ Engineering College"
                        error={errors.college?.message}
                        {...register("college", {
                            required: "College name is required",
                            minLength: { value: 3, message: "College name must be at least 3 characters long" },
                            maxLength: { value: 50, message: "College name must be less than 50 characters long" }
                        })}
                    />

                    {errors.root && (
                        <p className="mt-1.5 text-sm text-error">
                            {errors.root.message}
                        </p>
                    )}

                    <div className="flex gap-3 pt-4">
                        <Button
                            type="button"
                            disabled={isPending}
                            href="/dashboard"
                            variant="secondary"
                            className="flex-1"
                        >
                            Skip
                        </Button>

                        <Button
                            type="submit"
                            disabled={isPending}
                            className="flex-1"
                        >
                            {isPending ? "Saving..." : "Save & Continue"}
                        </Button>

                    </div>

                </form>
            </div>
        </div>
    )
}

export default OnBoardingPage
