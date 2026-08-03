# Hand-written marketplace migration: wallet/loyalty/credits economy.
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0103_alter_resourcecomment_user'),
    ]

    operations = [
        # ---- User: Nebians points, AI credits (persistent + monthly free), spend ----
        migrations.AddField(
            model_name='user',
            name='nebians_points',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='ai_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='free_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='free_credits_month',
            field=models.CharField(blank=True, default='', max_length=7),
        ),
        migrations.AddField(
            model_name='user',
            name='total_spent',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12),
        ),
        # ---- PaymentVerification: add an "On Hold" verification state ----
        migrations.AlterField(
            model_name='paymentverification',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending Verification'),
                    ('approved', 'Approved'),
                    ('hold', 'On Hold'),
                    ('rejected', 'Rejected'),
                ],
                db_index=True, default='pending', max_length=20,
            ),
        ),
        # ---- WithdrawalRequest: more Nepali payout methods ----
        migrations.AlterField(
            model_name='withdrawalrequest',
            name='payout_method',
            field=models.CharField(
                choices=[
                    ('esewa', 'eSewa'),
                    ('khalti', 'Khalti'),
                    ('mobile_banking', 'Mobile Banking'),
                    ('connectips', 'ConnectIPS'),
                    ('bank', 'Bank Transfer'),
                ],
                default='esewa', max_length=30,
            ),
        ),
        # ---- PaymentConfig: editable marketplace/company-QR/commission economy ----
        migrations.CreateModel(
            name='PaymentConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('company_qr_url', models.TextField(blank=True, default='')),
                ('company_qr_caption', models.CharField(blank=True, default='NEBians — Company QR', max_length=200)),
                ('payment_instructions', models.TextField(blank=True, default='')),
                ('upi_id', models.CharField(blank=True, default='', max_length=100)),
                ('commission_percent', models.DecimalField(decimal_places=2, default=Decimal('2.50'), max_digits=5)),
                ('withdraw_min', models.DecimalField(decimal_places=2, default=Decimal('1000.00'), max_digits=10)),
                ('points_per_rupee_buyer', models.DecimalField(decimal_places=2, default=Decimal('0.10'), max_digits=6)),
                ('points_per_rupee_seller', models.DecimalField(decimal_places=2, default=Decimal('0.10'), max_digits=6)),
                ('points_to_credit', models.PositiveIntegerField(default=2)),
                ('free_credits_per_month', models.PositiveIntegerField(default=10)),
                ('updated_at', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'payment_config',
            },
        ),
    ]
