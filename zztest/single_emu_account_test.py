from stock_data_manager.ddr_file_cache import read_ddr_fast
from trading.emulation.single_emu_account import HoldPeriod, SingleEmuAccount


def assert_hold_period_equal(hp1: HoldPeriod, hp2: HoldPeriod):
    assert hp1.buy_ts == hp2.buy_ts
    assert hp2.sell_ts == hp2.sell_ts
    assert hp1.buy_price == hp2.buy_price
    assert hp1.sell_price == hp2.sell_price


def assert_hold_periods_equal(hps1, hps2):
    assert len(hps1) == len(hps2)
    for hp1, hp2 in zip(hps1, hps2):
        assert_hold_period_equal(hp1, hp2)


def test_overlap_other():
    # [20170929 20171009 20171010 20171011 20171012 20171013 20171016 20171017
    #  20171018 20171019 20171020 20171023 20171024 20171025 20171026 20171027]
    dates = [20170929, 20171009, 20171010, 20171011, 20171012, 20171013, 20171016, 20171017
        , 20171018, 20171019, 20171020, 20171023, 20171024, 20171025, 20171026, 20171027
        , 20171030, 20171031, 20171101, 20171102, 20171103, 20171106, 20171107, 20171108
        , 20171109, 20171110, 20171113]
    code = '510050.XSHG'
    _calc_overlapped_hold_periods = SingleEmuAccount._calc_overlapped_hold_periods
    # Test empty
    hp1 = [HoldPeriod(code, dates[1], dates[2], 1, 2)]
    hp2 = [HoldPeriod(code, dates[2], dates[3], 1, 2)]
    val = _calc_overlapped_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [])
    val2 = _calc_overlapped_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)
    # Test empty
    hp1 = [HoldPeriod(code, dates[2], dates[3], 2, 2)]
    hp2 = [HoldPeriod(code, dates[1], dates[2], 1, 2)]
    val = _calc_overlapped_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [])
    val2 = _calc_overlapped_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)

    # test contain
    hp1 = [HoldPeriod(code, dates[1], dates[2], 1, 2)]
    hp2 = [HoldPeriod(code, dates[1], dates[2], 1, 2)]
    val = _calc_overlapped_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [HoldPeriod(code, dates[1], dates[2], 1, 2)])
    val2 = _calc_overlapped_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)
    # test contain
    hp1 = [HoldPeriod(code, dates[1], dates[2], 1, 2)]
    hp2 = [HoldPeriod(code, dates[1], dates[3], 1, 2)]
    val = _calc_overlapped_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [HoldPeriod(code, dates[1], dates[2], 1, 2)])
    val2 = _calc_overlapped_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)
    # test contain
    hp1 = [HoldPeriod(code, dates[1], dates[2], 1, 2)]
    hp2 = [HoldPeriod(code, dates[0], dates[3], 1, 2)]
    val = _calc_overlapped_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [HoldPeriod(code, dates[1], dates[2], 1, 2)])
    val2 = _calc_overlapped_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)

    # test intersect
    hp1 = [HoldPeriod(code, dates[0], dates[2], 1, 2)]
    hp2 = [HoldPeriod(code, dates[1], dates[3], 3, 4)]
    val = _calc_overlapped_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [HoldPeriod(code, dates[1], dates[2], 3, 2)])
    val2 = _calc_overlapped_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)

    # test intersect
    hp1 = [HoldPeriod(code, dates[0], dates[2], 1, 2)]
    hp2 = [HoldPeriod(code, dates[1], dates[3], 3, 4)]
    val = _calc_overlapped_hold_periods(hp1, hp2)
    assert_hold_periods_equal(
        val, [HoldPeriod(code, dates[1], dates[2], 3, 2)])
    val2 = _calc_overlapped_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)

    # test intersect
    hp1 = [HoldPeriod(code, dates[1], dates[2], 1, 2), HoldPeriod(code, dates[3], dates[4], 3, 4)]
    hp2 = [HoldPeriod(code, dates[0], dates[5], 0.1, 5)]
    val = _calc_overlapped_hold_periods(hp1, hp2)
    assert_hold_periods_equal(val, hp1)
    val2 = _calc_overlapped_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)

    # test intersect
    hp1 = [HoldPeriod(code, dates[0], dates[2], 0.1, 2),
           HoldPeriod(code, dates[3], dates[4], 3, 4)]
    hp2 = [HoldPeriod(code, dates[1], dates[5], 1, 5)]
    val = _calc_overlapped_hold_periods(hp1, hp2)
    assert_hold_periods_equal(val, [HoldPeriod(code, dates[1], dates[2], 1, 2),
                                    HoldPeriod(code, dates[3], dates[4], 3, 4)])
    val2 = _calc_overlapped_hold_periods(hp2, hp1)
    assert_hold_periods_equal(val2, val)


def test_HoldPeriod_left_trim():
    hp = HoldPeriod('510050.XSHG', 20161024, 20161027, 1, 2)
    assert hp

    sr = read_ddr_fast('510050.XSHG').df.open

    hp.left_trim(2, sr)
    assert hp.buy_price == (sr.at[20161026])
    assert hp

    hp = hp.left_trim(1, sr)
    assert not hp

    hp = hp.left_trim(1, sr)
    assert not hp


def test_calc_additional_info():
    code = '510050.XSHG'
    acc = SingleEmuAccount(code, (20161024, 20170801), 2)

    hp = HoldPeriod(code, 20161026, 20170327, 1, 2)
    hp2 = HoldPeriod(code, 20170419, 20170703, 1, 3)

    acc.reset_hold_period([hp])
    assert acc.hold_len == 102
    assert acc.day_len == 190
    assert 0.53 < acc.occupy_per < 0.54
    assert 5.28 < acc.hold_yyield < 5.3
    assert 2.44 < acc.yyield < 2.45

    acc.reset_hold_period([hp, hp2])
    assert acc.hold_len == 152
    assert acc.day_len == 190
    assert 0.79 < acc.occupy_per < 0.801
    assert 17 < acc.hold_yyield < 18
