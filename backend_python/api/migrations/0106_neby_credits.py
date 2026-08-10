import uuid
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0105_background_agent_thinking_mode'),
    ]

    operations = [
        migrations.CreateModel(
            name='NebyCreditTransaction',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(max_length=30)),
                ('amount', models.IntegerField(default=0)),
                ('points_spent', models.PositiveIntegerField(default=0)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('created_at', models.BigIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_transactions', to='api.user')),
            ],
            options={
                'db_table': 'neby_credit_transactions',
                'ordering': ['-created_at'],
            },
        ),
    ]
