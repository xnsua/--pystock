import datetime

import sortedcontainers as sortedcontainers

from common.helper import dt_today, dt_from_time


class TimePoints:
    def __init__(self, time_points=None):
        self.time_points = sortedcontainers.SortedDict(time_points)
        self.time_points_used = {}
        pass

    def hit_once(self, vdatetime):
        vtime = vdatetime.time()
        index = self.time_points.bisect_right(vtime)
        index = index - 1
        if index >= 0:
            time_point = self.time_points.iloc[index]
            if vtime > time_point \
                    and self.time_points_used.get(time_point,
                                                  None) != dt_today():
                self.time_points_used[time_point] = dt_today()
                time_point_name = self.time_points[time_point]
                if not time_point_name:
                    return 'default_time_point'
                return time_point_name
        return None


def test_time_point():
    tp = TimePoints({datetime.time(1, 1, 1): 't1',
                     datetime.time(1, 2, 1): 't2',
                     datetime.time(1, 3, 1): 't3',
                     })
    assert 't1' == tp.hit_once(dt_from_time(1, 1, 2))
    assert not tp.hit_once(dt_from_time(1, 1, 2))
    assert 't3' == tp.hit_once(dt_from_time(1, 3, 2))
