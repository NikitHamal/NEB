"""Re-file page views whose utm_source is really a known site (chatgpt.com, ig, ...).

Only rows currently marked `campaign` are touched, one UPDATE per distinct
utm_source, so it is cheap and idempotent. Nothing is deleted.
"""
from django.db import migrations


def reclassify(apps, schema_editor):
    from nebians.analytics import rules
    PageView = apps.get_model('api', 'PageView')
    sources = (PageView.objects.filter(referrer_type='campaign')
               .exclude(utm_source='').values_list('utm_source', flat=True).distinct())
    for src in list(sources)[:500]:
        ref = rules.classify_utm_source(src)
        if not ref:
            continue
        PageView.objects.filter(referrer_type='campaign', utm_source=src, referrer_domain='').update(
            referrer_type=ref.channel, referrer_name=ref.name[:80], referrer_domain=ref.host[:255])


class Migration(migrations.Migration):
    dependencies = [('api', '0171_alter_user_employment_alter_user_experience_years_and_more')]
    operations = [migrations.RunPython(reclassify, migrations.RunPython.noop)]
