import numpy as np

from common.data_structures.geometry import Point
from common_stock.stock_helper import p_repr


class MddInfo:
    def __init__(self, mdd, left_point, right_point):
        self.mdd = mdd
        self.left_point = left_point  # type: Point
        self.right_point = right_point  # type: Point

    @property
    def xs(self):
        return [self.left_point.x, self.right_point.x]

    @property
    def ys(self):
        return [self.left_point.y, self.right_point.y]

    def __repr__(self):
        return f'MDD{{{p_repr(self.mdd)},[{self.left_point},{self.right_point}]}}'


def calc_max_drawdown_pos_and_value(array_like):
    array_like = np.asarray(array_like)
    # noinspection PyArgumentList
    right = np.argmax(np.maximum.accumulate(array_like) - array_like)  # end of the period
    left = np.argmax(array_like[:right]) if right != 0 else 0  # start of period
    return left, right, array_like[right] / array_like[left] - 1


def calc_max_drawdown_info(x_arr, y_arr):
    left, right, mdd = calc_max_drawdown_pos_and_value(y_arr)
    return MddInfo(mdd, Point(x_arr[left], y_arr[left]), Point(x_arr[right], y_arr[right]))


def main():
    ll = [1, 1, 1.1, 0.9, 0.8, 0.7, 3, 3]
    import datetime
    s_time = datetime.datetime.now()
    result = calc_max_drawdown_pos_and_value(ll)
    print(datetime.datetime.now() - s_time)
    print(result)


if __name__ == '__main__':
    main()
