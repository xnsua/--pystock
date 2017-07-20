import bisect
import datetime
import traceback
from itertools import accumulate
from typing import List

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy
from matplotlib.dates import date2num, num2date
from matplotlib.gridspec import GridSpec

from common.helper import dt_date_to_dt
from common_stock.trade_day import gtrade_day


class StockTrendPlotter(object):
    """Display the x,y location of the nearest data point.
    https://stackoverflow.com/a/4674445/190597 (Joe Kington)
    https://stackoverflow.com/a/13306887/190597 (unutbu)
    https://stackoverflow.com/a/15454427/190597 (unutbu)
    """

    def __init__(self, lines, left_annotations, right_annotations, save_file_name):
        self.lines = lines  # type: List[LineAndStyle]
        self.left_annotations = left_annotations
        self.right_annoations = right_annotations
        self.save_file_name = save_file_name

        # Figure configuration
        plt.rcParams["font.family"] = "consolas"
        self.fig = plt.figure(figsize=(16, 4))
        gs = GridSpec(2, 1, height_ratios=[1, 4])
        self.ax_text = self.fig.add_subplot(gs[0, 0])
        self.ax_text.axis('off')
        self.ax_fig = self.fig.add_subplot(gs[1, 0])
        self.ax_fig.grid(True, alpha=0.4)
        self.fig.tight_layout()
        years = mdates.YearLocator()  # every year
        months = mdates.MonthLocator()  # every month
        year_fmt = mdates.DateFormatter('%Y')
        self.ax_fig.xaxis.set_major_locator(years)
        self.ax_fig.xaxis.set_major_formatter(year_fmt)
        self.ax_fig.xaxis.set_minor_locator(months)
        self.ax_fig.xaxis.set_label_position('top')

        self.plot_lines2()
        self.plot_texts2()

        # Moving annotation
        self.left_annotations = self.setup_annotation()
        plt.connect('motion_notify_event', self)

    def show_figure(self):
        plt.show()

    def save_figure(self, filename):
        plt.savefig(filename, format='png')

    def close_figure(self):
        plt.close()

    def plot_lines2(self):
        for line in self.lines:
            ys = line.ys
            if line.plot_bench:
                ratio = line.plot_bench[0] / ys[0]
                ys = [item * ratio for item in ys]

            self.ax_fig.plot(line.xs, ys, color=line.color, alpha=line.alpha,
                             label=line.label)
        self.ax_fig.legend()

    def plot_texts2(self):
        line1pos = [(x / 10, 0.6) for x in range(0, 10, 1)]
        line2pos = [(x / 10, 0.3) for x in range(0, 10, 1)]
        line3pos = [(x / 10, 0.0) for x in range(0, 10, 1)]
        lines = [line1pos, line2pos, line3pos]
        for i_row, row in enumerate(self.left_annotations):
            line = lines[i_row]
            for pos, item in enumerate(row):
                if item.formatter is None:
                    text = f'{item.key}: {item.value}'
                else:
                    text = item.formatter(item.key, item.value)
                self.ax_text.text(*line[pos], text, color=item.color, alpha=item.alpha)

        for i_row, row in enumerate(self.right_annoations):
            line = lines[i_row]
            for pos, item in enumerate(row):
                if item.formatter is None:
                    text = f'{item.key}: {item.value}'
                else:
                    text = item.formatter(item.key, item.value)
                self.ax_text.text(*line[-pos - 1], text, color=item.color, alpha=item.alpha)

    def __call__(self, event):
        try:
            ax = self.ax_fig
            # event.inaxes is always the current axis. If you use twinx, ax could be
            # a different axis.
            if event.inaxes == ax:
                x, y = event.xdata, event.ydata
            elif event.inaxes is None:
                return
            else:
                inv = ax.transData.inverted()
                x, y = inv.transform([(event.x, event.y)]).ravel()
            annotation = self.left_annotations
            x_axis, xpos, yvals = self.snap(x, y)
            annotation.xy = (x_axis, yvals[0])
            annotation.set_text(self._format_show_values(xpos, yvals))
            event.canvas.draw()
        except Exception:
            traceback.print_exc()

    def setup_annotation(self):
        """Draw and hide the annotation box."""
        annotation = self.ax_fig.annotate(
            '', xy=(0, 0), ha='left',
            xytext=(-20, 20), textcoords='offset points', va='bottom',
            bbox=dict(
                boxstyle='round,pad=0.5', fc='yellow', alpha=0.2),
            arrowprops=dict(
                arrowstyle='->', connectionstyle='arc3,rad=0'))
        return annotation

    # noinspection PyUnusedLocal
    def snap(self, x, y):
        pos_date = num2date(x).date()
        line1 = self.lines[0]
        pos = bisect.bisect_right(line1.xs, pos_date) - 1
        pos = max(0, pos)
        pos_date = line1.xs[pos]
        pos_axis = date2num(dt_date_to_dt(pos_date))

        yvals = []
        for line in self.lines:
            if line.show_value_in_annotation:
                yvals.append(line.ys[pos])
        return pos_axis, pos_date, yvals

    def _format_show_values(self, pos, values):
        assert len(values) == 2, 'Two value allowed, Value and Base'
        show_value0 = values[0]
        show_value1 = values[1]
        datestr = pos.strftime(f'date:  %y-%m-%d')

        str1 = f'\nvalue: {show_value0:.3f}'
        str2 = f'\nbase:  {show_value1:.3f}'
        return datestr + str1 + str2


class LineAndStyle:
    def __init__(self, xs, ys, color, alpha, show_value_in_annotaion=False, label='',
                 bench_vals=None):
        self.xs = xs
        self.ys = ys
        self.alpha = alpha
        self.color = color
        self.label = label
        self.show_value_in_annotation = show_value_in_annotaion
        self.plot_bench = bench_vals


class TextAnnotation:
    def __init__(self, key, value, alpha = 1, color='k', formatter=None):
        self.key = key
        self.value = value
        self.alpha = alpha
        self.color = color
        self.formatter = formatter

    @staticmethod
    def empty_annotation():
        return TextAnnotation('', '', alpha=0, color='b')


class LeftAlignTextAnnotations:
    def __init__(self, annotations: List[List[TextAnnotation]]):
        self.annotations = annotations


class RightAlignTextAnnotations:
    def __init__(self, annotations: List[List[TextAnnotation]]):
        self.annotiation = annotations


def plot_image_with_annotation(lines_and_style: List[LineAndStyle],
                               left_annotation,
                               right_annotation,
                               save_file_name=None, show=False):
    plotter = StockTrendPlotter(lines_and_style, left_annotation, right_annotation, save_file_name)
    if save_file_name:
        plotter.save_figure(save_file_name)
    if show:
        plotter.show_figure()
    plotter.close_figure()


def plot_test():
    days = gtrade_day.close_range_list(20170601, 20170710)
    days = list(map(gtrade_day.int_to_date, days))
    values = list(accumulate(numpy.random.randn(len(days))))
    # pyplot.plot(days, list(values))
    # pyplot.show()
    values2 = numpy.array(values) / 2
    # pyplot.plot(days, list(values))
    # pyplot.plot(days, list(values2))
    # pyplot.show()
    mdd_x = [datetime.date(2017, 6, 1), datetime.datetime(2017, 7, 10)]
    mdd_y = [1, 2]
    lines = [
        LineAndStyle(days, values, 'b', alpha=1, label='Value', show_value_in_annotaion=True),
        LineAndStyle(days, values2, 'k', alpha=0.3, label='Base', show_value_in_annotaion=True),
        LineAndStyle(mdd_x, mdd_y, 'k', alpha=0.3)
    ]
    line1annotations = [
        TextAnnotation('Key1', 0.1234, 6, 'b', formatter=None),
        TextAnnotation('Key2', 0.1234, 6, 'b', formatter=None),
    ]
    plot_image_with_annotation(lines, [line1annotations, line1annotations], [line1annotations],
                               show=False, save_file_name='d:/tfile.png')


def main():
    plot_test()
    # df_etf = read_etf_day_data('510900')
    # # print(df_etf)
    # df_etf = df_etf.tail(80)
    # df_etf.index = df_etf.index.map(gtrade_day.str_to_int)
    # print(df_etf)
    # # print(df_etf.open)
    # # df_index = read_index_day_data('000001')
    # # val = (df_index.loc[df_etf.index, :])
    # plot_test(df_etf.open, None)


if __name__ == '__main__':
    main()
