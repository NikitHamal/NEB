from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_performance_indexes'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='edithistory',
            old_name='api_edithistory_target_idx_edit_histor_target__ea3ea5_idx',
            new_name='api_edithistory_target_type_target_id_idx',
        ),
    ]