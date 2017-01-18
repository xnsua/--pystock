from datetime import datetime

from common import time_helper


def json_default_encoder(o):
    if isinstance(o, datetime):
        return time_helper.to_seconds_str(o)

    if isinstance(o, set):
        return list(o)
    return o.__dict__
