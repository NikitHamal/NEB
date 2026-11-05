# BCA viewer

A small Next.js (App Router) reader for the BCA books: `src/` is the app, `public/bca/` is every file it
serves and every file a student can download (Markdown chapters, syllabus spines, PDFs, docs, manifest,
`NEBians-BCA-all.zip`). Rebuild the data with `python3 notes/tools/bca_build.py --public <app>/public/bca`.
Needs `react-markdown remark-gfm remark-math remark-breaks rehype-katex rehype-raw katex`.
