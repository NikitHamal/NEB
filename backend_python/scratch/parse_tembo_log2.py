import re, sys
sys.stdout.reconfigure(encoding='utf-8')

log_path = r'E:\Downloads\sandbox-logs-1781172865596.txt'
with open(log_path, encoding='utf-8', errors='replace') as f:
    content = f.read()

events = content.split('\n---\n')
stdout_msgs = []
for ev in events:
    if '[stdout]' in ev and 'environmentType' in ev:
        # Find the result string
        m = re.search(r'"result":\s*"(.*?)"(?:,\s*"command"|,\s*"environment|\})', ev, re.DOTALL)
        if m:
            msg = m.group(1).encode('raw_unicode_escape').decode('unicode_escape', errors='replace')
            stdout_msgs.append(msg.strip()[:300])

print(f'Total stdout messages: {len(stdout_msgs)}')
for i, msg in enumerate(stdout_msgs):
    print(f'[{i+1}] {msg}')
    print()
