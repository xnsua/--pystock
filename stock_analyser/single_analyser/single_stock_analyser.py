from common_stock.py_dataframe import DayDataRepr
from stock_analyser.single_analyser.ma_model import MacdModel
from stock_analyser.single_analyser.single_abc_model import SingleAbcModel
from stock_analyser.single_analyser.single_emu_account import SingleEmuAccount
from stock_data_updater.ddr_fast import read_ddr_fast


def single_stock_analyser(ddr: DayDataRepr, model: SingleAbcModel):
    # for loss_stop in [0.2, 0.3, 0.5, 0.7]:
    for loss_stop in [0.5]:
        print('loss stop: ', loss_stop)
        acc = SingleEmuAccount(ddr.code, ddr, 10000, loss_stop=loss_stop / 10)
        acc.model_str = str(model)
        skip_len = model.skip_len
        for index in range(skip_len):
            acc.on_date_begin(index)
            acc.on_date_finished(index, ddr.ochl(index))
        for index in range(skip_len, len(ddr.days)):
            # if ddr.days[index] == 20130502:
            #     print(ddr.closes[index])
            #     print(model.ma[index])
            # if ddr.days[index] == 20130503:
            #     print(ddr.closes[index])
            #     print(model.ma[index])
            acc.on_date_begin(index)
            bs = model.buy_sell_price(index)
            if bs > 0:
                acc.buy(bs)
            elif bs < 0:
                acc.sell(-bs)
            acc.on_date_finished(index, ddr.ochl(index))

        acc.stat.original_earn = ddr.closes[-1] / ddr.closes[skip_len]
        acc.stat.original_year_earn = acc.stat.original_earn ** (245 / (len(ddr.days) - skip_len))

        acc.print_statistic()
        # print(acc.assets)

    return acc


def main():
    code = 'sh510900'
    ddr = read_ddr_fast(code)
    ma_model = MacdModel((29, 37, 9), ddr)
    # acc = single_stock_analyser(ddr, ma_model)
    # ma_model = MaModel(31, ddr, talib.EMA )
    acc = single_stock_analyser(ddr, ma_model)
    # acc.print_hold_period()


if __name__ == '__main__':
    main()
