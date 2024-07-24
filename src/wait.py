import datetime
import time


def sleep(milliseconds):
    time.sleep(milliseconds / 1000)
    return datetime.datetime.now().isoformat()
