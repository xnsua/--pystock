import traceback

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import patches
from matplotlib.collections import PatchCollection
from matplotlib.pyplot import Axes
from matplotlib.ticker import FuncFormatter

from common.numpy_helper import np_shift
from common.scipy_helper import pdSr
from common_stock.common_indicator import ArrayIndicator
from stock_data_manager.ddr_file_cache import read_ddr_fast
from stock_data_manager.stock_data.int_trade_day import intday_arr_of


class StockAxisPlot:
    def __init__(self, figaxes, df: pd.DataFrame, code=None, kline_width=0.7):
        self.code = code
        plt.rcParams["font.family"] = "consolas"
        self.fig = figaxes[0]
        self.ax = figaxes[1]  # type: Axes
        self.df = df
        self.kline_width = kline_width

        self.index_to_intday = intday_arr_of(df.index[0], df.index[-1])
        self.index_to_intday = pdSr(index=self.index_to_intday,
                                    data=np.arange(len(self.index_to_intday)))
        self.intday_to_index = self.index_to_intday[df.index]
        self.index_to_intday = pdSr(index=self.intday_to_index.values,
                                    data=self.intday_to_index.index.values)
        self.df_index = self.intday_to_index[df.index]

        self.date_len = len(self.index_to_intday)
        self.xs = self.intday_to_index.values

        self.x_tick_labels()

        self.time_pos_info = None

        self.lines = []
        self.scatter_points = []

        self.annotation = None

        self.hold_days = None

    def add_plot_lines(self, name, series: pdSr, **linestyle):
        assert isinstance(series, pd.Series)
        values = series[self.index_to_intday].values
        self.lines.append((name, values, linestyle))

    def add_scatter_point(self, name, series: pdSr, **linestyle):
        assert isinstance(series, pd.Series)
        self.scatter_points.append((name, series, linestyle))

    def add_hold_info(self, hold_days):
        self.hold_days = hold_days

    def x_tick_labels(self):
        arr = np.mod(self.index_to_intday, 10000)
        is_year_firsts = (arr - np_shift(arr, 1, fill_value=0)) < 0

        arr = np.mod(self.index_to_intday, 100)
        is_month_firsts = (arr - np_shift(arr, 1, fill_value=0)) < 0
        yposes = self.xs[is_year_firsts]
        mposes = self.xs[is_month_firsts]
        self.time_pos_info = yposes, mposes
        return yposes, mposes

    def plot(self):
        if self.df is not None:
            df2 = self.df
            opens = df2.open.values
            closes = df2.close.values
            highs = df2.high.values
            lows = df2.low.values
            rect_bottoms = np.minimum(opens, closes)
            rect_heights = np.abs(opens - closes)
            rect_is_ups = closes > np.roll(closes, 1)
            rect_lefts = self.intday_to_index.values - self.kline_width / 2

            patch_list = []
            width = self.kline_width
            for left, bottom, height, isup in zip(rect_lefts, rect_bottoms, rect_heights,
                                                  rect_is_ups):
                face_color = 'r' if isup else 'g'
                patch_list.append(
                    patches.Rectangle((left, bottom), width, height, facecolor=face_color,
                                      fill=True))
            self.ax.add_collection(PatchCollection(patch_list, match_original=True))

            patch_list = []
            for buy_st, sell_st in self.hold_days:
                buy_st = self.intday_to_index[buy_st]
                sell_st = self.intday_to_index[sell_st]
                patch_list.append(
                    patches.Rectangle((buy_st, 0), sell_st - buy_st, 1000, facecolor='y',
                                      fill=True, alpha=0.2)
                )

            self.ax.add_collection(PatchCollection(patch_list, match_original=True))

            bool_mask = np.isclose(opens, closes)
            stay_days = self.intday_to_index[bool_mask]
            stay_opens = opens[bool_mask]
            self.ax.hlines(stay_opens, stay_days - self.kline_width / 2,
                           stay_days + self.kline_width / 2, colors=['k'] * len(stay_days))

            colors = np.asarray(['g'] * len(self.xs))
            colors[rect_is_ups] = 'r'
            self.ax.vlines(self.xs, lows, highs, colors=colors)

            for label, data, style_dict in self.lines:
                self.ax.plot(data, label=label, **style_dict)
            for label, data, style_dict in self.scatter_points:
                sr = pdSr(data=self.index_to_intday)
                pos = sr[sr.isin(data.index)]
                self.ax.scatter(pos.index.values, data.values, label=label, **style_dict)

            self.set_x_y_lim()

            def major_formatter(x, pos_):
                # pos_ is not used by user
                try:
                    if 0 <= x < self.date_len:
                        return str(self.index_to_intday[int(x)])
                except:
                    traceback.print_exc()

            yticks, mticks = self.x_tick_labels()
            # self.ax.xaxis.set_ticks(mticks, minor=True)
            # self.ax.xaxis.set_ticklabels(self.plot_range[mticks], minor=True)
            self.ax.xaxis.set_ticks(yticks, minor=False)
            self.ax.xaxis.set_ticklabels(self.index_to_intday[yticks], minor=False)
            # self.ax.xaxis.set_minor_formatter(FuncFormatter(minor_formatter))
            self.ax.xaxis.set_major_formatter(FuncFormatter(major_formatter))
            self.ax.xaxis.set_label_text(
                str(self.index_to_intday.iat[0]) + ' - ' + str(self.index_to_intday.iat[-1]))

            self.fig.canvas.mpl_connect('motion_notify_event', self.mouse_move)

            self.fig.set_size_inches(15, 4)
            self.fig.tight_layout()

    def mouse_move(self, event):
        try:
            if not self.annotation:
                self.annotation = self.ax.annotate("Test 1", xy=(0.03, 0.97),
                                                   xycoords="axes fraction",
                                                   va="top", ha="left")
            # print(' x=%d, y=%d, xdata=%f, ydata=%f' %
            #       ( event.x, event.y, event.xdata, event.ydata))
            # return annotation
            self.annotation.set_text(self.annotation_text(event.xdata))
            event.canvas.draw()
        except Exception:
            traceback.print_exc()

    def annotation_text(self, xpos):
        if xpos is None:
            return
        xpos = int(xpos)
        if not 0 <= xpos < self.date_len:
            return
        day = self.index_to_intday[xpos]
        o = round(self.df.open[day], 3)
        c = round(self.df.close[day], 3)
        h = round(self.df.high[day], 3)
        l = round(self.df.low[day], 3)
        text = f' code: {self.code}\n' \
               f' open: {o}\n' \
               f'close: {c}\n' \
               f' high: {h}\n' \
               f'  low: {l}\n'
        for name, data, _ in self.lines:
            text += f'{name: >5}' + ': ' + str(round(data[xpos], 3))

        for name, data, _ in self.scatter_points:
            try:
                text += f'{name: >5}' + ': ' + str(round(data[day], 3))
            except KeyError:
                pass

        return text

    def set_x_y_lim(self):
        # ymin = np.min(self.df.low.values)
        ymin = np.min(self.df.low.values)
        ymax = np.max(self.df.high.values)
        self.ax.set_ylim([ymin * 0.9, ymax * 1.05])
        self.ax.set_xlim([0, self.date_len])


def plot_df_with_min_max(df):
    fig, ax = plt.subplots()
    val = StockAxisPlot((fig, ax), df)
    is_min = ArrayIndicator.is_min_poses(df.low.values, 5)
    is_max = ArrayIndicator.is_max_poses(df.high.values, 5)
    pos_shift = (max(df.high) - min(df.low)) / 30

    is_min_sr = df.low[is_min]
    is_max_sr = df.high[is_max]

    val.add_scatter_point('test', is_min_sr - pos_shift, color='b', marker='^')
    val.add_scatter_point('test', is_max_sr + pos_shift, color='b', marker='v')
    val.plot()
    plt.show()


def main():
    ddr = read_ddr_fast('510050.XSHG')
    ddr = ddr.tail(100)
    plot_df_with_min_max(ddr.df)


if __name__ == '__main__':
    main()
