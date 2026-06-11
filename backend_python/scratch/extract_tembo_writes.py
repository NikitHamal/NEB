import re, sys

log_path = r'E:\Downloads\sandbox-logs-1781172865596.txt'
with open(log_path, encoding='utf-8', errors='replace') as f:
    content = f.read()

events = content.split('\n---\n')
writes = []
for ev in events:
    if '[write]' in ev and 'environmentType' in ev:
        path_match = re.search(r'\[write\]\s+([^\n]+)', ev)
        if path_match:
            path = path_match.group(1).strip()
            if any(x in path for x in ['app/src', 'backend_python', '/api/', '.kt', '.py', '.html', '.js', '.css']):
                writes.append(path)

print(f'Total write events to source files: {len(writes)}')
for w in writes:
    print(w)
