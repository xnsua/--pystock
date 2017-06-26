import bisect
import traceback

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from common.helper import dt_date_from_str
from matplotlib.dates import date2num
from matplotlib.gridspec import GridSpec
from stock_analyser.stock_indicator.stock_indicator import calculate_trend_indicator
from stock_data_updater.day_data import read_etf_day_data, read_index_day_data


class StockTrendPlotter(object):
    """Display the x,y location of the nearest data point.
    https://stackoverflow.com/a/4674445/190597 (Joe Kington)
    https://stackoverflow.com/a/13306887/190597 (unutbu)
    https://stackoverflow.com/a/15454427/190597 (unutbu)
    """

    def __init__(self, ax_fig, ax_text, plot_data):
        self.ax_fig = ax_fig
        self.ax_text = ax_text
        self.plot_data = plot_data

        self.plot_lines()

        self.draw_text()

        self.plot_max_drawdrop()

        self.annotation = self.setup_annotation()
        plt.connect('motion_notify_event', self)

    def plot_lines(self):
        values = self.plot_data['values']
        normal_base = self.plot_data['normal_base_values']
        ratio = self.plot_data['ratios_values']
        xdata = [dt_date_from_str(item) for item in values.index]
        self.ax_fig.plot(xdata, values, label='values')
        self.ax_fig.plot(xdata, normal_base, label='base')
        self.ax_fig.plot(xdata, ratio, label='ratio')
        self.ax_fig.legend()

    def draw_text(self):
        indicator = self.plot_data['value_attr']
        indicator_base = self.plot_data['base_attr']
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
        indicator = self.plot_data['value_attr']
        mdd_info = indicator['mdd_info']
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
            x, ys = self.snap(x, y)
            annotation.xy = x, ys[0]
            annotation.set_text(self._fmt(x, ys))
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
        # print('xxyy', x, y)
        values = self.plot_data['values']
        base = self.plot_data['base_values']
        ratio = self.plot_data['ratios_values']
        index_date = [dt_date_from_str(item) for item in values.index]
        # xs = [date2num(date) for date in index_date]
        xs = date2num(index_date)
        pos = bisect.bisect_right(xs, x) - 1
        pos = pos if pos > 0 else 0
        # noinspection PyUnresolvedReferences
        x = dt_date_from_str(values.index[pos])
        val = x, (values[pos], base[pos], ratio[pos])
        return val

    def _fmt(self, x, y):
        datestr = x.strftime(f'date:  %y-%m-%d')
        str1 = f'\nvalue: {y[0]:.3f}'
        str2 = f'\nbase:  {y[1]:.3f}'
        return datestr + str1 + str2


def plot_stock_values(plot_values):
    plt.rcParams["font.family"] = "consolas"
    fig = plt.figure(figsize=(16, 4))
    gs = GridSpec(2, 1, height_ratios=[1, 4])
    ax_text = fig.add_subplot(gs[0, 0])
    ax_text.axis('off')
    ax_fig = fig.add_subplot(gs[1, 0])
    ax_fig.grid(True, alpha=0.4)
    fig.tight_layout()
    years = mdates.YearLocator()  # every year
    months = mdates.MonthLocator()  # every month
    year_fmt = mdates.DateFormatter('%Y')
    ax_fig.xaxis.set_major_locator(years)
    ax_fig.xaxis.set_major_formatter(year_fmt)
    ax_fig.xaxis.set_minor_locator(months)
    ax_fig.xaxis.set_label_position('top')
    # noinspection PyUnusedLocal
    cursor = StockTrendPlotter(ax_fig, ax_text, plot_values)
    plt.show()


def plot_trend(value, base):
    val = calculate_trend_indicator(value, base)
    plot_stock_values(val)


def main():
    df_etf = read_etf_day_data('510900')
    df_etf = df_etf.tail(8000)  # print(df_etf.open)
    df_index = read_index_day_data('000001')
    # val = (df_index.loc[df_etf.index, :])
    plot_trend(df_etf.open, df_index.open)


if __name__ == '__main__':
    main()
