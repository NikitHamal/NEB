"use client"
import { BookSpines, DEFAULT_SHELF_SPINES } from "@/components/decor";
import Loader from "@/components/ui/Loader";
import { ProgramCard } from "@/components/common/offering";
import { usePrograms } from "@/hooks/queries/use-academics";
import { getErrorMessage } from "@/lib/errors";

// SH (Science & Humanities) owns cross-cutting first-year subjects but isn't a program
// students enroll in - not shown here, same as it's excluded from db:seed-resources.
const NON_STUDENT_FACING_PROGRAM_CODES = new Set(["SH"]);

const ProgramsPage = () => {
    const { data: programs, isPending, error } = usePrograms();
    const visiblePrograms = (programs ?? []).filter((program) => !NON_STUDENT_FACING_PROGRAM_CODES.has(program.code));

    return (
        <div className="min-h-screen bg-background text-foreground max-w-7xl mx-auto md:px-8 px-6 md:py-8 py-6 md:space-y-8 space-y-6">
            <div className="relative overflow-hidden rounded-lg border border-border bg-background-secondary p-6 md:p-8">
                <BookSpines spines={DEFAULT_SHELF_SPINES} />
                <div className="relative z-10 max-w-md">
                    <h1 className="text-2xl md:text-3xl font-bold text-foreground">Programs</h1>
                    <p className="mt-1 text-foreground-secondary">
                        Browse any IOE program&apos;s full curriculum, semester by semester.
                    </p>
                </div>
            </div>

            {isPending ? (
                <div className="flex items-center justify-center py-16">
                    <Loader text="Loading programs. Please wait." />
                </div>
            ) : error ? (
                <div className="flex items-center justify-center py-16">
                    <p className="text-error">{getErrorMessage(error, "Couldn't load programs. Please try again.")}</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    {visiblePrograms.map((program) => (
                        <ProgramCard key={program.id} program={program} href={`/programs/${program.id}`} />
                    ))}
                </div>
            )}
        </div>
    );
};

export default ProgramsPage;
