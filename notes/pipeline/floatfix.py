"""Close the white holes that unbreakable blocks (figures, photo plates, short tables, cards)
leave at the foot of a page.

WeasyPrint has no page floats. When a figure does not fit under the text above it, the whole
figure moves to the next page and the space it would have used stays empty. Print typesetters
solve this by floating the figure: the text that follows it fills the hole and the figure lands
after that text. This module does exactly that on the parsed document:

  1. render, then for every page measure the free band above the foot;
  2. if the next page opens with an unbreakable block, move that block after the following
     paragraphs (never past a heading, a second unbreakable block or the chapter end) until
     they cover the hole;
  3. render again and keep the arrangement only if the hole total went down.

Up to PASSES rounds. Reading order and anchors are untouched, only the block moves down by a
paragraph or two, as a float does in a printed book.
"""
import copy

MM = 96 / 25.4                      # WeasyPrint lengths are CSS px
ATOMIC = {"figure", "table", "div"}
HEADS = {"h1", "h2", "h3", "h4"}
MIN_GAP = 22 * MM                   # holes smaller than this are ordinary ragged page ends
PASSES = 5
SPLIT_GAP = 30 * MM                 # a hole this big justifies splitting a card or short table
DEBUG = False


def _walk(box):
    yield box
    for c in getattr(box, "children", ()) or ():
        yield from _walk(c)


def _is_chapter(el):
    return el.tag == "section" and "chapter" in (el.get("class") or "").split()


def _atomic(el):
    if el.tag not in ATOMIC:
        return False
    cls = (el.get("class") or "").split()
    return not ({"ch-head", "syllabus", "ch-chips"} & set(cls))


def _splittable(el):
    cls = (el.get("class") or "").split()
    if el.tag == "table":
        return True
    return el.tag == "div" and ("box" in cls or "hk" in cls)


def measure(doc):
    """-> (frags, limits). frags[page] = {element: (y0, y1)} for chapter-level blocks;
    limits[page] = (content_top, content_bottom)."""
    frags, limits, seen = [], [], set()
    for pg in doc.pages:
        pb = pg._page_box
        top = pb.content_box_y()
        limits.append((top, top + pb.height))
        d = {}
        for root in pb.children:
            for b in _walk(root):
                el = getattr(b, "element", None)
                if el is None or el in d:
                    continue
                if getattr(b, "margin_height", None) is None:
                    continue
                d[el] = (b.position_y, b.position_y + b.margin_height(), b)
        frags.append(d)
    return frags, limits


def _parents(root):
    return {c: p for p in root.iter() for c in p}


def _score(doc, parent):
    """Sum of the holes (px) above the foot, chapter ends excluded."""
    frags, limits = measure(doc)
    holes = []
    tops = []
    for i, (d, (t, bot)) in enumerate(zip(frags, limits)):
        blocks = [(y0, y1, el) for el, (y0, y1, _b) in d.items()
                  if parent.get(el) is not None and _is_chapter(parent[el])]
        tops.append(sorted(blocks, key=lambda x: x[0]))
    for i in range(len(frags) - 1):
        cur, nxt = tops[i], tops[i + 1]
        if not cur or not nxt:
            continue
        t, bot = limits[i]
        low = max(y1 for _y0, y1, _e in cur)
        gap = bot - low
        first = nxt[0][2]
        if gap < MIN_GAP:
            continue
        # a chapter opener on the next page: the short page is legitimate
        if any(e.tag == "div" and "ch-head" in (e.get("class") or "") for _a, _b, e in nxt[:2]):
            continue
        holes.append((i, gap, nxt))
    return holes, sum(h[1] for h in holes)


def _fix_once(doc, parent):
    holes, total = _score(doc, parent)
    frags, limits = measure(doc)
    moved = 0
    height = {}
    for d in frags:
        for e, (y0, y1, _b) in d.items():
            height[e] = height.get(e, 0.0) + (y1 - y0)
    for i, gap, nxt in holes:
        t1 = limits[i + 1][0]
        cand = None
        for y0, y1, el in nxt:
            if y1 - y0 < 4 * MM:          # empty anchor paragraphs
                continue
            cand = (y0, y1, el)
            break
        if cand is None:
            continue
        y0, y1, el = cand
        # must open the page and start here (not a continuation of a block from the page above)
        if y0 - t1 > 3 * MM or not _atomic(el) or el in frags[i]:
            if DEBUG: print('skip', i + 1, el.tag, el.get('class'), round((y0 - t1) / MM), el in frags[i])
            continue
        par = parent.get(el)
        if par is None or not _is_chapter(par):
            continue
        sibs = list(par)
        k = sibs.index(el)
        acc, fill, skipped, crossed = 0.0, [], 0, 0
        for s in sibs[k + 1:]:
            cls = (s.get("class") or "").split()
            if "ch-head" in cls or "chsum" in cls or "paper" in cls:
                break
            if s.tag in HEADS:
                # a plate may drift one section down when the hole is big; other blocks never cross
                if el.tag != "figure" or gap < 40 * MM or crossed or s.tag == "h1":
                    break
                crossed = 1
                fill.append(s)
                acc += height.get(s, 0.0)
                continue
            if s.tag in ("figure", "table") or "hk" in cls or "nobreak" in cls:
                skipped += 1
                if skipped > 2:
                    break
                continue
            h = height.get(s, 0.0)
            acc += h
            if h > 4 * MM:
                fill.append(s)
            if acc >= gap * 0.95:
                break
        while fill and fill[-1].tag in HEADS:
            fill.pop()
        if DEBUG: print('page', i + 1, 'gap', round(gap / MM), 'acc', round(acc / MM), len(fill))
        if not fill or acc < gap * 0.45:
            # nothing to pull up: let a tall card or short table split across the page break instead
            if gap >= SPLIT_GAP and _splittable(el) and not el.get("data-split"):
                el.set("data-split", "1")
                if el.tag == "table":
                    el.set("data-long", "1")
                moved += 1
            continue
        # the text moves up in front of the block: the block floats down past it
        at = list(par).index(el)
        for s in fill:
            par.remove(s)
        for j, s in enumerate(fill):
            par.insert(at + j, s)
        moved += 1
    return moved


def render_best(html, css, passes=PASSES, log=None):
    """Render `html` (weasyprint.HTML) with `css`; float unbreakable blocks to close holes."""
    root = html.etree_element
    parent = _parents(root)
    best = html.render(stylesheets=[css])
    best_score = _score(best, parent)[1]
    best_n = len(best.pages)
    best_tree = copy.deepcopy(root)
    for n in range(passes):
        if best_score <= 0:
            break
        if not _fix_once(best, parent):
            break
        trial = html.render(stylesheets=[css])
        parent = _parents(root)
        sc = _score(trial, parent)[1]
        if log:
            log(f"  floatfix pass {n + 1}: pages {best_n}->{len(trial.pages)} holes {best_score / MM / 247:.1f}->{sc / MM / 247:.1f} pg")
        if len(trial.pages) < best_n or (len(trial.pages) == best_n and sc < best_score * 0.92):
            best, best_score, best_n = trial, sc, len(trial.pages)
            best_tree = copy.deepcopy(root)
        else:
            root.clear()
            root.attrib.update(best_tree.attrib)
            root.text = best_tree.text
            for c in list(best_tree):
                root.append(c)
            parent = _parents(root)
            break
    return best
