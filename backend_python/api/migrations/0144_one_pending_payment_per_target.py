"""One pending payment per buyer per target, enforced by the database.

`record_purchase` already looks for the buyer's open submission and updates it
instead of inserting a second one, but two taps of Submit racing each other both
saw none and both inserted. That left an admin two identical proofs to verify and
the seller in line to be credited twice for one sale.

Any duplicates an older build already wrote are collapsed first — the newest row
is the one `record_purchase` would have been updating, so it is the one kept.
"""
from django.db import migrations, models


def collapse_duplicate_pending(apps, schema_editor):
    PaymentVerification = apps.get_model('api', 'PaymentVerification')
    seen = set()
    stale = []
    rows = (PaymentVerification.objects
            .filter(status='pending')
            .order_by('-created_at')
            .values_list('id', 'buyer_id', 'course_id', 'resource_id'))
    for row_id, buyer_id, course_id, resource_id in rows:
        if course_id is None and resource_id is None:
            continue
        key = (buyer_id, course_id, resource_id)
        if key in seen:
            stale.append(row_id)
        else:
            seen.add(key)
    for start in range(0, len(stale), 500):
        PaymentVerification.objects.filter(id__in=stale[start:start + 500]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0143_creator_marketplace_pages_courses_posts'),
    ]

    operations = [
        migrations.RunPython(collapse_duplicate_pending, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='paymentverification',
            constraint=models.UniqueConstraint(
                condition=models.Q(('course__isnull', False), ('status', 'pending')),
                fields=('buyer', 'course'),
                name='uniq_pending_payment_per_course',
            ),
        ),
        migrations.AddConstraint(
            model_name='paymentverification',
            constraint=models.UniqueConstraint(
                condition=models.Q(('resource__isnull', False), ('status', 'pending')),
                fields=('buyer', 'resource'),
                name='uniq_pending_payment_per_resource',
            ),
        ),
    ]
