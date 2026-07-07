from django.db import migrations


RESOURCE_ID = 'f450b8c0-93d5-4317-b282-6554b76d20d4'


def improve_seo(apps, schema_editor):
    Resource = apps.get_model('api', 'Resource')
    try:
        r = Resource.objects.get(id=RESOURCE_ID)
    except Resource.DoesNotExist:
        return
    changed = False
    old_title = r.title
    old_desc = r.description
    old_tags = r.tags
    if 'past year' not in r.title.lower():
        r.title = 'BSc Nursing 1st Year Past Year Questions - TU, IOM'
        changed = True
    if r.description and 'past year' in r.description.lower():
        r.description = 'BSc Nursing 1st Year past year questions from TU and IOM. Practice with previous exam papers for Integrated Health Science I & II, Food & Nutrition, and Fundamentals of Nursing.'
        changed = True
    nursing_tags = 'BSc nursing, 1st year, past year questions, question bank, TU, IOM, nursing exam papers, integrated health science, fundamentals of nursing, food and nutrition, bachelor nursing, previous year questions'
    if r.tags != nursing_tags:
        r.tags = nursing_tags
        changed = True
    if changed:
        r.save()


def reverse_improve_seo(apps, schema_editor):
    Resource = apps.get_model('api', 'Resource')
    try:
        r = Resource.objects.get(id=RESOURCE_ID)
    except Resource.DoesNotExist:
        return
    r.title = 'Bsc nursing 1st year , TU, IOM'
    r.description = 'Past year questions of Bsc nursing 1st year , TU, IOM'
    r.tags = ''
    r.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0068_rename_ann_stat_pub_idx_announcemen_status_03b481_idx_and_more'),
    ]

    operations = [
        migrations.RunPython(improve_seo, reverse_improve_seo),
    ]
