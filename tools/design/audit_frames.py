"""Sweep app pages for avatar frames with a stroke/outline/shadow and badges with a fill.
   python3 tools/design/audit_frames.py SESSIONID [base] [width]
Exit code 1 when anything is found. Needs playwright + a running dev server (see AGENTS.md)."""
import sys
from playwright.sync_api import sync_playwright

PATHS = ['/app/', '/app/forum/', '/app/forum/post/{post}/', '/app/profile/{user}/', '/app/forum/leaderboard/',
         '/app/requests/', '/app/library/', '/app/settings/', '/app/search/?q=a', '/app/notifications/',
         '/app/bookmarks/', '/app/news/', '/app/marketplace/']
JS = """() => {
  const out = [];
  const frames = [...document.querySelectorAll('[class*="avatar"],[data-shape],[data-avatar-seed]')];
  for (const e of frames) {
    const cs = getComputedStyle(e);
    if (!e.offsetWidth || e.matches('input,textarea,select,button,label,section,ul')) continue;
    const bw = Math.max(...['Top','Right','Bottom','Left'].map(s => cs['border'+s+'Style'] !== 'none' ? parseFloat(cs['border'+s+'Width']) : 0));
    const ow = cs.outlineStyle !== 'none' ? parseFloat(cs.outlineWidth) : 0;
    if (e.matches('[class*="badge"],.notif-dot,.epf-identity-camera,.pf-avatar-camera')) continue;
    const small = e.offsetWidth <= 160 && e.offsetHeight <= 160;
    if (small && (bw > 0 || ow > 0 || cs.boxShadow !== 'none')) out.push('FRAME ' + e.tagName + '.' + String(e.className).slice(0, 60) + ' border=' + bw + ' outline=' + ow + ' shadow=' + (cs.boxShadow !== 'none'));
  }
  const badges = [...document.querySelectorAll('.role-badge,.avatar-badge-overlay,.pf-verified,[class*="-badge"]:not(.notif-popup-badge):not(.notif-badge):not(.nav-badge)')];
  for (const e of badges) {
    if (!e.offsetWidth) continue;
    const cs = getComputedStyle(e);
    const bg = cs.backgroundColor;
    const filled = bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent';
    const bd = cs.borderTopStyle !== 'none' && parseFloat(cs.borderTopWidth) > 0;
    if (filled || bd) out.push('BADGE ' + e.tagName + '.' + String(e.className).slice(0, 60) + ' bg=' + bg + ' border=' + bd);
  }
  return out;
}"""

def main():
    sid = sys.argv[1]; base = sys.argv[2] if len(sys.argv) > 2 else 'http://127.0.0.1:8000'
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 1280
    import os, sqlite3
    post = user = ''
    try:
        con = sqlite3.connect(os.path.join(os.path.dirname(__file__), '..', '..', 'backend_python', 'db.sqlite3'))
        post = con.execute('select id from api_post limit 1').fetchone()[0]
        user = con.execute("select username from api_user where username='student_demo'").fetchone()[0]
    except Exception as ex:
        print('db lookup failed', ex)
    bad = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': width, 'height': 900})
        ctx.add_cookies([{'name': 'sessionid', 'value': sid, 'url': base}])
        pg = ctx.new_page()
        for path in PATHS:
            url = base + path.format(post=post, user=user)
            try:
                pg.goto(url, wait_until='networkidle', timeout=30000)
            except Exception as ex:
                print('skip', path, str(ex)[:60]); continue
            pg.wait_for_timeout(500)
            res = sorted(set(pg.evaluate(JS)))
            print(path, 'ok' if not res else '')
            for r in res:
                print('   ', r); bad += 1
        b.close()
    sys.exit(1 if bad else 0)

main()
