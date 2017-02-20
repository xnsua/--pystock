from datetime import datetime

import common.helper


def json_default_encoder(o):
    if isinstance(o, datetime):
        return common.helper.to_seconds_str(o)

    if isinstance(o, set):
        return list(o)
    return o.__dict__
