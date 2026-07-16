from django.db import migrations


REMOVED_PROVIDERS = ['eqing', 'freegpt', 'deepseekai', 'surfsense', 'g4f']


def forward(apps, schema_editor):
    BotConfig = apps.get_model('api', 'BotConfig')
    ArenaChatSession = apps.get_model('api', 'ArenaChatSession')

    BotConfig.objects.filter(provider__in=REMOVED_PROVIDERS).update(provider='qwen')
    ArenaChatSession.objects.filter(provider__in=REMOVED_PROVIDERS).update(provider='qwen')


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0078_social_link_click_details'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
