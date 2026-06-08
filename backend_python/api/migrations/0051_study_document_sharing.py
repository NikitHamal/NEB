# Generated for Study Lab document sharing.
import uuid
from django.db import migrations, models
import django.db.models.deletion


def populate_share_tokens(apps, schema_editor):
    StudyDocument = apps.get_model('api', 'StudyDocument')
    for doc in StudyDocument.objects.all().only('pk', 'share_token'):
        token = str(uuid.uuid4())
        while StudyDocument.objects.filter(share_token=token).exclude(pk=doc.pk).exists():
            token = str(uuid.uuid4())
        doc.share_token = token
        doc.save(update_fields=['share_token'])


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_study_lab_summary_mindmap'),
    ]

    operations = [
        migrations.AddField(
            model_name='studydocument',
            name='share_token',
            field=models.CharField(blank=True, db_index=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='studydocument',
            name='share_mode',
            field=models.CharField(choices=[('private', 'Private'), ('link', 'Anyone with link'), ('specific', 'Specific users')], db_index=True, default='private', max_length=20),
        ),
        migrations.AddField(
            model_name='studydocument',
            name='shared_at',
            field=models.BigIntegerField(default=0),
        ),
        migrations.RunPython(populate_share_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='studydocument',
            name='share_token',
            field=models.CharField(db_index=True, default=uuid.uuid4, max_length=64, unique=True),
        ),
        migrations.CreateModel(
            name='StudyDocumentShare',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('created_at', models.BigIntegerField(default=0)),
                ('document', models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.CASCADE, related_name='share_grants', to='api.studydocument')),
                ('granted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_document_grants', to='api.user')),
                ('user', models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.CASCADE, related_name='study_document_shares', to='api.user')),
            ],
            options={
                'db_table': 'study_document_shares',
                'unique_together': {('document', 'user')},
            },
        ),
        migrations.AddIndex(
            model_name='studydocumentshare',
            index=models.Index(fields=['document', 'user'], name='study_docum_documen_a90d1b_idx'),
        ),
        migrations.AddIndex(
            model_name='studydocumentshare',
            index=models.Index(fields=['user', '-created_at'], name='study_docum_user_id_5481bc_idx'),
        ),
    ]
