"""Fetch a published paper page: OCR text (draft only) + page images into a scratch cache (never committed)."""
import sys, re, os, json, html, requests
CACHE = os.environ.get("PAPER_CACHE", "/tmp/psrc")
UA = {"User-Agent": "Mozilla/5.0"}

def body_text(h):
    m = re.search(r"<div class=.post-body[^>]*>(.*?)<div class=.post-footer", h, re.S) or re.search(r"<article.*?</article>", h, re.S)
    b = m.group(1) if m else h
    imgs = [u for u in re.findall(r'<img[^>]+src="(https://blogger[^"]+)"', b)]
    b = re.sub(r"<script.*?</script>|<style.*?</style>", "", b, flags=re.S)
    b = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</h\d>", "\n", b)
    t = html.unescape(re.sub(r"<[^>]+>", "", b)).replace("\xa0", " ")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip(), imgs

def fetch(url, key):
    d = os.path.join(CACHE, key); os.makedirs(d, exist_ok=True)
    h = requests.get(url, headers=UA, timeout=40).text
    t, imgs = body_text(h)
    open(os.path.join(d, "ocr.txt"), "w").write(t)
    seen = []
    for u in imgs:
        if u not in seen: seen.append(u)
    out = []
    for i, u in enumerate(seen):
        p = os.path.join(d, f"p{i}.jpg")
        if not os.path.exists(p):
            r = requests.get(u.replace("/s16000-rw/", "/s1600/"), headers=UA, timeout=60)
            open(p, "wb").write(r.content)
        out.append(p)
    json.dump({"url": url, "images": out}, open(os.path.join(d, "meta.json"), "w"))
    return t, out

if __name__ == "__main__":
    t, o = fetch(sys.argv[1], sys.argv[2]); print(len(t), "chars", len(o), "images")
