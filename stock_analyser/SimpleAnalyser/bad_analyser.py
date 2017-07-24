import numpy

from common_stock.trade_day import gtrade_day
from stock_data_updater.data_provider import gdp


def drop_after_count1(code, days=None):
    # Close - Open as drop
    ddr = gdp.ddr_of(code)

    money = 10000
    stock = 0
    drop_count = 0
    buy_count = 0
    if not days: days = ddr.days
    for index, day in enumerate(days):
        if stock != 0:
            money = stock * gdp.open(code, day)
            stock = 0
        elif drop_count == 2:
            buy_count += 1
            stock = money / gdp.open(code, day)
            money = 0
        else:
            pass

        if gdp.open(code, day) > gdp.close(code, day):
            drop_count += 1
        else:
            drop_count = 0
        print(money)

    if stock != 0:
        money = stock * gdp.close(code, days[-1])
    yield_ = money / 10000
    year_yield = yield_ ** (245 / buy_count)
    original_yield = gdp.close(code, ddr.days[-1]) / gdp.open(code, ddr.days[0])
    year_yield_base = original_yield ** (245 / len(ddr.days))
    ycompare = year_yield / year_yield_base
    year_yield = round(year_yield, 3)
    year_yield_base = round(year_yield_base, 3)
    ycompare = round(ycompare, 3)
    name = gdp.name_of(code)
    print(
        f'Code: {code}, Name:{name}, BaseYYield:{year_yield_base}, YYield:{year_yield}, YieldRaise: {ycompare}')
    return ycompare


def drop_after_count2(code):
    ddr = gdp.ddr_of(code)
    money = 100000
    stock = 0
    drop_count = 0
    buy_count = 0
    for index, day in enumerate(ddr.days):
        if index == 0: continue
        if stock != 0:
            money = stock * gdp.open(code, day)
            stock = 0
        elif drop_count == 2:
            buy_count += 1
            stock = money / gdp.open(code, day)
            money = 0
        else:
            pass

        if gdp.close(code, ddr.days[index - 1]) > gdp.close(code, day):
            drop_count += 1
        else:
            drop_count = 0

    if stock != 0:
        money = stock * gdp.close(code, ddr.days[-1])
    yield_ = money / 100000
    year_yield = yield_ ** (245 / buy_count)
    original_yield = gdp.close(code, ddr.days[-1]) / gdp.open(code, ddr.days[0])
    year_yield_base = original_yield ** (245 / len(ddr.days))
    ycompare = year_yield / year_yield_base
    year_yield = round(year_yield, 3)
    year_yield_base = round(year_yield_base, 3)
    ycompare = round(ycompare, 3)
    name = gdp.name_of(code)
    print(
        f'Code: {code}, Name:{name}, YYield:{year_yield_base}, YYield:{year_yield}, YieldRaise: {ycompare}')
    return ycompare


def drop_after_count3(code):
    ddr = gdp.ddr_of(code)
    money = 100000
    stock = 0
    drop_count = 0
    buy_count = 0
    for index, day in enumerate(ddr.days):
        if index == 0: continue
        if stock != 0:
            money = stock * gdp.open(code, day)
            stock = 0
        elif drop_count == 2:
            buy_count += 1
            stock = money / gdp.open(code, day)
            money = 0
        else:
            pass

        if gdp.open(code, ddr.days[index - 1]) > gdp.open(code, day) \
                and gdp.close(code, ddr.days[index - 1]) > gdp.close(code, day):
            drop_count += 1
        else:
            drop_count = 0

    if stock != 0:
        money = stock * gdp.close(code, ddr.days[-1])
    yield_ = money / 100000
    year_yield = yield_ ** (245 / buy_count)
    original_yield = gdp.close(code, ddr.days[-1]) / gdp.open(code, ddr.days[0])
    year_yield_base = original_yield ** (245 / len(ddr.days))
    ycompare = year_yield / year_yield_base
    year_yield = round(year_yield, 3)
    year_yield_base = round(year_yield_base, 3)
    ycompare = round(ycompare, 3)
    name = gdp.name_of(code)
    print(
        f'Code: {code}, Name:{name}, YYield:{year_yield_base}, YYield:{year_yield}, YieldRaise: {ycompare}')
    return ycompare


def drop_after_count4(code, days):
    # Test sz159919 and sh510330
    moneys = []
    ddr = gdp.ddr_of(code)
    money = 100000
    stock = 0
    drop_count = 0
    buy_count = 0
    last_buy_day = None
    if not days: days = ddr.days
    for index, day in enumerate(days):
        moneys.append(money)
        if stock != 0:
            if gtrade_day.span_of(last_buy_day, day) >= 1:
                money = stock * gdp.open(code, day)
                stock = 0
        else:
            if drop_count == 2:
                last_buy_day = day
                buy_count += 1
                stock = money / gdp.open(code, day)
                money = 0
            else:
                pass

        if gdp.open(code, day) > gdp.close(code, day):
            drop_count += 1
        else:
            drop_count = 0

    if stock != 0:
        money = stock * gdp.close(code, ddr.days[-1])
        moneys[-1] = money
    print(buy_count)
    yield_ = money / 100000
    year_yield = yield_ ** (245 / buy_count)
    original_yield = gdp.close(code, ddr.days[-1]) / gdp.open(code, ddr.days[0])
    year_yield_base = original_yield ** (245 / len(ddr.days))
    ycompare = year_yield / year_yield_base
    year_yield = round(year_yield, 3)
    year_yield_base = round(year_yield_base, 3)
    ycompare = round(ycompare, 3)
    name = gdp.name_of(code)
    print(
        f'Code: {code}, Name:{name}, YYield:{year_yield_base}, YYield:{year_yield}, YieldRaise: {ycompare}')
    # return ycompare
    # print(moneys)
    om = [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 59.218, 989619.992, 989619.992,
          989619.992, 989619.992, 989619.992, 989619.992, 28.309, 991940.254, 991940.254,
          991940.254, 30.251, 984804.211, 984804.211, 984804.211, 984804.211, 64.397, 989715.632,
          989715.632, 44.007, 992183.641, 992183.641, 992183.641, 992183.641, 992183.641, 46.111,
          1011976.909, 1011976.909, 1011976.909, 1011976.909, 34.136, 1022936.578, 1022936.578,
          11.481, 1014150.719, 1014150.719, 1014150.719, 58.573, 1011612.316, 1011612.316,
          1011612.316, 1011612.316, 1011612.316, 1011612.316, 50.644, 1014206.064, 1014206.064,
          18.926, 1019557.975, 1019557.975, 1019557.975, 1019557.975, 1019557.975, 1019557.975,
          1019557.975, 1019557.975, 1019557.975, 1019557.975, 24.428, 1032179.436, 1032179.436,
          1032179.436, 49.997, 1026348.197, 1026348.197, 1026348.197, 1026348.197, 1026348.197,
          1026348.197, 22.163, 1014414.173, 1014414.173, 1014414.173, 1014414.173, 1014414.173,
          1014414.173, 1014414.173, 1014414.173, 1014414.173, 1014414.173, 1014414.173, 47.246,
          986165.98, 986165.98, 986165.98, 986165.98, 986165.98, 986165.98, 986165.98, 31.387,
          1024864.09, 1024864.09, 1024864.09, 1024864.09, 1024864.09]
    om = numpy.array(om)
    om[om<1000] = 0
    om = list(om)
    for day, m1, m2 in zip(days, moneys, om):
        print(day, '\t',m1, '\t', m2)
    return ycompare


def compare():
    c1 = []
    # etf_with_amount = ['sz159919', 'sh510330']
    # codes = ['sh510050']
    # codes = gdp.components_of('sh000016')
    days = gdp.ddr_of('sh510050').days[0:30]
    print(gdp.ddr_of('sh510050').df)
    codes = ['sh510050']
    for code in codes:
        c1.append(drop_after_count1(code, days))
    print('c1:: ', c1)
    # return
    # ##
    # c2 = []
    # for code in codes:
    #     c2.append(drop_after_count4(code, days))
    # # pyplot.plot(c2[0][1])
    # # pyplot.show()
    # # return
    # # scomp = numpy.array(c1) /c2
    # # print(scomp)
    # geo_mean_c1 = geo_mean_overflow(c1)
    # geo_mean_c2 = geo_mean_overflow(c2)
    # print('geo_mean_c1:: ', geo_mean_c1)
    # print('geo_mean_c2:: ', geo_mean_c2)


if __name__ == '__main__':
    compare()
