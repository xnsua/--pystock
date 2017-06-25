import bisect
import datetime
import traceback

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from common_stock.stock_indicator.stock_indicator import calc_trend_indicator
from matplotlib.dates import date2num
from matplotlib.gridspec import GridSpec
from stock_data_updater.stock_day_bar_manager import StockUpdater


def _fmt(x, y):
    datestr = x.strftime(f'date:  %y-%m-%d')
    str1 = f'\nvalue: {y[0]:.3f}'
    str2 = f'\nbase:  {y[1]:.3f}'
    return datestr + str1 + str2


class FollowDotCursor(object):
    """Display the x,y location of the nearest data point.
    https://stackoverflow.com/a/4674445/190597 (Joe Kington)
    https://stackoverflow.com/a/13306887/190597 (unutbu)
    https://stackoverflow.com/a/15454427/190597 (unutbu)
    """

    def __init__(self, ax_fig, ax_text, xvals, yvals, ybase_vals, formatter=_fmt,
                 offsets=(-20, 20)):
        self.ax_fig = ax_fig
        self.ax_text = ax_text
        self.plot_data = xvals, (yvals, ybase_vals)
        self.formatter = formatter
        self.offsets = offsets
        self.indicator = calc_trend_indicator(self.plot_data[0], self.plot_data[1][0])
        self.indicator_base = calc_trend_indicator(self.plot_data[0], self.plot_data[1][1])

        normal_factor = yvals[0] / ybase_vals[0]
        normal_ybase_vals = [item * normal_factor for item in ybase_vals]
        relative_normal_factor = yvals[0]
        normal_relative_vals = [x / y * relative_normal_factor for x, y in
                                zip(yvals, normal_ybase_vals)]

        self.relative_indicator = calc_trend_indicator(self.plot_data[0], self.plot_data[1][1])
        ax_fig.grid(True, alpha=0.4)
        # self.fig = ax_fig.figure
        self.ax_fig.xaxis.set_label_position('top')
        ax_fig.plot(xvals, yvals)
        ax_fig.plot(xvals, normal_ybase_vals)
        ax_fig.plot(xvals, normal_relative_vals)
        # ax_fig.legend()

        # mdd = self.plot_max_drawdrop(ax_fig, xvals, yvals[0])
        # self.draw_text(ax_text, {'mdd': mdd})
        self.draw_text()
        self.plot_max_drawdrop()

        self.annotation = self.setup_annotation()
        plt.connect('motion_notify_event', self)

    def draw_text(self):
        indicator = self.indicator
        indicator_base = self.indicator_base
        mdd1 = indicator['mdd_info']

        line1pos = [(x / 10, 0.6) for x in range(0, 10, 1)]
        line2pos = [(x / 10, 0.3) for x in range(0, 10, 1)]
        self.ax_text.text(*line1pos[0], f"YIELD: {indicator['yield_']:.1%}".replace('%', ' %'))
        self.ax_text.text(*line1pos[1],
                          f"Y_YIELD: {indicator['year_yield']:.1%}".replace('%', ' %'),
                          color='r')
        self.ax_text.text(*line1pos[2], f"MDD: {mdd1[0]:.1%}".replace('%', ' %'), color='g')

        self.ax_text.text(*line2pos[0],
                          f"YIELD: {indicator_base['yield_']:.1%}".replace('%', ' %'),
                          alpha=0.5)
        self.ax_text.text(*line2pos[1],
                          f"Y_YIELD: {indicator_base['year_yield']:.1%}".replace('%', ' %'),
                          alpha=0.5)

    def plot_max_drawdrop(self):
        # Plot maxdrawdown info
        mdd_info = self.indicator['mdd_info']
        leftp, rightp, endp = mdd_info[1]

        self.ax_fig.plot(*zip(leftp, rightp), alpha=0.3)
        self.ax_fig.plot(*zip(leftp, endp), alpha=0.3)

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
            annotation = self.annotation
            x, y = self.snap(x, y)
            annotation.xy = x, y[0]
            annotation.set_text(self.formatter(x, y))
            event.canvas.draw()
        except Exception:
            traceback.print_exc()

    def setup_annotation(self):
        """Draw and hide the annotation box."""
        annotation = self.ax_fig.annotate(
            '', xy=(0, 0), ha='left',
            xytext=self.offsets, textcoords='offset points', va='bottom',
            bbox=dict(
                boxstyle='round,pad=0.5', fc='yellow', alpha=0.2),
            arrowprops=dict(
                arrowstyle='->', connectionstyle='arc3,rad=0'))
        return annotation

    # noinspection PyUnusedLocal
    def snap(self, x, y):
        # print(x, y)
        xs = [date2num(item) for item in self.plot_data[0]]
        pos = bisect.bisect_right(xs, x) - 1
        pos = pos if pos > 0 else 0
        val = self.plot_data[0][pos], list(item[pos] for item in self.plot_data[1])
        return val


def plot_stock_info(index_date, values, base_values):
    """
    :param index_date:
    :param base_values:
    :param values: values[0] for stratege value
                   values[1] for base value
    """
    plt.rcParams["font.family"] = "consolas"

    fig = plt.figure(figsize=(16, 4))
    gs = GridSpec(2, 1, height_ratios=[1, 4])

    ax_text = fig.add_subplot(gs[0, 0])
    ax_text.axis('off')
    ax_fig = fig.add_subplot(gs[1, 0])
    fig.tight_layout()
    # fig, ax = plt.subplots(figsize=(16, 4))
    years = mdates.YearLocator()  # every year
    months = mdates.MonthLocator()  # every month
    year_fmt = mdates.DateFormatter('%Y')
    ax_fig.xaxis.set_major_locator(years)
    ax_fig.xaxis.set_major_formatter(year_fmt)
    ax_fig.xaxis.set_minor_locator(months)
    # noinspection PyUnusedLocal
    cursor = FollowDotCursor(ax_fig, ax_text, index_date, values, base_values)
    plt.show()


df = StockUpdater.read_etf_day_data('510900')
dates = [datetime.datetime.strptime(item, '%Y-%m-%d') for item in df.index]
opens = list(df.open)
length = 1000
dates = dates[0:length]
opens = opens[0:length]
high = list(df.high)[0:length]
df2 = StockUpdater.read_etf_day_data('')
plot_stock_info(dates, opens, high)
