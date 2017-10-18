from common_stock.common_indicator import ArrayIndicator
from stock_data_manager.ddr_file_cache import read_ddr_fast
from trading.emulation.single_emu_account import SingleEmuAccount


def support_line_emu(df, window_len):
    pass


def do_support_line_emus(codes, window_len):
    for code in codes:
        ddr = read_ddr_fast(code)
        df = ddr.df
        sl_high = ArrayIndicator.is_max_poses(df.high.values, window_len)
        sl_low = ArrayIndicator.is_min_poses(df.low.values, window_len)

        acc = SingleEmuAccount(code, ddr, 10000, 50)







def main():
    do_support_line_emus(['600000.XSHG'], 5)


if __name__ == '__main__':
    main()
