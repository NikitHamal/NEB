from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0084_coding_agent_attachments'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name='CodingAgentEvent'),
                migrations.DeleteModel(name='CodingAgentFileChange'),
                migrations.DeleteModel(name='CodingAgentToolCall'),
                migrations.DeleteModel(name='CodingAgentMessage'),
                migrations.DeleteModel(name='CodingAgentSession'),
                migrations.DeleteModel(name='CodingAgentProject'),
            ],
        ),
    ]
