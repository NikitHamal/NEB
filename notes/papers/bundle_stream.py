"""Bundle papers of DIFFERENT subjects into one stream bundle (e.g. Computer Engineering technical stream 2080).

    python3 bundle_stream.py --slug 12-ce-technical-2080 --title "Computer Engineering Technical Stream" \
        --year 2080 --ids 12-vp-2080-9341 12-wdd-2080-656 12-sepm-2080-9371

Writes pdf/bundles/NEBians-Past-Papers-Grade-12-<slug>-Bundle.pdf and adds a record to bundles.json
(same cover/contents/bookmarks layout as bundle_papers.py)."""
import argparse, json, os, html as _html
import pymupdf
from weasyprint import HTML
import bundle_papers as bp
ap = argparse.ArgumentParser()
ap.add_argument("--slug", required=True); ap.add_argument("--title", required=True)
ap.add_argument("--year", required=True); ap.add_argument("--grade", default="12"); ap.add_argument("--label", default="Board past papers"); ap.add_argument("--filetag", default="Past-Papers"); ap.add_argument("--category", default="Board Exam Bundle"); ap.add_argument("--ids", nargs="+", required=True)
a = ap.parse_args()
man = {m["id"]: m for m in json.load(open(os.path.join(bp.HERE, "manifest.json"), encoding="utf-8")) if "id" in m}
rs = [man[i] for i in a.ids]
os.makedirs(bp.OUT, exist_ok=True)
name = "NEBians-%s-Grade-%s-%s-Bundle.pdf" % (a.filetag, a.grade, a.slug)
rows, page = [], 2
for r in rs:
    rows.append((r, page)); page += r["pages"]
trs = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
    _html.escape(r["subject"]), _html.escape(r["code"] or r.get("stream", "").split("(")[-1].rstrip(")")), r["marks"], r["time"], p) for r, p in rows)
cover = ('<html><head><style>%s</style></head><body><div class="brand">NEBIANS</div><h1>%s</h1>'
         '<div class="sub">Grade %s · %s %s BS · with full solutions</div>'
         '<table><tr><th>Subject</th><th>Code / coverage</th><th>Marks</th><th>Time</th><th>Page</th></tr>%s</table>'
         '<p class="note">%d papers, %d pages. Every paper is followed by its worked solutions: answer key with reasons, '
         'programs and diagrams drawn out, and answers sized to the marks.</p></body></html>'
         % (bp.CSS, _html.escape(a.title), a.grade, a.label, a.year, trs, len(rs), page - 1))
tmp = os.path.join(bp.OUT, "_cover.pdf"); HTML(string=cover).write_pdf(tmp)
out = pymupdf.open(tmp)
toc = [[1, "%s %s Bundle" % (a.title, a.year), 1]]
for r, p in rows:
    out.insert_pdf(pymupdf.open(os.path.join(bp.PDF, r["file"]))); toc.append([1, "%s (%s)" % (r["subject"], r["code"] or "mid-term"), p])
out.set_toc(toc)
out.set_metadata({"title": "%s Grade %s %s %s - NEBians" % (a.title, a.grade, a.label, a.year), "author": "NEBians"})
path = os.path.join(bp.OUT, name); out.save(path, garbage=4, deflate=True); os.remove(tmp)
bj = os.path.join(bp.HERE, "bundles.json"); recs = json.load(open(bj))
recs = [x for x in recs if x["file"] != "bundles/" + name]
recs.append({"file": "bundles/" + name, "subject": a.title, "grade": a.grade, "years_bs": a.year, "papers": a.ids,
             "pages": len(out), "bytes": os.path.getsize(path), "category": a.category, "slug": a.slug})
json.dump(recs, open(bj, "w"), indent=1); print(name, len(out), "pages")
