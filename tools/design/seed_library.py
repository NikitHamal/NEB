"""Seed library resources of every kind for viewer audits (DEBUG + sqlite only).
   cd backend_python && DB_ENGINE=sqlite DEBUG=True SECRET_KEY=x python3 ../tools/design/seed_library.py
Prints "<label> <id>" per resource."""
import math, os, struct, sys, time, uuid, wave
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
import django
django.setup()
from django.conf import settings
assert settings.DEBUG
from api.models import Resource

root = settings.MEDIA_ROOT / 'resources' / 'demo'
root.mkdir(parents=True, exist_ok=True)

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
pdf = root / 'physics-notes.pdf'
c = canvas.Canvas(str(pdf), pagesize=A4)
for p in range(1, 5):
    c.setFont('Helvetica-Bold', 28); c.drawString(72, 760, 'Physics - Wave Motion, page %d' % p)
    c.setFont('Helvetica', 13)
    for i in range(30):
        c.drawString(72, 720 - i * 20, 'Line %d: a wave transfers energy without transferring matter.' % (i + 1))
    c.showPage()
c.save()

from PIL import Image, ImageDraw
img = root / 'diagram.png'
im = Image.new('RGB', (1200, 800), (232, 240, 255)); d = ImageDraw.Draw(im)
for i in range(0, 1200, 60): d.line([(i, 0), (i, 800)], fill=(200, 215, 245))
d.ellipse([400, 200, 800, 600], outline=(0, 75, 212), width=12)
im.save(img)

wav = root / 'lecture.wav'
w = wave.open(str(wav), 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(22050)
w.writeframes(b''.join(struct.pack('<h', int(9000 * math.sin(2 * math.pi * 330 * i / 22050))) for i in range(22050 * 6)))
w.close()

now = int(time.time() * 1000)
def make(label, **kw):
    rid = str(uuid.uuid4())
    base = dict(id=rid, title=label, description='A short description of this resource for students.', subject='Physics',
                grade_level='Class 12', type='PDF', approval_status='approved', added_at=now, file_size=0)
    base.update(kw)
    Resource.objects.filter(title=label).delete()
    Resource.objects.create(**base)
    print(label.replace(' ', '_'), rid)
    return rid

make('Single PDF', file_url='/media/resources/demo/physics-notes.pdf', type='PDF', file_size=482000)
make('Image only', file_url='/media/resources/demo/diagram.png', type='Image', file_size=91000)
make('Audio only', file_url='/media/resources/demo/lecture.wav', type='Audio', file_size=264000)
make('Video YouTube', file_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ', type='Video')
make('Link only', file_url='https://example.com/syllabus', type='Link')
make('Word note', file_url='/media/resources/demo/notes.docx', type='Note', file_size=22000)
make('No file', file_url='', type='Note')
make('Paid course', file_url='/media/resources/demo/physics-notes.pdf', is_paid=True, price=199)
gid = str(uuid.uuid4())
make('Bundle PDF', file_url='/media/resources/demo/physics-notes.pdf', type='PDF', upload_group_id=gid, file_size=482000, added_at=now)
make('Bundle Audio', file_url='/media/resources/demo/lecture.wav', type='Audio', upload_group_id=gid, is_lead=False, file_size=264000, added_at=now + 1)
make('Bundle Diagram', file_url='/media/resources/demo/diagram.png', type='Image', upload_group_id=gid, is_lead=False, file_size=91000, added_at=now + 2)
