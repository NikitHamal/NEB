import base64
import io
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from PIL import Image, ImageGrab
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False
    Image = None
    ImageGrab = None

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".neby", "images")


def ensure_cache_dir() -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    return CACHE_DIR


def grab_clipboard_image() -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    if not _PIL_AVAILABLE:
        return False, "Pillow library is not installed.", None

    try:
        data = ImageGrab.grabclipboard()
        if data is None:
            return False, "No image found in system clipboard. Copy an image first.", None

        if isinstance(data, list):
            for item in data:
                ext = Path(item).suffix.lower()
                if ext in SUPPORTED_EXTENSIONS and os.path.exists(item):
                    return load_image_from_path(item)
            return False, "Clipboard contains files, but none are supported images.", None

        if hasattr(data, "save"):
            ensure_cache_dir()
            ts = int(time.time() * 1000)
            file_path = os.path.join(CACHE_DIR, f"clipboard_{ts}.png")
            data.save(file_path, "PNG")
            return load_image_from_path(file_path)

        return False, "Unsupported clipboard image format.", None
    except Exception as exc:
        return False, f"Failed to grab clipboard image: {exc}", None


def load_image_from_path(file_path: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    path = os.path.abspath(os.path.expanduser(file_path.strip().strip("'\"")))
    if not os.path.exists(path):
        return False, f"Image file '{path}' does not exist.", None

    ext = Path(path).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return False, f"Unsupported image extension '{ext}'. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}", None

    try:
        with open(path, "rb") as f:
            raw_bytes = f.read()

        b64_data = base64.b64encode(raw_bytes).decode("utf-8")
        file_size_kb = len(raw_bytes) / 1024.0

        width, height = 0, 0
        mime_type = "image/png" if ext == ".png" else "image/jpeg" if ext in (".jpg", ".jpeg") else f"image/{ext[1:]}"

        if _PIL_AVAILABLE:
            try:
                with Image.open(io.BytesIO(raw_bytes)) as img:
                    width, height = img.size
            except Exception:
                pass

        info = {
            "path": path,
            "filename": os.path.basename(path),
            "extension": ext,
            "mime_type": mime_type,
            "width": width,
            "height": height,
            "size_kb": round(file_size_kb, 1),
            "base64": b64_data,
            "data_url": f"data:{mime_type};base64,{b64_data}",
        }
        return True, f"Loaded image '{os.path.basename(path)}' ({width}x{height}, {file_size_kb:.1f} KB)", info
    except Exception as exc:
        return False, f"Error reading image '{path}': {exc}", None


def list_images_in_dir(dir_path: str = ".", max_count: int = 20) -> List[str]:
    path = os.path.abspath(dir_path)
    if not os.path.exists(path):
        return []

    found = []
    for root, _, files in os.walk(path):
        if any(ignored in root for ignored in ("node_modules", ".git", "__pycache__", "venv")):
            continue
        for f in sorted(files):
            if Path(f).suffix.lower() in SUPPORTED_EXTENSIONS:
                found.append(os.path.join(root, f))
                if len(found) >= max_count:
                    return found
    return found


def render_ascii_preview(file_path: str, max_cols: int = 48) -> str:
    if not _PIL_AVAILABLE:
        return "[Image preview requires Pillow]"

    try:
        with Image.open(file_path) as img:
            img = img.convert("RGB")
            w, h = img.size
            if w <= 0 or h <= 0:
                return "[Invalid image dimensions]"

            aspect = h / float(w)
            target_cols = min(max_cols, w)
            target_rows = max(2, int(target_cols * aspect * 0.45))
            target_rows = target_rows if target_rows % 2 == 0 else target_rows + 1

            resized = img.resize((target_cols, target_rows), Image.Resampling.BILINEAR)
            pixels = resized.load()

            lines = []
            for y in range(0, target_rows, 2):
                row_str = ""
                for x in range(target_cols):
                    r_top, g_top, b_top = pixels[x, y]
                    if y + 1 < target_rows:
                        r_bot, g_bot, b_bot = pixels[x, y + 1]
                    else:
                        r_bot, g_bot, b_bot = 0, 0, 0
                    row_str += f"\033[38;2;{r_top};{g_top};{b_top}m\033[48;2;{r_bot};{g_bot};{b_bot}m▀\033[0m"
                lines.append(row_str)

            header = f"\n  [Image: {os.path.basename(file_path)} | {w}x{h} px | {target_cols}x{target_rows//2} terminal blocks]\n"
            return header + "\n".join("  " + l for l in lines) + "\n"
    except Exception as exc:
        return f"[Image preview unavailable: {exc}]"


def format_image_description(img_info: Dict[str, Any]) -> str:
    path = img_info.get("path", "image")
    filename = img_info.get("filename", os.path.basename(path))
    w = img_info.get("width", 0)
    h = img_info.get("height", 0)
    size = img_info.get("size_kb", 0)
    mime = img_info.get("mime_type", "image/png")

    return (
        f"Attached Image Reference:\n"
        f"- File: {filename}\n"
        f"- Path: {path}\n"
        f"- Dimensions: {w}x{h} px\n"
        f"- MIME: {mime}\n"
        f"- Size: {size} KB\n"
    )
