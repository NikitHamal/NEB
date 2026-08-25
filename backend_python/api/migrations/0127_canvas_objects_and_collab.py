from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0126_alter_agentaction_action_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanvasObject',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('obj_type', models.CharField(db_index=True, default='pen', max_length=24)),
                ('payload', models.TextField(blank=True, default='{}')),
                ('x', models.FloatField(default=0)),
                ('y', models.FloatField(default=0)),
                ('z', models.IntegerField(default=0)),
                ('created_at', models.BigIntegerField(default=0)),
                ('updated_at', models.BigIntegerField(default=0)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='canvas_objects', to='api.canvasboard')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_canvas_objects', to='api.user')),
            ],
            options={
                'db_table': 'canvas_objects',
                'ordering': ['z', 'created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='canvasobject',
            index=models.Index(fields=['board', 'z'], name='canvas_obj_board_z_idx'),
        ),
    ]
