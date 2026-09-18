# 📦 How to Sync & Export Files to NEBians Server

You can upload and sync your code modifications or generated assets directly back to our server using terminal commands or Python scripts.

---

### 🔑 Endpoint & Credentials
* **Upload URL:** `https://nebians.consica.com.np/api/agent-drop/upload/`
* **Auth Header:** `X-Agent-Token: <AGENT_DROP_SECRET from server .env - ask an admin, never commit it>`
* **Alternative Auth:** `Authorization: Bearer <secret>` (prefer the header; avoid `?token=` URLs - they land in logs)

---

### 🚀 Upload Methods

#### Option 1: Zip & Upload Entire Project (Recommended)
Bundle the workspace and upload in a single command (excluding cache/git noise):

```bash
zip -r build.zip . -x "node_modules/*" -x ".git/*" -x "__pycache__/*" -x "*.pyc" -x ".venv/*"

curl -X POST "https://nebians.consica.com.np/api/agent-drop/upload/" \
  -H "X-Agent-Token: $AGENT_DROP_SECRET" \
  -F "file=@build.zip"
```

---

#### Option 2: Upload a Single Modified File (Preserving Relative Path)
Upload individual files while preserving their path inside the project tree:

```bash
curl -X POST "https://nebians.consica.com.np/api/agent-drop/upload/" \
  -H "X-Agent-Token: $AGENT_DROP_SECRET" \
  -F "path=web/templates/web/canvas.html" \
  -F "file=@web/templates/web/canvas.html"
```

---

#### Option 3: Python Script (Auto-Scan & Upload All Code as JSON)
A standalone script to automatically collect all project files and push them directly:

```python
import os
import requests

URL = "https://nebians.consica.com.np/api/agent-drop/upload/"
TOKEN = os.environ["AGENT_DROP_SECRET"]  # export AGENT_DROP_SECRET=<secret from an admin>

IGNORED_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".idea", ".vscode"}
IGNORED_EXTS = {".pyc", ".pyo", ".zip", ".tar.gz", ".png", ".jpg", ".jpeg"}

files_payload = {}

for root, dirs, filenames in os.walk("."):
    dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
    for fname in filenames:
        if any(fname.endswith(ext) for ext in IGNORED_EXTS):
            continue
        full_path = os.path.join(root, fname)
        rel_path = os.path.relpath(full_path, ".").replace("\\", "/")
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                files_payload[rel_path] = f.read()
        except Exception:
            pass

response = requests.post(
    URL,
    headers={"X-Agent-Token": TOKEN},
    json={"files": files_payload},
    timeout=60,
)

print("Status:", response.status_code)
print("Response:", response.json())
```

---

### 📥 Server Response Format
On successful upload, the server returns a JSON response containing a unique `batch_id`:

```json
{
  "status": "ok",
  "batch_id": "20260823_173000_a1b2c3",
  "file_count": 14,
  "files": [
    "web/templates/web/canvas.html",
    "web/static/web/js/canvas/agent.js"
  ],
  "batch_id": "20260823_173000_a1b2c3",
  "file_count": 14
}
```

Staff can download batches from the staff-only page (`/staff/agent-drops/`, Django staff login required); API downloads accept the same `X-Agent-Token` header.
