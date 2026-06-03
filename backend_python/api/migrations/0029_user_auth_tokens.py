from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_increase_notification_field_sizes'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAuthToken',
            fields=[
                ('id', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('token_hash', models.CharField(max_length=64, unique=True)),
                ('created_at', models.BigIntegerField(default=0)),
                ('last_used_at', models.BigIntegerField(default=0)),
                ('revoked_at', models.BigIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_tokens', to='api.user')),
            ],
            options={
                'db_table': 'user_auth_tokens',
            },
        ),
        migrations.AddIndex(
            model_name='userauthtoken',
            index=models.Index(fields=['user_id', 'revoked_at'], name='user_auth_t_user_id_e4923b_idx'),
        ),
        migrations.AddIndex(
            model_name='userauthtoken',
            index=models.Index(fields=['token_hash', 'revoked_at'], name='user_auth_t_token_h_060eb2_idx'),
        ),
    ]
