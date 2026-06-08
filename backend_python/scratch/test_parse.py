import sys
import os
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
django.setup()

from api.models import StudyDocument
from api import qwen_proxy
from web.views_study_lab import _prepare_doc_for_qwen

class MockDoc:
    def __init__(self):
        self.file_name = "test.pdf"
        self.file_url = "some/local/path"

doc = MockDoc()
import uuid

file_name = f"test_{uuid.uuid4().hex}.pdf"
print(f"Testing doc {file_name}")

file_data = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Count 1\n/Kids [3 0 R]\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n/Resources <<\n/Font <<\n/F1 <<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\n>>\n>>\n>>\nendobj\n4 0 obj\n<<\n/Length 48\n>>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Hello Unparsed World) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000267 00000 n\ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n365\n%%EOF"

qwen_session, _ = qwen_proxy._get_session()
midtoken = qwen_proxy.get_midtoken(qwen_session)
if midtoken:
    qwen_session.headers['bx-umidtoken'] = midtoken
    qwen_session.headers['bx-v'] = '2.5.31'
req_headers = dict(qwen_session.headers)

from api.qwen_utils.file_upload import upload_file_from_bytes
file_obj = upload_file_from_bytes(file_name, file_data, qwen_session, req_headers)
if not file_obj:
    print("Failed to upload")
    sys.exit(0)

print("Prepared successfully!")
print(file_obj)

prepared = {'is_image': False, 'has_file': True, 'uploaded_files': [file_obj], 'text_content': None}

if 'parse_meta' in file_obj['file']['meta']:
    del file_obj['file']['meta']['parse_meta']

from web.views_study_lab import _qwen_model
chat_id = qwen_proxy.create_chat(qwen_session, model=_qwen_model())
print("Chat ID:", chat_id)
if chat_id:
    prompt = "Summarize this document."
    result = qwen_proxy.send_message(
        qwen_session, chat_id, prompt, model=_qwen_model(),
        parent_id=None, uploaded_files=prepared.get('uploaded_files')
    )
    print("Result:")
    print(result)