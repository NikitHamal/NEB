import Link from "next/link";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import remarkBreaks from "remark-breaks";
import rehypeKatex from "rehype-katex";
import rehypeRaw from "rehype-raw";
import { getManifest, prepare, readUnit } from "@/lib/bca";

export function generateStaticParams() {
  return getManifest().books.flatMap((b) =>
    b.units.map((u) => ({ book: b.slug, unit: String(u.n) })),
  );
}

export default async function ReadPage({
  params,
}: {
  params: Promise<{ book: string; unit: string }>;
}) {
  const { book, unit } = await params;
  const b = getManifest().books.find((x) => x.slug === book);
  const idx = b ? b.units.findIndex((u) => String(u.n) === unit) : -1;
  if (!b || idx < 0) notFound();
  const u = b.units[idx];
  const prev = b.units[idx - 1];
  const next = b.units[idx + 1];
  const md = prepare(readUnit(u.file));

  return (
    <main className="mx-auto max-w-3xl px-4 pb-24 pt-6">
      <nav className="mb-6 flex flex-wrap items-center gap-x-4 gap-y-2 text-sm">
        <Link href="/" className="font-semibold text-amber-800 hover:underline">
          ← BCA library
        </Link>
        <span className="text-stone-400">/</span>
        <span className="text-stone-600">{b.name}</span>
        <span className="ml-auto flex gap-3">
          <a className="btn" href={`/bca/${u.file}`} download>
            Chapter .md
          </a>
          <a className="btn" href={`/bca/${b.pdf}`} download>
            Book PDF
          </a>
        </span>
      </nav>
      <p className="text-xs uppercase tracking-wider text-stone-500">
        {b.name} · {u.area} · {u.mcq} practice questions · ~{Math.round(u.words / 200)} min read
      </p>
      <h1 className="mb-6 mt-1 text-3xl font-bold leading-tight text-stone-900">
        {u.n}. {u.title}
      </h1>
      <article className="bca-prose">
        <ReactMarkdown
          remarkPlugins={[remarkGfm, remarkMath, remarkBreaks]}
          rehypePlugins={[rehypeRaw, [rehypeKatex, { throwOnError: false, strict: false }]]}
        >
          {md}
        </ReactMarkdown>
      </article>
      <div className="mt-12 grid grid-cols-2 gap-3">
        {prev ? (
          <Link className="navcard" href={`/read/${b.slug}/${prev.n}`}>
            <span className="text-xs text-stone-500">Previous</span>
            <span className="font-semibold">
              {prev.n}. {prev.title}
            </span>
          </Link>
        ) : (
          <span />
        )}
        {next ? (
          <Link className="navcard text-right" href={`/read/${b.slug}/${next.n}`}>
            <span className="text-xs text-stone-500">Next</span>
            <span className="font-semibold">
              {next.n}. {next.title}
            </span>
          </Link>
        ) : (
          <span />
        )}
      </div>
    </main>
  );
}
