import os, re, sys, json, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONTENT = os.path.join(ROOT, "content")
KW = re.compile(r"\b(human|heart|brain|kidney|liver|lung|eye|ear|skin|skull|skeleton|bone|muscle|tooth|teeth|stomach|intestin|nephron|neuron|sperm|ovum|ovary|uterus|embryo|foetus|fetus|placenta|blood|cell|cells|micrograph|section|t\.s\.|l\.s\.|root|stem|leaf|flower|fruit|seed|pollen|stomata|chloroplast|mitochond|nucleus|chromosom|bacteri|virus|fung|alga|moss|fern|amoeba|paramecium|euglena|yeast|hydra|planaria|tapeworm|roundworm|earthworm|leech|cockroach|insect|butterfl|mosquito|bee|honey|ant\b|spider|crab|prawn|snail|starfish|fish|frog|toad|lizard|snake|turtle|bird|pigeon|rabbit|mammal|animal|plant|tree|forest|species|specimen|organism|dissect|apparatus|set-?up|experiment|burette|pipette|flask|beaker|test tube|bunsen|microscope|vernier|screw gauge|galvanometer|voltmeter|ammeter|rheostat|telescope|motherboard|cpu|ram|hard disk|ssd|port|connector|cable|router|switch|server|keyboard|monitor|printer|scanner|ic\b|chip|circuit board|network hardware|planet|moon|sun\b|galaxy|nebula|star|earth|crystal|mineral|ore|flame|precipitate|portrait|photograph|map of|nepal|mountain|river|glacier|rock|fossil)\b", re.I)
def scan():
    rows = []
    for slug in sorted(os.listdir(CONTENT)):
        d = os.path.join(CONTENT, slug)
        if not os.path.isdir(d) or slug.startswith("."): continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md"): continue
            lines = open(os.path.join(d, fn), encoding="utf-8").read().replace("\r", "").split("\n")
            for i, ln in enumerate(lines, 1):
                m = re.match(r'^```(figure|photo)\b(.*)$', ln)
                if not m: continue
                kind, rest = m.groups()
                cap = re.search(r'caption="((?:[^"\\]|\\.)*)"', rest)
                pid = re.search(r'id="([^"]+)"', rest)
                rows.append(dict(book=slug, unit=fn[5:7], line=i, kind="real" if kind == "photo" else "generated",
                                 id=pid.group(1) if pid else "", caption=(cap.group(1) if cap else "")[:200]))
    return rows
if __name__ == "__main__":
    rows = scan()
    for r in rows:
        r["candidate"] = bool(r["kind"] == "generated" and KW.search(r["caption"]))
    json.dump(rows, open(os.path.join(ROOT, "inventory", "figures.json"), "w"), ensure_ascii=False, indent=0)
    agg = collections.OrderedDict()
    for r in rows:
        a = agg.setdefault(r["book"], [0, 0, 0]); a[0] += r["kind"] == "real"; a[1] += r["kind"] == "generated"; a[2] += r["candidate"]
    print(f"{'book':8} real generated candidates")
    for b, (re_, g, c) in agg.items(): print(f"{b:8} {re_:4} {g:9} {c:9}")
    print("TOTAL", sum(a[0] for a in agg.values()), sum(a[1] for a in agg.values()), sum(a[2] for a in agg.values()))

def write_md(rows):
    by = collections.OrderedDict()
    for r in rows: by.setdefault(r["book"], []).append(r)
    o = open(os.path.join(ROOT, "inventory", "FIGURES.md"), "w", encoding="utf-8")
    o.write("# Figure inventory\n\nRegenerate with `python3 pipeline/figinventory.py`. `real` = ```photo block (licensed image in `assets/`); `generated` = ```figure block (matplotlib). ⚑ = generated figure whose caption names a real-world thing, flagged for review.\n\n| book | real | generated | flagged |\n|---|---|---|---|\n")
    for b, rs in by.items():
        o.write(f"| {b} | {sum(r['kind']=='real' for r in rs)} | {sum(r['kind']=='generated' for r in rs)} | {sum(r['candidate'] for r in rs)} |\n")
    for b, rs in by.items():
        o.write(f"\n## {b}\n\n| unit | line | kind | id | caption |\n|---|---|---|---|---|\n")
        for r in rs:
            o.write(f"| {r['unit']} | {r['line']} | {r['kind']}{' ⚑' if r['candidate'] else ''} | {r['id']} | {r['caption'].replace('|','/')[:110]} |\n")
rows = scan()
for r in rows: r["candidate"] = bool(r["kind"] == "generated" and KW.search(r["caption"]))
write_md(rows)
