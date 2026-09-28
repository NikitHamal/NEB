import time
import uuid
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def now_ms():
    return int(time.time() * 1000)


def uuid_str():
    return str(uuid.uuid4())

def money_str(value):
    """Rupees as a display string: exact to the paisa, never scientific.

    The old formatting went through ``'%g' % float(value)``, which drops the
    cents past six significant digits and turns a Rs. 1,234,567.89 balance into
    ``1.23457e+06``. Decimal keeps the paisa; whole amounts stay whole so a
    Rs. 500 course still reads "Rs. 500" and not "Rs. 500.00".
    """
    try:
        amount = Decimal(str(value or 0))
    except (InvalidOperation, TypeError, ValueError):
        return '0'
    if not amount.is_finite():
        return '0'
    amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    if amount == 0:
        return '0'
    whole = amount.to_integral_value()
    return str(whole.quantize(Decimal('1'))) if amount == whole else f'{amount:f}'
