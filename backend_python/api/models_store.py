"""
Cosmetics store models — owned items and the points spending ledger.
No FK to users (latin1 charset on the production table blocks FK constraints).
"""
from django.db import models


class UserCosmetic(models.Model):
    user_id = models.CharField(max_length=255, db_index=True)
    item_key = models.CharField(max_length=40)
    kind = models.CharField(max_length=12)
    price_paid = models.PositiveIntegerField(default=0)
    acquired_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'user_cosmetics'
        unique_together = [('user_id', 'item_key')]
        indexes = [models.Index(fields=['user_id', 'kind'])]

    def __str__(self):
        return f'{self.user_id}:{self.item_key}'


class PointsLedger(models.Model):
    user_id = models.CharField(max_length=255, db_index=True)
    delta = models.IntegerField(default=0)
    reason = models.CharField(max_length=40)
    item_key = models.CharField(max_length=40, blank=True, default='')
    balance_after = models.PositiveIntegerField(default=0)
    created_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'points_ledger'

    def __str__(self):
        return f'{self.user_id}:{self.reason}:{self.delta}'
