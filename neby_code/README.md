# Neby Code local daemon

Run from the repository root using the command shown by the **Connect local machine** dialog in `/code/`.

```bash
python -m pip install -r neby_code/requirements.txt
python -m neby_code --workspace . --ws-url "wss://.../ws/" --ticket "..."
```

The daemon exposes only the selected workspace to your authenticated Neby Code session and keeps file operations and command execution on your machine.
