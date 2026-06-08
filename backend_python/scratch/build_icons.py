"""Generate squircle favicon set for NEBians.

Source: existing n-logo-512.png (a 512x512 RGBA squircle with white background
and the blue N logo composited on top).

Outputs (all overwritten in-place):
    web/static/web/img/n-logo-1024.png
    web/static/web/img/n-logo-512.png
    web/static/web/img/n-logo-192.png
    web/static/web/img/n-logo-180.png
    web/static/web/img/n-logo-48.png
    web/static/web/img/n-logo-32.png
    web/static/web/img/n-logo-16.png
    web/static/web/img/favicon.ico     (multi-size: 16, 32, 48)

After running, also copies favicon.ico to public/favicon.ico so LiteSpeed
serves it at the site root (/favicon.ico) where browsers and Googlebot look.
"""

import os
import shutil
from PIL import Image


IMG_DIR = r"F:\NEB\backend_python\web\static\web\img"
PUBLIC_DIR = r"F:\NEB\backend_python\public"


def create_squircle_icon(src_path, dest_path, size, radius_pct=0.22):
    """Resize a transparent logo onto a white squircle canvas of `size`x`size`."""
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source not found: {src_path}")

    logo = Image.open(src_path).convert("RGBA")
    logo = logo.resize((size, size), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    from PIL import ImageDraw
    d = ImageDraw.Draw(draw)
    radius = max(1, int(size * radius_pct))
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=(255, 255, 255, 255))
    canvas.alpha_composite(draw)
    canvas.alpha_composite(logo)
    canvas.save(dest_path, "PNG", optimize=True)
    print(f"  wrote {os.path.basename(dest_path)} ({size}x{size})")


def build_favicon_ico(src_path, dest_path, sizes=(16, 32, 48)):
    """Build a multi-resolution favicon.ico from a high-res source PNG."""
    base = Image.open(src_path).convert("RGBA")
    frames = []
    for s in sizes:
        f = base.resize((s, s), Image.Resampling.LANCZOS)
        frames.append(f)
    base.save(
        dest_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=frames[1:],
    )
    print(f"  wrote {os.path.basename(dest_path)} (sizes={list(sizes)})")


def main():
    # Pick the highest-res squircle source we have
    for candidate in ("n-logo-1024.png", "n-logo-512.png"):
        src = os.path.join(IMG_DIR, candidate)
        if os.path.exists(src):
            break
    else:
        raise FileNotFoundError("No high-res source logo found in img/")

    print(f"Source: {src}")
    print(f"Image dir: {IMG_DIR}")
    print()

    # Regenerate all raster sizes from the source
    targets = [
        ("n-logo-1024.png", 1024),
        ("n-logo-512.png", 512),
        ("n-logo-192.png", 192),
        ("n-logo-180.png", 180),
        ("n-logo-48.png", 48),
        ("n-logo-32.png", 32),
        ("n-logo-16.png", 16),
    ]
    print("PNG outputs:")
    for filename, size in targets:
        create_squircle_icon(src, os.path.join(IMG_DIR, filename), size)

    # Build multi-size favicon.ico
    print()
    print("ICO output:")
    build_favicon_ico(os.path.join(IMG_DIR, "n-logo-512.png"),
                      os.path.join(IMG_DIR, "favicon.ico"),
                      sizes=(16, 32, 48))

    # Copy favicon.ico to public/ root so /favicon.ico resolves at site root
    public_favicon = os.path.join(PUBLIC_DIR, "favicon.ico")
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    shutil.copy2(os.path.join(IMG_DIR, "favicon.ico"), public_favicon)
    print()
    print(f"Copied favicon.ico to: {public_favicon}")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
