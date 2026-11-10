"""Session 32 helper: expands {{C:file}}, {{F:file}} and {{FIG:key|caption}} placeholders in a .tpl
into a content/<id>.md.  C and Fortran sources live in prog/ (every program was compiled and run).

    python3 gen_ct401.py ct401_shrawan.tpl ../../content/ioe-ct401-2082-shrawan.md
"""
import re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))

PRE = r"""
fig, ax = plt.subplots(figsize=(4.6, 4.4))
def B(x, y, t, k='p', w=2.2, h=0.7):
    if k == 'd':
        ax.add_patch(plt.Polygon([[x, y+h*0.8], [x+w*0.62, y], [x, y-h*0.8], [x-w*0.62, y]], fc='#fff3e0', ec='#b8860b'))
    elif k == 't':
        ax.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h, fc='#e0f0e6', ec='#2e8b57', lw=1.6))
    elif k == 'io':
        ax.add_patch(plt.Polygon([[x-w/2+0.2, y+h/2], [x+w/2+0.2, y+h/2], [x+w/2-0.2, y-h/2], [x-w/2-0.2, y-h/2]], fc='#e8eef7', ec='#1d6fb8'))
    else:
        ax.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h, fc='#e8eef7', ec='#1d6fb8'))
    ax.text(x, y, t, ha='center', va='center', fontsize=7.5)
def A(x1, y1, x2, y2, l=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', color='#14181f', lw=1))
    if l:
        ax.text((x1+x2)/2+0.12, (y1+y2)/2+0.1, l, fontsize=7, color='#d9534f')
def L(xs, ys):
    ax.plot(xs, ys, color='#14181f', lw=1)
"""
POST = "\nax.set_xlim(-2, 6.4); ax.set_ylim(%s, %s); ax.axis('off')\n"

FIGS = {
 'evenodd': (0.8, 7.6, r"""
B(0,7,'Start','t'); A(0,6.65,0,6.3)
B(0,5.9,'Read n','io'); A(0,5.55,0,5.15)
B(0,4.5,'n % 2 == 0 ?','d',w=2.6); A(0.85,4.5,2.1,4.5,'Yes'); A(0,3.9,0,3.15,'No')
B(3.1,4.5,'Print "Even"'); B(0,2.8,'Print "Odd"')
A(3.1,4.15,1.2,1.75); A(0,2.45,0.0,1.95)
B(0.0,1.6,'Stop','t')
"""),
 'sumn': (1.6, 9.1, r"""
B(0,8.7,'Start','t'); A(0,8.35,0,8.0)
B(0,7.6,'Read n','io'); A(0,7.25,0,6.9)
B(0,6.5,'sum = 0, i = 1'); A(0,6.15,0,5.75)
B(0,5.0,'i <= n ?','d',w=2.2); A(0.7,5.0,1.9,5.0,'Yes'); A(0,4.4,0,3.7,'No')
B(3.1,5.0,'sum = sum + i\ni = i + 1',w=2.2,h=0.8)
L([3.1,3.1],[5.4,5.75]); L([3.1,0],[5.75,5.75])
B(0,3.3,'Print sum','io'); A(0,2.95,0,2.3)
B(0,1.95,'Stop','t')
"""),
 'ladder': (0.9, 9.4, r"""
B(0,9,'Start','t'); A(0,8.65,0,8.45)
B(0,7.7,'cond 1 ?','d',w=2.0); B(3.0,7.7,'stmt 1'); A(0.62,7.7,1.9,7.7,'T'); A(0,7.0,0,6.75,'F')
B(0,6.0,'cond 2 ?','d',w=2.0); B(3.0,6.0,'stmt 2'); A(0.62,6.0,1.9,6.0,'T'); A(0,5.3,0,5.05,'F')
B(0,4.3,'cond 3 ?','d',w=2.0); B(3.0,4.3,'stmt 3'); A(0.62,4.3,1.9,4.3,'T'); A(0,3.6,0,3.35,'F')
B(0,3.0,'else: stmt 4')
for y in (7.7,6.0,4.3): L([4.1,5.0],[y,y])
L([1.1,5.0],[3.0,3.0]); L([5.0,5.0],[7.7,1.9]); A(5.0,1.9,2.7,1.5)
B(1.6,1.4,'Stop','t')
"""),
 'nested': (1.0, 8.9, r"""
B(0,8.5,'Start','t'); A(0,8.15,0,7.85)
B(0,7.2,'cond 1 ?','d',w=2.0); A(0,6.6,0,6.1,'T'); A(0.62,7.2,1.9,7.2,'F'); B(3.0,7.2,'stmt 3')
B(0,5.5,'cond 2 ?','d',w=2.0); A(0.62,5.5,1.9,5.5,'T'); A(0,4.9,0,4.5,'F')
B(3.0,5.5,'stmt 1'); B(0,4.1,'stmt 2')
for (x,y) in ((4.1,7.2),(4.1,5.5)): L([x,5.2],[y,y])
L([1.1,5.2],[4.1,4.1]); L([5.2,5.2],[7.2,2.3]); A(5.2,2.3,2.7,1.9)
B(1.6,1.8,'Stop','t')
"""),
}

def fig(key, cap):
    y0, y1, body = FIGS[key]
    return '```figure caption="%s"\n%s%s%s```' % (cap, PRE.strip('\n') + '\n', body.strip('\n') + '\n', (POST % (y0, y1)).strip('\n') + '\n')

def code(m):
    kind, name = m.group(1), m.group(2)
    lang = {'C': 'c', 'F': 'fortran'}[kind]
    src = open(os.path.join(HERE, 'prog', name)).read().rstrip('\n')
    return '```%s\n%s\n```' % (lang, src)

tpl = open(sys.argv[1]).read()
tpl = re.sub(r'\{\{([CF]):([^}]+)\}\}', code, tpl)
tpl = re.sub(r'\{\{FIG:(\w+)\|([^}]*)\}\}', lambda m: fig(m.group(1), m.group(2)), tpl)
open(sys.argv[2], 'w').write(tpl)
print('wrote', sys.argv[2], len(tpl))
