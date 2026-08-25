from django.db import migrations, models

import api.models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0123_syllabus_rich_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="CodeSession",
            fields=[
                ("id", models.CharField(default=api.models._new_code_session_id, max_length=32, primary_key=True, serialize=False)),
                ("user_id", models.CharField(blank=True, db_index=True, default="", max_length=255)),
                ("name", models.CharField(blank=True, default="New session", max_length=200)),
                ("provider", models.CharField(blank=True, default="", max_length=40)),
                ("model", models.CharField(blank=True, default="", max_length=120)),
                ("effort", models.CharField(blank=True, default="balanced", max_length=16)),
                ("status", models.CharField(default="idle", max_length=16)),
                ("error", models.TextField(blank=True, default="")),
                ("workspace_label", models.CharField(blank=True, default="", max_length=300)),
                ("daemon_info", models.JSONField(blank=True, null=True)),
                ("cancel_flag", models.BooleanField(default=False)),
                ("created_at", models.BigIntegerField(default=0)),
                ("updated_at", models.BigIntegerField(default=0)),
            ],
            options={
                "db_table": "code_sessions",
                "ordering": ["-updated_at"],
            },
        ),
        migrations.AddIndex(
            model_name="codesession",
            index=models.Index(fields=["user_id", "-updated_at"], name="code_sessio_user_id_c7f142_idx"),
        ),
        migrations.AddIndex(
            model_name="codesession",
            index=models.Index(fields=["status", "updated_at"], name="code_sessio_status_c01fb3_idx"),
        ),
        migrations.CreateModel(
            name="CodeMessage",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("session", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="messages", to="api.codesession")),
                ("role", models.CharField(default="user", max_length=12)),
                ("content", models.TextField(blank=True, default="")),
                ("meta", models.JSONField(blank=True, null=True)),
                ("created_at", models.BigIntegerField(default=0)),
            ],
            options={
                "db_table": "code_messages",
                "ordering": ["created_at", "id"],
            },
        ),
        migrations.AddIndex(
            model_name="codemessage",
            index=models.Index(fields=["session", "created_at"], name="code_messag_session_260060_idx"),
        ),
    ]
