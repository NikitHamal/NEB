import fs from "fs";
import path from "path";

const ROOT = path.join(process.cwd(), "public", "bca");

export type Unit = {
  n: number;
  title: string;
  area: string;
  questions: number;
  file: string;
  words: number;
  mcq: number;
};
export type Book = {
  slug: string;
  name: string;
  paperQuestions: number;
  pdf: string;
  syllabus: string;
  units: Unit[];
  header: string;
};
export type Manifest = {
  title: string;
  books: Book[];
  docs: { name: string; file: string }[];
};

export function getManifest(): Manifest {
  return JSON.parse(fs.readFileSync(path.join(ROOT, "manifest.json"), "utf8")) as Manifest;
}

/** Markdown of a chapter without its frontmatter. */
export function readUnit(file: string): string {
  const raw = fs.readFileSync(path.join(ROOT, file), "utf8");
  const m = raw.match(/^---\n([\s\S]*?)\n---\n/);
  return m ? raw.slice(m[0].length) : raw;
}

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/**
 * Turns the NEBians `::: key Title ... :::` containers into HTML wrappers.
 * Answer boxes become collapsed <details> so a student can try first.
 */
export function prepare(md: string): string {
  const out: string[] = [];
  const stack: string[] = [];
  for (const line of md.split("\n")) {
    const open = line.match(/^:::\s+(\w+)\s*(.*)$/);
    if (open) {
      const type = open[1];
      const title = esc(open[2] || type);
      if (type === "note" && /Answers/.test(title)) {
        out.push(`<details class="answers"><summary>${title}</summary>`, "");
        stack.push("</details>");
      } else {
        out.push(`<div class="box box-${type}"><div class="box-title">${title}</div>`, "");
        stack.push("</div>");
      }
      continue;
    }
    if (/^:::\s*$/.test(line) && stack.length) {
      out.push("", stack.pop() as string, "");
      continue;
    }
    out.push(line);
  }
  return out.join("\n");
}
