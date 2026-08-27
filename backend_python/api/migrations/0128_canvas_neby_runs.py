from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0127_canvas_objects_and_collab'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanvasNebyRun',
            fields=[
                ('id', models.CharField(default=django.db.models.fields.uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('kind', models.CharField(choices=[('explore', 'Explore'), ('suggest', 'Suggest')], db_index=True, default='explore', max_length=10)),
                ('goal', models.TextField(blank=True, default='')),
                ('summary', models.TextField(blank=True, default='')),
                ('questions', models.JSONField(blank=True, default=list)),
                ('provider', models.CharField(blank=True, default='', max_length=60)),
                ('created_at', models.BigIntegerField(default=0)),
                ('board', models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.CASCADE, related_name='neby_runs', to='api.canvasboard')),
                ('user', models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.CASCADE, related_name='canvas_neby_runs', to='api.user')),
            ],
            options={
                'db_table': 'canvas_neby_runs',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['board', '-created_at'], name='canvas_run_board_created_idx')],
            },
        ),
    ]
