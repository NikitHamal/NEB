"""Reading flow: turn dense authored paragraphs into short, scannable blocks.

Every pass works on the HTML that md2html has already produced, so it improves every book
without touching a source file:

* `blank_before_lists`  a list that follows a line of text without a blank line was being
  swallowed into the paragraph ("1. ... 2. ... 3. ..." printed as one run).
* `promote_tall`        a tall formula (fraction, limit, integral, sum) inside running text is set
  on its own centred line, as in a printed textbook.
* `structure_prose`     a long paragraph is cut into short blocks at sentence ends; labelled
  sub-parts ("Verification:", "Example:", "Geometrically") start their own block with a label.
* `example_steps`       inside worked examples every statement of the working gets its own line and
  (a) (b) (c) parts become rows.
* `align_tables`        tables whose cells are short values (trig tables, truth tables) are
  centred on equal columns.
"""
import html as _html
import re

_LISTLN = re.compile(r"^[ \t]{0,3}(?:\d{1,2}[.)]|[-*+])[ \t]+\S")
_HR = re.compile(r"^[ \t]{0,3}(?:[-*_][ \t]*){3,}$")
_TAGS = re.compile(r"<[^>]+>")


def blank_before_lists(body):
    out, fence, prev = [], False, ""
    for ln in body.split("\n"):
        if re.match(r"^\s*(```|~~~)", ln):
            fence = not fence
        if (not fence and _LISTLN.match(ln) and not _HR.match(ln) and prev.strip()
                and not _LISTLN.match(prev) and not _HR.match(prev)
                and not prev.startswith((" ", "\t", ":::", "|", ">", "#", "<", "\x00"))
                and not re.match(r"^\x00NEB\d+\x00$", prev.strip())):
            out.append("")
        out.append(ln)
        prev = ln
    return "\n".join(out)


# ---------------------------------------------------------------- helpers
def _balanced(s):
    for t in ("strong", "em", "b", "i", "code", "span", "a", "sub", "sup"):
        if len(re.findall(r"<%s[\s>]" % t, s)) != len(re.findall(r"</%s>" % t, s)):
            return False
    return True


def _weight(frag):
    """Visible length where every formula image counts as a clause."""
    n = len(re.findall(r"<img\b", frag))
    return len(_TAGS.sub("", re.sub(r"<img[^>]*>", "", frag)).strip()) + 12 * n


_END = re.compile(r"(?<!\bRs)(?<!e\.g)(?<!i\.e)(?<!\bNo)(?<!\bvs)(?<!etc)(?<!\bFig)(?<!\bDr)(?<!\bMr)"
                  r"(?<!\bSt)(?<!\bapprox)(?<![\s(][A-Za-z])(?<!\bcf)(?<!\bEq)"
                  r"([.!?])\s+(?=<img class=\"(?:im|dvi)\"|<em>|<strong>|[A-Z(\[])")


def split_sentences(text):
    out, start = [], 0
    for m in _END.finditer(text):
        out.append(text[start:m.start() + 1])
        start = m.end()
    out.append(text[start:])
    return [s for s in out if s.strip()]


def _chunks(text, limit=235):
    sents = split_sentences(text)
    if len(sents) < 2:
        return [text]
    groups, cur = [], ""
    for s in sents:
        if cur and _weight(cur) + _weight(s) > limit:
            groups.append(cur)
            cur = s
        else:
            cur = (cur + " " + s).strip()
    if cur:
        groups.append(cur)
    # never leave a one-word orphan block at the end
    if len(groups) > 1 and _weight(groups[-1]) < 38:
        groups[-2] += " " + groups.pop()
    return groups


# ---------------------------------------------------------------- labelled sub-parts
_PLAIN_LAB = (r"(?:Example|Another(?: example)?|Check|Verification|Proof|Solution|Remark|Conclusion|Note|"
              r"Method|Why it works|Steps|Result|Answer|Interpretation|Meaning|Geometrically|In words)")
_SUB_SPLIT = re.compile(r"(?<=[.!?:;)>])\s+(?=(?:<em>[A-Z][^<>]{1,30}[.:]</em>|<em>[A-Z][^<>]{1,30}</em>[.:]|<em>(?:Geometrically|Algebraically|Physically|Graphically|Intuitively)</em>,|" + _PLAIN_LAB + r"\b[^<.:]{0,22}:)\s)")
_LEAD_EM = re.compile(r"^<em>([A-Z][^<>]{1,30}?)[.:]?</em>[.:,]?\s*")
_LEAD_PLAIN = re.compile(r"^(" + _PLAIN_LAB + r"\b[^<.:]{0,22}):\s*")


def _label(part):
    m = _LEAD_EM.match(part) or _LEAD_PLAIN.match(part)
    if not m:
        return part, False
    return '<span class="sl">%s</span> %s' % (m.group(1), part[m.end():]), True


_PARA = re.compile(r'<p(?: class="hm")?>((?:(?!</p>).)*)</p>', re.S)
_SKIP = ('class="opts', 'class="parts', 'class="part"', 'class="opt"', 'class="fxs', 'ansline', "<table")


def structure_prose(htm):
    def one(m):
        inner = m.group(1)
        if any(s in inner for s in _SKIP) or _weight(inner) < 175:
            return m.group(0)
        pieces = [p for p in _SUB_SPLIT.split(inner) if p.strip()]
        lead = ""
        blocks = []
        for k, piece in enumerate(pieces):
            piece, labelled = (_label(piece) if k else (piece, False))
            if _weight(piece) >= 270:
                cs = _chunks(piece)
            else:
                cs = [piece]
            for j, c in enumerate(cs):
                cls = ' class="ck"' if (j > 0) else (' class="sub"' if labelled else "")
                blocks.append("<p%s>%s</p>" % (cls, c.strip()))
        if len(blocks) < 2:
            return m.group(0)
        new = "".join(blocks)
        if not all(_balanced(b) for b in blocks):
            return m.group(0)
        return new
    return _PARA.sub(one, htm)


# ---------------------------------------------------------------- tall formulas on their own line
_TALL_IMG = re.compile(r'<img data-t="([^"]*)" class="im" data-w="([0-9.]+)" src="[^"]*" style="[^"]*" alt="math">')
_BLOCK = re.compile(r'<(p|li)(?: class="hm")?>((?:(?!</\1>).)*?data-t=.*?)</\1>', re.S)
_NOPROMOTE = ('class="opts', 'class="parts', 'class="part"', 'class="opt"', 'class="fxs', "ansline", "<table")


def promote_tall(htm):
    import md2html as M

    cur = {"tag": "p"}

    def img(m):
        if float(m.group(2)) < (27 if cur["tag"] == "p" else 40):
            return m.group(0)
        tex = _html.unescape(m.group(1))
        big = M._math_img(tex, 11.4, display=True, cls="dvi", derive_min=1)
        return '<span class="dv">%s</span>' % big if big else m.group(0)

    def blk(m):
        tag, inner = m.group(1), m.group(2)
        cur["tag"] = tag
        if any(s in inner for s in _NOPROMOTE):
            return m.group(0)
        text = _TAGS.sub("", re.sub(r"<img[^>]*>", "", inner)).strip()
        if len(text) < 10:
            return m.group(0)
        new = _TALL_IMG.sub(img, inner)
        return "<%s>%s</%s>" % (tag, new, tag)

    htm = _BLOCK.sub(blk, htm)
    return re.sub(r' data-t="[^"]*"', "", htm)


# ---------------------------------------------------------------- worked examples as steps
_STEPBOX = re.compile(r'class="box (?:example|derivation)"')


def example_steps(htm):
    import md2html as M

    def para(m):
        inner = m.group(1)
        if "class=\"dv\"" in inner or "fxs" in inner or "opts" in inner:
            return m.group(0)
        run = M._label_run(inner)
        if run:
            stem = inner[:run[0].start()].rstrip()
            opts = [inner[run[i].end():(run[i + 1].start() if i + 1 < len(run) else len(inner))].strip()
                    for i in range(len(run))]
            if not all(opts):
                return m.group(0)
            rows = "".join('<span class="part"><i>(%s)</i> %s</span>' % (r.group(1), M._sentences(o))
                           for r, o in zip(run, opts))
            return '<p class="hm">%s<span class="parts">%s</span></p>' % (stem, rows)
        body = M._sentences(inner)
        if body == inner:
            return m.group(0)
        return '<p class="hm"><span class="stps">%s</span></p>' % body

    toks = re.split(r"(<div\b[^>]*>|</div>)", htm)
    stack, out = [], []
    for t in toks:
        if t.startswith("<div"):
            stack.append(bool(_STEPBOX.search(t)))
        elif t == "</div>":
            if stack:
                stack.pop()
        elif any(stack):
            t = re.sub(r'<p(?: class="hm")?>((?:(?!</p>).)*)</p>', para, t, flags=re.S)
        out.append(t)
    return "".join(out)


# ---------------------------------------------------------------- short-value tables
def align_tables(htm):
    def tbl(m):
        t = m.group(0)
        if 'class="' in t[:40]:
            return t
        rows = re.findall(r"<tr>(.*?)</tr>", t, re.S)
        if len(rows) < 3:
            return t
        worst, cols = 0, 0
        for r in rows:
            cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S)
            cols = max(cols, len(cells))
            for c in cells[1:]:
                worst = max(worst, _weight(c))
        if cols >= 4 and worst <= 30:
            return t.replace("<table", '<table class="ctr"', 1)
        return t
    return re.sub(r"<table\b.*?</table>", tbl, htm, flags=re.S)


def sheet_paragraphs(htm):
    """A paragraph that holds a formula sheet stays whole, so its title never strands on the previous page."""
    return re.sub(r'<p(?: class="hm")?>((?:(?!</p>).)*?<span class="fxs.*?)</p>',
                  lambda m: '<p class="fxp">%s</p>' % m.group(1), htm, flags=re.S)


_LEADONLY = re.compile(r'<p>((?:<strong>[^<]{2,90}</strong>|<em>[^<]{2,90}</em>|[^<]{3,90}:|[^<]{2,60}:\s*<span[^>]*>[^<]*</span>)\s*)</p>(?=\s*<(?:p class="fxp"|table|figure|div class="(?:dm|hk)"|ol|ul|span class="fxs))')


def keep_with_next(htm):
    """A line that only introduces what follows (a bold lead, 'Laws:') never ends a page."""
    htm = _LEADONLY.sub(lambda m: '<p class="kn">%s</p>' % m.group(1), htm)
    # a label paragraph followed by a table whose rows are all kept together
    return htm
