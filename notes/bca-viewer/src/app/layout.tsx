import type { Metadata } from "next";
import "katex/dist/katex.min.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "NEBians BCA Entrance — free notes, MCQs and model papers",
  description:
    "Complete, free preparation for the TU BCA entrance: syllabus, chapter notes, formula sheets, explained MCQs and full model papers. Read online or download Markdown and PDF.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
