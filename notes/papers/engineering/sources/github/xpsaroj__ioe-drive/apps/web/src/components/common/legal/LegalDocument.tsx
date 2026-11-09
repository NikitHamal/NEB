import Link from "next/link";

export interface LegalSection {
    id: string;
    heading: string;
    body: React.ReactNode;
}

interface LegalDocumentProps {
    title: string;
    description: string;
    lastUpdated: string;
    sections: LegalSection[];
}

// Shared prose styling for section bodies, applied once here so /privacy and /terms can
// just write plain <p>/<ul>/<strong>/<a> without repeating classes in every section.
const proseClasses =
    "[&>*+*]:mt-4 " +
    "[&>p]:text-foreground-secondary [&>p]:leading-relaxed " +
    "[&>ul]:list-disc [&>ul]:space-y-2 [&>ul]:pl-5 [&>ul]:text-foreground-secondary " +
    "[&_strong]:font-semibold [&_strong]:text-foreground " +
    "[&_a]:text-accent [&_a]:underline [&_a]:underline-offset-2 hover:[&_a]:text-accent-hover";

// Shared by /privacy and /terms - a title block, a jump-to-section TOC, and numbered sections.
const LegalDocument = ({ title, description, lastUpdated, sections }: LegalDocumentProps) => {
    return (
        <div className="container mx-auto max-w-5xl px-6 py-16 md:py-20">
            <div className="max-w-2xl">
                <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">{title}</h1>
                <p className="mt-4 text-foreground-secondary">{description}</p>
                <p className="mt-3 text-sm text-foreground-tertiary">Last updated {lastUpdated}</p>
            </div>

            <div className="mt-12 flex flex-col gap-10 md:flex-row md:gap-16">
                <nav
                    aria-label="Sections"
                    className="shrink-0 md:sticky md:top-6 md:h-fit md:w-56"
                >
                    <p className="font-display text-xs font-semibold uppercase tracking-wide text-foreground-tertiary">
                        On this page
                    </p>
                    <ol className="mt-3 space-y-2">
                        {sections.map((section, index) => (
                            <li key={section.id}>
                                <Link
                                    href={`#${section.id}`}
                                    className="text-sm text-foreground-secondary hover:text-accent transition-colors"
                                >
                                    {index + 1}. {section.heading}
                                </Link>
                            </li>
                        ))}
                    </ol>
                </nav>

                <div className="min-w-0 flex-1 divide-y divide-border">
                    {sections.map((section, index) => (
                        <section key={section.id} id={section.id} className="scroll-mt-6 py-8 first:pt-0">
                            <h2 className="text-xl font-semibold text-foreground">
                                {index + 1}. {section.heading}
                            </h2>
                            <div className={`mt-3 ${proseClasses}`}>{section.body}</div>
                        </section>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default LegalDocument;
