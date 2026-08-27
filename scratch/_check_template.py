import sys, os, types, django
from django.conf import settings

os.chdir(r'F:\NEB\backend_python')
sys.path.insert(0, r'F:\NEB\backend_python')

urls = types.ModuleType('stub_urls')
urls.app_name = 'web'
from django.urls import path
urls.urlpatterns = [path('edit_profile', lambda r: None, name='edit_profile')]
sys.modules['stub_urls'] = urls

settings.configure(
    DEBUG=True, SECRET_KEY='test',
    INSTALLED_APPS=['django.contrib.staticfiles', 'django.contrib.contenttypes'],
    STATIC_URL='/static/', ROOT_URLCONF='stub_urls',
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [r'F:\NEB\backend_python\web\templates'],
                'APP_DIRS': False,
                'OPTIONS': {'string_if_invalid': 'INVALID-STAR',
                            'libraries': {'web_extras': 'web.templatetags.web_extras'}}}],
)
django.setup()
from django.template import engines
eng = engines['django']
src = open(r'F:\NEB\backend_python\web\templates\web\home.html').read()
result_file = r'F:\NEB\scratch\_tpl_result.txt'
log = open(result_file, 'w')


def emit(*a):
    s = ' '.join(str(x) for x in a)
    print(s)
    log.write(s + '\n')
    log.flush()


try:
    eng.from_string(src)
    emit('COMPILE OK: home.html compiled (needs_profile block syntax valid)')
    op = '{% if needs_profile %}'
    ed = '{% endif %}'
    i0 = src.index(op)
    i1 = src.index(ed, i0 + len(op)) + len(ed)
    frag = src[i0:i1]
    emit('extracted banner fragment len=%d' % len(frag))
    frag_tpl = eng.from_string(frag)
    ctx = {'csp_nonce': 'NONCE', 'profile_user': None, 'needs_profile': True}
    rendered = frag_tpl.render(ctx)
    emit('RENDER OK fragment len=%d' % len(rendered))
    emit('banner_div:', 'profile-complete-banner' in rendered)
    emit('later_button:', "I'll do it later" in rendered)
    emit('dismiss_script:', 'pcLater' in rendered and 'localStorage' in rendered)
    emit('style_block:', '.profile-complete-banner' in rendered)
    emit('edit_link:', 'href="/edit_profile"' in rendered)
except Exception:
    import traceback as tb
    emit('EXCEPTION:')
    emit(tb.format_exc())
finally:
    log.close()
