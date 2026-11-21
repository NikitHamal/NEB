# Generated migration removing dropped Marketplace models and obsolete 2D avatar fields.
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0174_heal_verified_institution_owners'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='paymentverification',
            name='uniq_pending_payment_per_course',
        ),
        migrations.RemoveIndex(
            model_name='paymentverification',
            name='payment_ver_buyer_i_0d0d14_idx',
        ),
        migrations.RemoveField(
            model_name='paymentverification',
            name='course',
        ),
        migrations.AlterUniqueTogether(
            name='creatorcourseresource',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='creatorcourseresource',
            name='course',
        ),
        migrations.RemoveField(
            model_name='creatorcourseresource',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='creatorpost',
            name='page',
        ),
        migrations.AlterUniqueTogether(
            name='creatorcourse',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='creatorcourse',
            name='page',
        ),
        migrations.RemoveField(
            model_name='creatorpage',
            name='user',
        ),
        migrations.DeleteModel(
            name='CreatorCourseResource',
        ),
        migrations.DeleteModel(
            name='CreatorPost',
        ),
        migrations.DeleteModel(
            name='CreatorCourse',
        ),
        migrations.DeleteModel(
            name='CreatorPage',
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar_anim',
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar_bg',
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar_bg_color',
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar_color',
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar_expression',
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar_eye_color',
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar_hue',
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar_shape',
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar_tone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='avatar_use_pp',
        ),
    ]
