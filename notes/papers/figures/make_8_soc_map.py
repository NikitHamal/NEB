"""Schematic outline map of Nepal for 8-soc-ble-2082-kathmandu Q20 (SVG, Devanagari labels shaped by WeasyPrint).
Outline is a hand-simplified polygon of the border (lon, lat); the two sites use real coordinates."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
BORDER = [(80.06,28.83),(80.25,29.2),(80.35,29.65),(80.2,29.95),(80.55,30.45),(81.1,30.2),(81.4,30.38),(81.85,30.33),
 (82.15,30.05),(82.6,29.75),(83.0,29.55),(83.45,29.35),(83.9,29.3),(84.2,29.05),(84.25,28.85),(84.7,28.6),(85.1,28.55),
 (85.15,28.3),(85.6,28.25),(85.95,27.95),(86.4,27.95),(86.75,28.1),(87.35,27.82),(87.85,27.9),(88.15,27.88),(88.1,27.3),
 (88.2,26.45),(87.75,26.4),(87.0,26.55),(86.0,26.62),(85.2,26.75),(84.65,27.0),(83.9,27.37),(83.3,27.38),(82.7,27.7),
 (82.1,28.15),(81.7,28.4),(81.3,28.15),(80.5,28.5)]
S = 100.0
def P(lon, lat): return (round(24 + (lon - 79.9) * S * 0.88, 1), round(40 + (30.6 - lat) * S, 1))
pts = " ".join("%s,%s" % P(*p) for p in BORDER)
sx, sy = P(86.925, 27.988); bx, by = P(85.362, 27.721)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 480" width="840" height="480" font-family="Noto Sans Devanagari, sans-serif">
<rect x="1" y="1" width="838" height="478" fill="#ffffff" stroke="#cfd5de" stroke-width="1.5" rx="10"/>
<polygon points="{pts}" fill="#eef3fb" stroke="#1f3a68" stroke-width="2.4" stroke-linejoin="round"/>
<polygon points="{sx},{sy-17} {sx-15},{sy+10} {sx+15},{sy+10}" fill="#c0392b" stroke="#7b241c" stroke-width="1.5"/>
<polygon points="{sx},{sy-17} {sx-4.5},{sy-8} {sx+4.5},{sy-8}" fill="#ffffff"/>
<line x1="{sx+4}" y1="{sy-14}" x2="{sx+40}" y2="{sy-42}" stroke="#333" stroke-width="1.2"/>
<g transform="translate({bx},{by})" fill="#f1c40f" stroke="#7d6608" stroke-width="1.4">
<path d="M-13,10 A13,12 0 0 1 13,10 Z"/><rect x="-3.5" y="-9" width="7" height="8" fill="#fff"/><polygon points="0,-24 -3.5,-9 3.5,-9" fill="#c0392b" stroke="#7b241c"/></g>
<line x1="{bx-6}" y1="{by+14}" x2="{bx-20}" y2="{by+34}" stroke="#333" stroke-width="1.2"/>
<g transform="translate(790,62)"><line x1="0" y1="30" x2="0" y2="-12" stroke="#14233f" stroke-width="3"/><polygon points="0,-24 -8,-8 8,-8" fill="#14233f"/></g>
<rect x="600" y="150" width="214" height="88" rx="8" fill="#ffffff" stroke="#1f3a68" stroke-width="1.4"/>
<polygon points="624,200 612,221 636,221" fill="#c0392b" stroke="#7b241c" stroke-width="1.2"/>
<g transform="translate(722,212)" fill="#f1c40f" stroke="#7d6608" stroke-width="1.2"><path d="M-11,8 A11,10 0 0 1 11,8 Z"/><polygon points="0,-20 -3,-7 3,-7" fill="#c0392b" stroke="#7b241c"/></g>
</svg>'''
open(os.path.join(HERE, "8-soc-ble-2082-q20-map.svg"), "w", encoding="utf-8").write(svg)
import base64
K = 140.0 / 840  # mm per svg unit
def lab(cx, y, txt, size=17, bold=False, color="#222", w=220):
    return ('<div style="position:absolute; left:%.2fmm; top:%.2fmm; width:%.2fmm; text-align:center; font-size:%.2fmm; line-height:1.15; color:%s; font-weight:%s; font-family:\'Noto Sans Devanagari\', sans-serif;">%s</div>'
            % ((cx - w / 2) * K, (y - size * 1.05) * K, w * K, size * K, color, "700" if bold else "400", txt))
L = []
L.append(lab(420, 30, "नेपालको रेखाचित्र", 21, True, "#14233f"))
L.append(lab(440, 86, "चीन (तिब्बत)", 17, False, "#6b7585"))
L.append(lab(520, 468, "भारत", 17, False, "#6b7585"))
L.append(lab(150, 360, "भारत", 17, False, "#6b7585"))
L.append(lab(sx + 55, sy - 46, "सगरमाथा हिमाल", 17, True, "#14233f", 220))
L.append(lab(bx - 20, by + 56, "बौद्धनाथ स्तुपा", 17, True, "#14233f", 220))
L.append(lab(790, 114, "उत्तर", 17, False, "#14233f", 80))
L.append(lab(707, 173, "सङ्केत", 17, True, "#14233f", 200))
L.append(lab(668, 216, "हिमाल", 16, False, "#222", 80))
L.append(lab(786, 216, "स्तुपा", 16, False, "#222", 80))
b64 = base64.b64encode(svg.encode("utf-8")).decode()
html = ('<div style="position:relative; width:140mm; height:80mm; margin:0 auto;"><img src="data:image/svg+xml;base64,%s" style="position:absolute; left:0; top:0; width:140mm; height:80mm;" alt="map">%s</div>'
        % (b64, "".join(L)))
open(os.path.join(HERE, "8-soc-ble-2082-q20-map.html"), "w", encoding="utf-8").write(html)
print("written")
