# Generated for Study Lab summary modes, editable summaries, and mindmaps.
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_alter_botconfig_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='studydocument',
            name='summary_compact',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='studydocument',
            name='summary_detailed',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='studydocument',
            name='summary_updated_at',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studydocument',
            name='mindmap_json',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='studydocument',
            name='mindmap_generated_at',
            field=models.BigIntegerField(default=0),
        ),
        migrations.RunSQL(
            "UPDATE study_documents SET summary_compact = summary WHERE COALESCE(summary_compact, '') = '' AND COALESCE(summary, '') <> ''",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
