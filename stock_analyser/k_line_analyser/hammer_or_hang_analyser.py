from stock_analyser.k_line_analyser.hammer_or_hang import calc_hammer_or_hang
from stock_analyser.plot import plot_kline_with_marker
from stock_data_updater.data_provider import data_provider


def analyser(stock_code):
    ddr = data_provider.ddr_of(stock_code).tail(300)
    markers = calc_hammer_or_hang(ddr)
    plot_kline_with_marker(ddr,markers, save_filename= 'd:/tfile.png')


def main():
    analyser('sh510050')


if __name__ == '__main__':
    main()

