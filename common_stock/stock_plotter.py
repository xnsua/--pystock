import traceback

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import patches
from matplotlib.collections import PatchCollection
from matplotlib.pyplot import Axes
from matplotlib.ticker import FuncFormatter

from common.numpy_helper import np_shift
from stock_data_manager.ddr_file_cache import read_ddr_fast
from stock_data_manager.stock_data.int_trade_day import intday_arr_of


class StockAxisPlot:
    def __init__(self, figaxes, df: pd.DataFrame, plot_range=None, kline_width=0.7):
        plt.rcParams["font.family"] = "consolas"
        self.fig = figaxes[0]
        self.ax = figaxes[1]  # type: Axes
        self.df = df
        self.kline_width = kline_width
        self.plot_range = plot_range
        if plot_range is None:
            self.plot_range = intday_arr_of(df.index[0], df.index[-1])
        elif len(plot_range) == 2:
            self.plot_range = intday_arr_of(*plot_range)

        self.plot_range = np.asarray(self.plot_range)
        self.date_len = len(self.plot_range)
        self.xs = np.arange(self.date_len)

        self.x_tick_labels()

        self.time_pos_info = None

        self.lines = []

        self.annotation = None

    def add_plot_lines(self, name, series, **linestyle):
        assert isinstance(series, pd.Series)
        values = series[self.plot_range].values
        self.lines.append((name, values, linestyle))

    def x_tick_labels(self):
        arr = np.mod(self.plot_range, 10000)
        is_year_firsts = (arr - np_shift(arr, 1, fill_value=0)) < 0

        arr = np.mod(self.plot_range, 100)
        is_month_firsts = (arr - np_shift(arr, 1, fill_value=0)) < 0
        yposes = self.xs[is_year_firsts]
        mposes = self.xs[is_month_firsts]
        self.time_pos_info = yposes, mposes
        return yposes, mposes

    def plot(self):
        if self.df is not None:
            df2 = self.df.loc[self.plot_range, :]
            opens = df2.open.values
            closes = df2.close.values
            highs = df2.high.values
            lows = df2.low.values
            rect_bottoms = np.minimum(opens, closes)
            rect_heights = np.abs(opens - closes)
            rect_is_ups = closes > np.roll(closes, 1)
            rect_lefts = np.arange(len(opens)) - self.kline_width / 2

            patch_list = []
            width = self.kline_width
            for left, bottom, height, isup in zip(rect_lefts, rect_bottoms, rect_heights,
                                                  rect_is_ups):
                face_color = 'r' if isup else 'g'
                patch_list.append(
                    patches.Rectangle((left, bottom), width, height, facecolor=face_color,
                                      fill=True))
            self.ax.add_collection(PatchCollection(patch_list, match_original=True))

            bool_mask = np.isclose(opens, closes)
            stay_days = np.arange(len(self.xs))[bool_mask]
            stay_opens = opens[bool_mask]
            self.ax.hlines(stay_opens, stay_days - self.kline_width / 2,
                           stay_days + self.kline_width / 2, colors=['k'] * len(stay_days))

            colors = np.asarray(['g'] * len(self.xs))
            colors[rect_is_ups] = 'r'
            self.ax.vlines(self.xs, lows, highs, colors=colors)

            for label, data, style_dict in self.lines:
                self.ax.plot(data, label=label, **style_dict)

            self.set_x_y_lim()

            def major_formatter(x, pos):
                if 0 <= x < self.date_len:
                    if pos is not None:
                        return str(self.plot_range[int(x)] // 10000)
                    else:
                        return str(self.plot_range[int(x)])

            yticks, mticks = self.x_tick_labels()
            # self.ax.xaxis.set_ticks(mticks, minor=True)
            # self.ax.xaxis.set_ticklabels(self.plot_range[mticks], minor=True)
            self.ax.xaxis.set_ticks(yticks, minor=False)
            self.ax.xaxis.set_ticklabels(self.plot_range[yticks], minor=False)
            # self.ax.xaxis.set_minor_formatter(FuncFormatter(minor_formatter))
            self.ax.xaxis.set_major_formatter(FuncFormatter(major_formatter))
            self.ax.xaxis.set_label_text(
                str(self.plot_range[0]) + ' - ' + str(self.plot_range[-1]))

            self.fig.canvas.mpl_connect('motion_notify_event', self.mouse_move)

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
        o = round(self.df.open.values[xpos],3)
        c = round(self.df.close.values[xpos],3)
        h = round(self.df.high.values[xpos],3)
        l = round(self.df.low.values[xpos],3)
        text = f' open: {o}\n' \
               f'close: {c}\n' \
               f' high: {h}\n' \
               f'  low: {l}\n'
        for name, data, _ in self.lines:
            text += f'{name: >5}' + ': ' + str(round(data[xpos],3))
        return text

    def set_x_y_lim(self):
        # ymin = np.min(self.df.low.values)
        ymin = np.min(self.df.low.values)
        ymax = np.max(self.df.high.values)
        self.ax.set_ylim([ymin * 0.9, ymax * 1.05])
        self.ax.set_xlim([0, self.date_len])


def main():
    ddr = read_ddr_fast('510050.XSHG')
    # ddr = ddr.tail(1000)
    # plot_range = ddr.df.index[10], ddr.df.index[20]
    # print(plot_range)
    fig, ax = plt.subplots()
    val = StockAxisPlot((fig, ax), ddr.df)
    val.add_plot_lines('test', ddr.df.high + 0.2, color='b')
    val.plot()
    plt.show()


if __name__ == '__main__':
    main()
