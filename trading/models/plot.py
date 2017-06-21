import bisect
import datetime
import traceback

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

from data_manager.stock_day_bar_manager import DayBar


def _fmt(x, y):
    datestr = x.strftime(f'date:  %y-%m-%d')
    pstr = datestr
    for name, val in y:
        name = name + ':'
        pstr += f'\n{name:6} {val:.3f}'
    return pstr


class FollowDotCursor(object):
    """Display the x,y location of the nearest data point.
    https://stackoverflow.com/a/4674445/190597 (Joe Kington)
    https://stackoverflow.com/a/13306887/190597 (unutbu)
    https://stackoverflow.com/a/15454427/190597 (unutbu)
    """

    def __init__(self, ax, x, ys, formatter=_fmt, offsets=(-20, 20)):
        # ys = np.asarray(ys, dtype='float')
        # self._points = np.column_stack((x, zip(*y)))
        self.plot_data_names = [item[0] for item in ys]
        ys = [item[1] for item in ys]
        self.plot_data = x, ys
        self.offsets = offsets
        self.formatter = formatter
        self.ax = ax
        self.fig = ax.figure
        self.ax.xaxis.set_label_position('top')
        for i in range(len(ys)):
            self.dot = ax.plot(x, ys[i])
        self.annotation = self.setup_annotation()
        plt.connect('motion_notify_event', self)

    def __call__(self, event):
        try:
            ax = self.ax
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
            annotation.set_text(self.formatter(x, zip(self.plot_data_names, y)))
            event.canvas.draw()
        except Exception as e:
            traceback.print_exc()

    def setup_annotation(self):
        """Draw and hide the annotation box."""
        annotation = self.ax.annotate(
            '', xy=(0, 0), ha='left',
            xytext=self.offsets, textcoords='offset points', va='bottom',
            bbox=dict(
                boxstyle='round,pad=0.5', fc='yellow', alpha=0.75),
            arrowprops=dict(
                arrowstyle='->', connectionstyle='arc3,rad=0'))
        return annotation

    def snap(self, x, y):
        xs = [date2num(item) for item in self.plot_data[0]]
        pos = bisect.bisect_right(xs, x) - 1
        pos = pos if pos > 0 else 0
        val = self.plot_data[0][pos], list(item[pos] for item in self.plot_data[1])
        return val


def plot_stock_info(index_date, values):
    plt.rcParams["font.family"] = "consolas"
    fig, ax = plt.subplots()
    years = mdates.YearLocator()  # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    cursor = FollowDotCursor(ax, dates, values)
    plt.show()


df = DayBar.read_etf_day_data('510900')
dates = [datetime.datetime.strptime(item, '%Y-%m-%d') for item in df.index]
opens = list(df.open)
length = 1000
dates = dates[0:length]
opens = opens[0:length]
high = list(df.high)[0:length]
plot_stock_info(dates, (('open', opens), ('high', high)))
