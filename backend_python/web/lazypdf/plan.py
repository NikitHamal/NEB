TOP_MARGIN = 30.0
BOTTOM_MARGIN = 26.0
LH_RATIO = 1.18

import math


def build_plan(extracted, max_pages):
    pages_in = extracted["pages"][:max_pages]
    truncated = len(extracted["pages"]) > max_pages
    xs = []
    for pg in pages_in:
        for ln in pg["lines"]:
            if 0 <= ln["x"] < pg["w"]:
                xs.append(ln["x"])
    doc_left = min(xs) if xs else 28.0
    if doc_left > 90:
        doc_left = 28.0

    planned = []
    for pg in pages_in:
        rec = _plan_page(pg, doc_left)
        planned.append(rec)

    return {
        "title": extracted.get("title") or "",
        "doc_left": round(doc_left, 1),
        "pages": planned,
        "truncated": truncated,
        "total_runs": extracted.get("total_runs", 0),
        "skipped_rotated": extracted.get("skipped_rotated", 0),
    }


def _plan_page(pg, doc_left):
    lines = sorted(pg["lines"], key=lambda l: -l["y"])
    for i, ln in enumerate(lines):
        indent = max(0.0, ln["x"] - doc_left)
        ln["indent"] = round(indent, 1)
        ln["lh"] = round(ln["size"] * LH_RATIO, 2)
        ln["space_before"] = 0.0
        ln["space_after"] = 0.0
        ln["center"] = False
        ln["tabs_rel"] = [round(t - doc_left, 1) for t in ln["tabs"]]
        w_page_center = pg["w"] / 2.0
        line_mid = (ln["x"] + ln["right_est"]) / 2.0
        line_w = ln["right_est"] - ln["x"]
        if (
            abs(line_mid - w_page_center) < max(6.0, pg["w"] * 0.02)
            and line_w < pg["w"] * 0.72
            and i == 0
            or (abs(line_mid - w_page_center) < max(4.0, pg["w"] * 0.015) and line_w < pg["w"] * 0.5)
        ):
            ln["center"] = True

    n = len(lines)
    gap_total = 0.0
    for i in range(n - 1):
        g = lines[i]["y"] - lines[i + 1]["y"]
        sa = g - lines[i]["lh"]
        if sa < -lines[i]["lh"] * 0.30:
            sa = 0.0
        sa = min(sa, 260.0)
        lines[i]["space_after"] = round(sa, 2)
        gap_total += lines[i]["lh"] + lines[i]["space_after"]
    if n:
        first = lines[0]
        top_off = first["y"]
        sb0 = top_off - TOP_MARGIN - first["lh"] * 0.86
        first["space_before"] = round(min(max(sb0, 0.0), 320.0), 2)

    need = gap_total + (lines[0]["space_before"] + lines[0]["lh"] if n else 0)
    avail = pg["h"] - TOP_MARGIN - BOTTOM_MARGIN
    fit_scale = None
    if need > avail * 1.02 and need > 0:
        k = avail / need
        if k >= 0.55:
            for ln in lines:
                ln["space_after"] = round(ln["space_after"] * k, 2)
            lines[0]["space_before"] = round(lines[0]["space_before"] * k, 2)
        else:
            fit_scale = max(0.72, min(0.82, math.sqrt(k)))
            for ln in lines:
                ln["size"] = round(ln["size"] * fit_scale, 1)
                ln["lh"] = round(ln["lh"] * fit_scale, 2)
                ln["space_after"] = round(ln["space_after"] * fit_scale, 2)
                ln["space_before"] = round(ln["space_before"] * fit_scale, 2)

    return {
        "idx": pg["idx"],
        "w": pg["w"],
        "h": pg["h"],
        "lines": lines,
        "images": pg["images"],
        "decode_names": pg.get("decode_names") or [],
        "resolve_image": pg.get("resolve_image"),
        "autofit": fit_scale is not None,
    }