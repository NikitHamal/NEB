import io
import math


def mult(a, b):
    return [
        a[0] * b[0] + a[1] * b[2],
        a[0] * b[1] + a[1] * b[3],
        a[2] * b[0] + a[3] * b[2],
        a[2] * b[1] + a[3] * b[3],
        a[4] * b[0] + a[5] * b[2] + b[4],
        a[4] * b[1] + a[5] * b[3] + b[5],
    ]


def mat_scale(m):
    d = abs(m[0] * m[3] - m[1] * m[2])
    return math.sqrt(d) if d > 1e-9 else 0.0


def _hex_color(rgb):
    def cl(v):
        v = max(0.0, min(1.0, float(v)))
        return int(round(v * 255))
    r, g, b = rgb
    return "#%02X%02X%02X" % (cl(r), cl(g), cl(b))


def _style_flags(font_dict):
    name = ""
    try:
        if font_dict is not None:
            bf = font_dict.get("/BaseFont")
            if bf is not None:
                name = str(bf).split("+")[-1].lower()
            else:
                fd = font_dict.get("/FontDescriptor")
                if fd is not None:
                    nm = fd.get("/FontName")
                    if nm is not None:
                        name = str(nm).split("+")[-1].lower()
    except Exception:
        name = ""
    bold = any(k in name for k in ("bold", "black", "heavy", "-bd"))
    italic = any(k in name for k in ("italic", "oblique"))
    return bold, italic, name


class FillState:
    def __init__(self):
        self.rgb = (0.0, 0.0, 0.0)

    def apply(self, op, operands):
        vals = []
        for o in operands:
            try:
                vals.append(float(o))
            except Exception:
                return
        if op == "rg" and len(vals) >= 3:
            self.rgb = (vals[0], vals[1], vals[2])
        elif op == "g" and len(vals) >= 1:
            self.rgb = (vals[0], vals[0], vals[0])
        elif op == "k" and len(vals) >= 4:
            c, m, y, k = vals[:4]
            self.rgb = ((1 - c) * (1 - k), (1 - m) * (1 - k), (1 - y) * (1 - k))
        elif op in ("sc", "scn"):
            if len(vals) == 1:
                self.rgb = (vals[0], vals[0], vals[0])
            elif len(vals) == 3:
                self.rgb = (vals[0], vals[1], vals[2])
            elif len(vals) >= 4:
                c, m, y, k = vals[0], vals[1], vals[2], vals[3]
                self.rgb = ((1 - c) * (1 - k), (1 - m) * (1 - k), (1 - y) * (1 - k))

    @property
    def hex(self):
        return _hex_color(self.rgb)


def _clean(text):
    if not text:
        return ""
    return text.replace("\r", " ").replace("\n", " ").replace("\t", " ")


MAX_DOC_IMAGES = 120
MAX_PAGE_IMAGES = 40


def extract_pdf(data):
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    if getattr(reader, "is_encrypted", False):
        try:
            reader.decrypt("")
        except Exception:
            raise ValueError("This PDF is password protected")
    meta_title = ""
    try:
        if reader.metadata and getattr(reader.metadata, "title", None):
            meta_title = str(reader.metadata.title)[:160]
    except Exception:
        pass

    pages_out = []
    total_runs = 0
    skipped_rotated = 0
    for pageno, page in enumerate(reader.pages):
        mb = page.mediabox
        pw = float(mb.width)
        ph = float(mb.height)
        fill = FillState()
        raw_runs = []
        do_events = []

        image_names = set()
        try:
            res = page.get("/Resources")
            xo = res.get("/XObject") if res is not None else None
            if xo is not None:
                for nm, ref in xo.items():
                    try:
                        obj = ref.get_object()
                        st = obj.get("/Subtype")
                        if st is not None and str(st) == "/Image":
                            image_names.add(str(nm))
                    except Exception:
                        continue
        except Exception:
            image_names = set()

        def op_visitor(operator, operands, cm, tm):
            op = operator.decode("latin-1") if isinstance(operator, (bytes, bytearray)) else str(operator)
            if op in ("rg", "g", "k", "sc", "scn"):
                fill.apply(op, operands)
            elif op == "Do" and operands:
                name = str(operands[0])
                if name in image_names and len(do_events) < MAX_PAGE_IMAGES:
                    do_events.append({"name": name, "cm": list(cm)})

        def text_visitor(text, cm, tm, font_dict, font_size):
            nonlocal skipped_rotated, total_runs
            clean = _clean(text)
            if not clean.strip():
                return
            m = mult(tm, cm)
            sc = mat_scale(m)
            if sc < 0.05:
                return
            x = float(m[4]) - float(mb.left)
            y = ph - (float(m[5]) - float(mb.bottom))
            size = float(font_size or 0) * sc
            if size < 0.5 or size > 400:
                return
            denom = math.hypot(m[0], m[1])
            if denom > 1e-6 and abs(m[1]) / denom > 0.08:
                skipped_rotated += 1
                return
            bold, italic, fname = _style_flags(font_dict)
            raw_runs.append({
                "t": clean,
                "x": x,
                "y": y,
                "size": size,
                "color": fill.hex,
                "bold": bold,
                "italic": italic,
                "font": fname,
            })
            total_runs += 1

        try:
            page.extract_text(
                visitor_operand_before=op_visitor,
                visitor_text=text_visitor,
            )
        except Exception:
            pass

        lines = _assemble_lines(raw_runs)
        images = []
        for ev in do_events:
            cmx = ev["cm"]
            xs, ys = [], []
            for px, py in ((0, 0), (1, 0), (0, 1), (1, 1)):
                ex = px * cmx[0] + py * cmx[2] + cmx[4]
                ey = px * cmx[1] + py * cmx[3] + cmx[5]
                xs.append(ex - float(mb.left))
                ys.append(ph - (ey - float(mb.bottom)))
            x0, x1 = min(xs), max(xs)
            yt, yb = min(ys), max(ys)
            if x1 - x0 < 4 or yb - yt < 4:
                continue
            if len(images) < MAX_PAGE_IMAGES:
                images.append({
                    "name": ev["name"],
                    "x": x0,
                    "y_top": yt,
                    "w": x1 - x0,
                    "h": yb - yt,
                })
        pages_out.append({
            "idx": pageno,
            "w": pw,
            "h": ph,
            "lines": lines,
            "images": images,
            "decode_names": list(image_names),
        })

    def resolver_factory(page_obj):
        cache = {}

        def resolve(name):
            if name in cache:
                return cache[name]
            out = None
            try:
                wanted = name.lstrip("/").lower()
                for img in page_obj.images:
                    nm = str(img.name).lstrip("/")
                    low = nm.lower()
                    for extn in (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".gif", ".jpx", ".jp2"):
                        if low.endswith(extn):
                            low = low[: -len(extn)]
                            break
                    if low == wanted or nm.lower() == wanted or low.endswith(wanted) or wanted.endswith(low):
                        out = img.image
                        break
            except Exception:
                out = None
            cache[name] = out
            return out

        return resolve

    for rec, page_obj in zip(pages_out, reader.pages):
        rec["resolve_image"] = resolver_factory(page_obj)

    return {
        "title": meta_title,
        "pages": pages_out,
        "total_runs": total_runs,
        "skipped_rotated": skipped_rotated,
    }


def _assemble_lines(raw_runs):
    if not raw_runs:
        return []
    runs = sorted(raw_runs, key=lambda r: (-round(r["y"], 1), r["x"]))
    clusters = []
    for r in runs:
        tol = max(2.2, r["size"] * 0.38)
        placed = False
        for cl in clusters[-8:]:
            if abs(cl["anchor"] - r["y"]) <= tol:
                cl["items"].append(r)
                cl["anchor"] = sum(it["y"] for it in cl["items"]) / len(cl["items"])
                placed = True
                break
        if not placed:
            clusters.append({"anchor": r["y"], "items": [r]})
    clusters.sort(key=lambda c: -c["anchor"])

    out = []
    for cl in clusters:
        items = sorted(cl["items"], key=lambda r: r["x"])
        merged = []
        for it in items:
            it_end = it["x"] + len(it["t"]) * it["size"] * 0.52
            if merged:
                prev = merged[-1]
                gap = it["x"] - prev["_end"]
                same_style = (
                    prev["bold"] == it["bold"]
                    and prev["italic"] == it["italic"]
                    and prev["color"] == it["color"]
                    and abs(prev["size"] - it["size"]) < 0.4
                )
                if gap <= max(1.2, prev["size"] * 0.34) and same_style:
                    prev["t"] += it["t"]
                    prev["_end"] = it_end
                    continue
            rec = dict(it)
            rec["_end"] = it_end
            rec["gap_before"] = (it["x"] - merged[-1]["_end"]) if merged else None
            merged.append(rec)
        if not merged:
            continue
        segs = []
        tabs = []
        first = True
        for it in merged:
            is_tab = False
            if not first and it["gap_before"] is not None:
                is_tab = it["gap_before"] > it["size"] * 2.6
            if is_tab:
                tabs.append(round(it["x"], 1))
            segs.append({
                "t": it["t"],
                "color": it["color"],
                "bold": it["bold"],
                "italic": it["italic"],
                "size": it["size"],
                "tab_before": is_tab,
            })
            first = False
        sizes = [m["size"] for m in merged]
        out.append({
            "y": cl["anchor"],
            "x": merged[0]["x"],
            "right_est": merged[-1]["_end"],
            "size": max(set(sizes), key=sizes.count),
            "segs": segs,
            "tabs": tabs,
        })
    return out