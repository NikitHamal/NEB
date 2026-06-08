import time
import uuid


def now_ms():
    return int(time.time() * 1000)


def uuid_str():
    return str(uuid.uuid4())