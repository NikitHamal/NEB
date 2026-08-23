from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0122_canvas_snapshots_and_settings"),
    ]

    operations = [
        migrations.AddField(
            model_name="syllabuscontent",
            name="rich_content",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="syllabuscontent",
            name="source_resource_id",
            field=models.CharField(blank=True, default="", max_length=36),
        ),
        migrations.AddField(
            model_name="syllabuscontent",
            name="source_label",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
