import pandas as pd

from stock_data_updater.ddr_fast import read_ddr_fast


class StockAxisPlot:
    def __init__(self, ax, df:pd.DataFrame, plot_range=None):
        self.ax = ax
        self.df = df
        self.plot_range =

    def plot(self):
        loc1 = self.df.index.get_loc(self.plot_range[0])
        loc2 = self.df.index.get_loc(self.plot_range[1])
        print(loc1)
        print(loc2)


def main():
    ddr = read_ddr_fast('sh510090')
    print(ddr.df)


if __name__ == '__main__':
    main()


