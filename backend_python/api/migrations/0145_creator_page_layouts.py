# Two more layouts for a creator storefront: `magazine` and `stack`.
#
# Choices-only, so nothing changes in the database -- but leaving it
# unmigrated makes `makemigrations --check` fail for whoever comes next.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0144_one_pending_payment_per_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creatorpage',
            name='layout',
            field=models.CharField(choices=[('editorial', 'Editorial'), ('spotlight', 'Spotlight'), ('grid', 'Grid'), ('classic', 'Classic'), ('magazine', 'Magazine'), ('stack', 'Stack')], default='editorial', max_length=20),
        ),
    ]
