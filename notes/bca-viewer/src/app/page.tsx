import Link from "next/link";
import { getManifest } from "@/lib/bca";

const BLURB: Record<string, string> = {
  "bca-math":
    "Half the paper. Arithmetic, algebra, trigonometry, coordinate geometry, vectors, calculus and reasoning, with formula sheets and 600 keyed questions.",
  "bca-eng":
    "Forty marks of grammar and vocabulary: idioms, tenses, voice, narration, clauses, error spotting, plus reading passages.",
  "bca-gk":
    "Ten marks that cost the least to win: Nepal and world GK (dated to 2026) and computer fundamentals, Internet, HTML and full forms.",
  "bca-mock":
    "The exam guide, a 12-week plan, the BCA programme map, and three full 100-question model papers in the Dean's Office layout.",
};

export default function Home() {
  const m = getManifest();
  const chapters = m.books.reduce((a, b) => a + b.units.length, 0);
  const mcq = m.books.reduce((a, b) => a + b.units.reduce((x, u) => x + u.mcq, 0), 0);
  return (
    <main className="mx-auto max-w-5xl px-4 pb-24 pt-10">
      <header className="mb-10">
        <p className="text-xs font-semibold uppercase tracking-widest text-amber-800">
          NEBians · free and open learning
        </p>
        <h1 className="mt-2 text-4xl font-extrabold leading-tight text-stone-900 sm:text-5xl">
          BCA Entrance, end to end.
        </h1>
        <p className="mt-4 max-w-2xl text-lg text-stone-700">
          The complete preparation set for the Tribhuvan University BCA entrance (FOHSS): syllabus,
          chapter notes, formula sheets, {mcq.toLocaleString()} explained questions and three model
          papers. Read it here or download every file.
        </p>
        <div className="mt-6 flex flex-wrap gap-3 text-sm">
          <a className="btn-primary" href="/bca/NEBians-BCA-all.zip" download>
            Download everything (.zip)
          </a>
          <Link className="btn" href="/read/bca-mock/1">
            Start with the exam guide
          </Link>
          <Link className="btn" href="/read/bca-mock/2">
            Take Model Paper 1
          </Link>
        </div>
        <dl className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
          {[
            ["100", "questions in the paper"],
            ["2 h", "to answer them"],
            [String(chapters), "chapters written"],
            [mcq.toLocaleString(), "keyed practice MCQs"],
          ].map(([a, b]) => (
            <div key={b} className="rounded-xl border border-stone-200 bg-white p-4">
              <dt className="text-2xl font-bold text-stone-900">{a}</dt>
              <dd className="text-sm text-stone-600">{b}</dd>
            </div>
          ))}
        </dl>
      </header>

      <section className="mb-10 rounded-2xl border border-amber-200 bg-amber-50 p-5 text-sm leading-6 text-stone-800">
        <b>How the paper splits:</b> English grammar 40 · Mathematics 50 · General Knowledge and IT
        10, in that order (Group A, B, C), one mark each. Start with Mathematics; it is half the
        marks. The pattern comes from the Faculty&apos;s published description and the Dean&apos;s
        Office model questions. Negative marking is not reported by any source we found, but check
        the notice of your year.
      </section>

      <section className="grid gap-5 md:grid-cols-2">
        {m.books.map((b) => (
          <div key={b.slug} className="rounded-2xl border border-stone-200 bg-white p-5 shadow-sm">
            <div className="flex items-baseline justify-between gap-2">
              <h2 className="text-xl font-bold text-stone-900">{b.name}</h2>
              <span className="text-xs text-stone-500">
                {b.slug === "bca-mock" ? "3 papers" : `${b.paperQuestions} of 100 marks`}
              </span>
            </div>
            <p className="mt-2 text-sm text-stone-600">{BLURB[b.slug]}</p>
            <ol className="mt-4 space-y-1.5 text-sm">
              {b.units.map((u) => (
                <li key={u.n} className="flex items-start gap-2">
                  <span className="w-6 shrink-0 text-right text-stone-400">{u.n}</span>
                  <Link
                    className="flex-1 text-stone-800 hover:text-amber-800 hover:underline"
                    href={`/read/${b.slug}/${u.n}`}
                  >
                    {u.title}
                  </Link>
                  <a
                    className="text-xs text-stone-400 hover:text-amber-800"
                    href={`/bca/${u.file}`}
                    download
                    title="Download Markdown"
                  >
                    .md
                  </a>
                </li>
              ))}
            </ol>
            <div className="mt-5 flex flex-wrap gap-2 text-sm">
              <a className="btn-primary" href={`/bca/${b.pdf}`} download>
                Download PDF
              </a>
              <a className="btn" href={`/bca/${b.syllabus}`} download>
                Syllabus spine
              </a>
            </div>
          </div>
        ))}
      </section>

      <section className="mt-12 rounded-2xl border border-stone-200 bg-white p-5">
        <h2 className="text-lg font-bold">Documentation</h2>
        <ul className="mt-3 list-disc space-y-1 pl-5 text-sm">
          {m.docs.map((d) => (
            <li key={d.file}>
              <a className="text-amber-800 underline" href={`/bca/${d.file}`}>
                {d.name}
              </a>
              {d.name.startsWith("HANDOFF")
                ? " — state, sources, what is missing, next steps"
                : " — the authoring contract"}
            </li>
          ))}
        </ul>
        <p className="mt-4 text-sm text-stone-600">
          All questions are original practice written to the published pattern, not past papers. The
          books have not yet been reviewed by a BCA entrance teacher: if a key looks wrong, trust
          your teacher and tell us.
        </p>
      </section>
    </main>
  );
}
