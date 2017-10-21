from typing import List

from common.helper import p_repr
from stock_data_manager.stock_data.int_trade_day import intday_span


class HoldPeriod:
    def __init__(self, stock_code, start_date, end_date, buy_price, sell_price):
        self.stock_code = stock_code
        self.start_date = start_date
        self.buy_price = buy_price
        self.end_date = end_date
        self.sell_price = sell_price

        self.period_len = None
        self.yield_ = None
        self.yyield = None

        self._calc_info()

    def _calc_info(self):
        # May not use.
        self.period_len = intday_span(self.start_date, self.end_date)
        self.yield_ = (self.sell_price / self.buy_price)
        self.yyield = self.yield_ ** (245 / self.period_len)


class SingleEmuAccount:
    def __init__(self, code, date_range, yield_):
        self.code = code
        self.hold_periods = []  # type: List[HoldPeriod]

        self._buy_day = None
        self._buy_price = None

        self.date_range = date_range
        self.day_len = intday_span(*date_range)

        self.yield_ = yield_
        self.yyield = yield_ ** (245 / self.day_len)

        self.hold_len = None
        self.hold_yield = None
        self.hold_yyield = None
        self.occupy_per = None

        self.df = None

    def buy(self, day, price):
        if not self._buy_day:
            self._buy_day = day
            self._buy_price = price

    def sell(self, day, price):
        if self._buy_day:
            self.hold_periods.append(
                HoldPeriod(self.code, self._buy_day, day, self._buy_price, price)
            )
            self._buy_day = None

    def calc_addition_infos(self):
        if self.df is None:
            import pandas
            pandas.options.display.float_format = '{:,.3f}'.format
            df = pandas.DataFrame([item.__dict__ for item in self.hold_periods])
            df = df[
                ['stock_code', 'start_date', 'end_date', 'buy_price', 'sell_price', 'period_len',
                 'yield_', 'yyield']]
            self.df = df
        self.hold_len = self.df.period_len.sum()
        self.hold_yield = self.df.yield_.prod()
        self.hold_yyield = self.hold_yield ** (245 / self.hold_len)

        self.occupy_per = self.hold_len / self.day_len

        return self

    def __repr__(self):
        occupy_per = p_repr(self.occupy_per, 4)
        yyield, hold_yyield = p_repr(self.yyield, 4), p_repr(self.hold_yyield, 4)
        return f'Acc:{{day_len: {self.day_len}  hold_len: {self.hold_len}  occupy_per: {occupy_per}\n' \
               f'       yyield: {yyield}  hold_yyield: {hold_yyield}'

    def overlap_other(self, other: 'SingleEmuAccount'):
        new_periods = _overlap_hold_periods(self.hold_periods, other.hold_periods)
        acc = SingleEmuAccount(self.code, self.date_range, self.yield_)
        acc.hold_periods = new_periods
        acc.calc_addition_infos()
        return acc


def _overlap_hold_periods(ps1, ps2):
    index1 = 0
    index2 = 0
    periods1 = ps1  # type: List[HoldPeriod]
    periods2 = ps2  # type: List[HoldPeriod]

    new_periods = []

    while index1 < len(periods1) and index2 < len(periods2):
        p1 = periods1[index1]
        p2 = periods2[index2]

        max_start = max(p1.start_date, p2.start_date)
        min_end = min(p1.end_date, p2.end_date)
        buy_price = p1.buy_price if max_start == p1.start_date else p2.buy_price
        sell_price = p1.sell_price if min_end == p1.end_date else p2.sell_price
        if min_end > max_start:
            tmp = HoldPeriod(p1.stock_code, max_start, min_end, buy_price, sell_price)
            new_periods.append(tmp)

        if p1.end_date < p2.end_date:
            index1 = index1 + 1
        else:
            index2 = index2 + 1
    return new_periods


def test_overlap_other():
    def assert_hold_period_equal(hp1: HoldPeriod, hp2: HoldPeriod):
        assert hp1.start_date == hp2.start_date
        assert hp2.end_date == hp2.end_date
        assert hp1.buy_price == hp2.buy_price
        assert hp1.sell_price == hp2.sell_price

    def assert_hold_periods_equal(hps1, hps2):
        assert len(hps1) == len(hps2)
        for hp1, hp2 in zip(hps1, hps2):
            assert_hold_period_equal(hp1, hp2)

    # [20170929 20171009 20171010 20171011 20171012 20171013 20171016 20171017
    #  20171018 20171019 20171020 20171023 20171024 20171025 20171026 20171027]
    dates = [20170929, 20171009, 20171010, 20171011, 20171012, 20171013, 20171016, 20171017
        , 20171018, 20171019, 20171020, 20171023, 20171024, 20171025, 20171026, 20171027
        , 20171030, 20171031, 20171101, 20171102, 20171103, 20171106, 20171107, 20171108
        , 20171109, 20171110, 20171113]
    code = '510050.XSHG'
    # Test empty
    hp1 = [HoldPeriod(code, dates[1], dates[2], 1, 2)]
    hp2 = [HoldPeriod(code, dates[2], dates[3], 1, 2)]
    val = _overlap_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [])
    val2 = _overlap_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)
    # Test empty
    hp1 = [HoldPeriod(code, dates[2], dates[3], 2, 2)]
    hp2 = [HoldPeriod(code, dates[1], dates[2], 1, 2)]
    val = _overlap_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [])
    val2 = _overlap_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)

    # test contain
    hp1 = [HoldPeriod(code, dates[1], dates[2], 1, 2)]
    hp2 = [HoldPeriod(code, dates[1], dates[2], 1, 2)]
    val = _overlap_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [HoldPeriod(code, dates[1], dates[2], 1, 2)])
    val2 = _overlap_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)
    # test contain
    hp1 = [HoldPeriod(code, dates[1], dates[2], 1, 2)]
    hp2 = [HoldPeriod(code, dates[1], dates[3], 1, 2)]
    val = _overlap_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [HoldPeriod(code, dates[1], dates[2], 1, 2)])
    val2 = _overlap_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)
    # test contain
    hp1 = [HoldPeriod(code, dates[1], dates[2], 1, 2)]
    hp2 = [HoldPeriod(code, dates[0], dates[3], 1, 2)]
    val = _overlap_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [HoldPeriod(code, dates[1], dates[2], 1, 2)])
    val2 = _overlap_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)

    # test intersect
    hp1 = [HoldPeriod(code, dates[0], dates[2], 1, 2)]
    hp2 = [HoldPeriod(code, dates[1], dates[3], 3, 4)]
    val = _overlap_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [HoldPeriod(code, dates[1], dates[2], 3, 2)])
    val2 = _overlap_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)

    # test intersect
    hp1 = [HoldPeriod(code, dates[0], dates[2], 1, 2)]
    hp2 = [HoldPeriod(code, dates[1], dates[3], 3, 4)]
    val = _overlap_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [HoldPeriod(code, dates[1], dates[2], 3, 2)])
    val2 = _overlap_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)

    # test intersect
    hp1 = [HoldPeriod(code, dates[1], dates[2], 1, 2), HoldPeriod(code, dates[3], dates[4], 3, 4)]
    hp2 = [HoldPeriod(code, dates[0], dates[5], 0.1, 5)]
    val = _overlap_hold_periods(hp1, hp2)
    assert_hold_periods_equal(val, hp1)
    val2 = _overlap_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)

    # test intersect
    hp1 = [HoldPeriod(code, dates[0], dates[2], 0.1, 2),
           HoldPeriod(code, dates[3], dates[4], 3, 4)]
    hp2 = [HoldPeriod(code, dates[1], dates[5], 1, 5)]
    val = _overlap_hold_periods(hp1, hp2)
    assert_hold_periods_equal(val, [HoldPeriod(code, dates[1], dates[2], 1, 2),
                                    HoldPeriod(code, dates[3], dates[4], 3, 4)])
    val2 = _overlap_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)
