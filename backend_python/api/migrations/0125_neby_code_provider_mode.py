from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0124_neby_code_sessions'),
    ]

    operations = [
        migrations.AddField(
            model_name='codesession',
            name='provider_id',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='codesession',
            name='model',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='codesession',
            name='mode',
            field=models.CharField(blank=True, default='agent', max_length=16),
        ),
    ]
