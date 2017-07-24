import bisect
import traceback
from typing import List

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date
from matplotlib.gridspec import GridSpec

from common.helper import dt_date_to_dt
from common_stock.trade_day import gtrade_day
from stock_data_updater.data_provider import gdp


# noinspection PyUnusedLocal
class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None


    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print (event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * relx])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * rely])
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion


class StockTrendPlotter(object):
    """Display the x,y location of the nearest data point.
    https://stackoverflow.com/a/4674445/190597 (Joe Kington)
    https://stackoverflow.com/a/13306887/190597 (unutbu)
    https://stackoverflow.com/a/15454427/190597 (unutbu)
    """

    def __init__(self, lines, left_annotations, right_annotations, save_file_name,
                 show_float_annotation=True):
        self.show_float_annotation = show_float_annotation
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
        # self.ax_fig.xaxis_date()
        self.ax_fig.xaxis.set_major_locator(years)
        self.ax_fig.xaxis.set_major_formatter(year_fmt)
        self.ax_fig.xaxis.set_minor_locator(months)
        self.ax_fig.xaxis.set_label_position('top')

        zp = ZoomPan()
        zp.zoom_factory(self.ax_fig, base_scale = 1.1)
        zp.pan_factory(self.ax_fig)

        self.plot_lines2()
        self.plot_texts2()

        # Moving annotation
        self.left_annotations = self.setup_annotation()
        if self.show_float_annotation:
            plt.connect('motion_notify_event', self)

    def show_figure(self):
        plt.show()

    def save_figure(self, filename):
        plt.savefig(filename, format='png')

    def close_figure(self):
        plt.close()

    def plot_lines2(self):
        for line in self.lines:
            if isinstance(line, KLine):
                import mpl_finance
                mpl_finance.candlestick_ochl(self.ax_fig, line.data, width=0.6,
                                             colorup=line.up_color, colordown=line.down_color)
                continue
            ys = line.ys
            if line.plot_bench:
                ratio = line.plot_bench[0] / ys[0]
                ys = [item * ratio for item in ys]

            self.ax_fig.plot(line.xs, ys, color=line.color, alpha=line.alpha,
                             label=line.label, marker = line.marker)
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
        if not self.show_float_annotation:
            return
        assert len(values) == 2, 'Two value allowed, Value and Base'
        show_value0 = values[0]
        show_value1 = values[1]
        datestr = pos.strftime(f'date:  %y-%m-%d')

        str1 = f'\nvalue: {show_value0:.3f}'
        str2 = f'\nbase:  {show_value1:.3f}'
        return datestr + str1 + str2


class LineAndStyle:
    def __init__(self, xs, ys, color, alpha = 1, marker = None, show_value_in_annotaion=False, label='',
                 bench_vals=None):
        self.marker = marker
        self.xs = xs
        self.ys = ys
        self.alpha = alpha
        self.color = color
        self.label = label
        self.show_value_in_annotation = show_value_in_annotaion
        self.plot_bench = bench_vals
        # self.style=


class KLine:
    def __init__(self, data, up_color, down_color):
        self.data = data
        self.up_color = up_color
        self.down_color = down_color


class TextAnnotation:
    def __init__(self, key, value, alpha=1, color='k', formatter=None):
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
                               save_file_name=None, show=False, show_float_annotation=True):
    plotter = StockTrendPlotter(lines_and_style, left_annotation, right_annotation, save_file_name,
                                show_float_annotation)
    if save_file_name:
        plotter.save_figure(save_file_name)
    if show:
        plotter.show_figure()
    plotter.close_figure()


# def plot_test():
    # ddr = gdp.ddr_of('sh510900')
    # ddr = ddr.clip(20170605, gtrade_day.previous(20170710))
    #
    # days = [gtrade_day.int_to_date(item) for item in ddr.days]
    # days_num = list(map(date2num, days))
    # kline = KLine(list(zip(days_num, ddr.open, ddr.close, ddr.high, ddr.low)), up_color='r',
    #               down_color='g')
    # values = ddr.open
    # mdd_x = [datetime.date(2017, 6, 4), datetime.datetime(2017, 6, 8)]
    # mdd_y = [1, 0.8]
    # lines = [
    #     LineAndStyle(days, values, 'b', marker='o', label='Value', show_value_in_annotaion=True),
    #     kline,
    # ]
    # line1annotations = [
    #     TextAnnotation('Key1', 0.1234, 6, 'b', formatter=None),
    #     TextAnnotation('Key2', 0.1234, 6, 'b', formatter=None),
    # ]
    # plot_image_with_annotation(lines, [line1annotations, line1annotations], [line1annotations],
    #                            show=True, save_file_name='d:/tfile.png',
    #                            show_float_annotation=False)

def plot_ddr_with_marker(ddr, markers):
    days = [gtrade_day.int_to_date(item) for item in ddr.days]
    days_num = list(map(date2num, days))
    marker_value = [ ddr.open_of(item) for item in markers ]
    markers = map(gtrade_day.int_to_date, markers)
    markers = list(map(date2num, markers))
    kline = KLine(list(zip(days_num, ddr.open, ddr.close, ddr.high, ddr.low)), up_color='r',
                  down_color='g')
    lines = [
        LineAndStyle(markers, marker_value, 'b', marker='o', label='Value', show_value_in_annotaion=True),
        kline,
    ]
    plot_image_with_annotation(lines, [], [],
                               show=True, save_file_name='d:/tfile.png',
                               show_float_annotation=False)

# def plot_test2():
#     date1 = (2014, 12, 1)  # 起始日期，格式：(年，月，日)元组
#     date2 = (2016, 12, 1)  # 结束日期，格式：(年，月，日)元组
#     ddr = gdp.ddr_of('sh510900')
#     df = ddr.df
#     ddr2 = ddr.clip(20170604, gtrade_day.previous(20170710))
#
#     days = ddr2.days
#     values = ddr2.open
#     mdd_x = [datetime.date(2017, 6, 1), datetime.datetime(2017, 7, 10)]
#     mdd_y = [1, 2]
#     # noinspection PyTypeChecker
#     lines = [
#         LineAndStyle(days, values, 'b', alpha=1, label='Value', show_value_in_annotaion=True),
#         LineAndStyle(mdd_x, mdd_y, 'k', alpha=0.3)
#     ]
#     line1annotations = [
#         TextAnnotation('Key1', 0.1234, 6, 'b', formatter=None),
#         TextAnnotation('Key2', 0.1234, 6, 'b', formatter=None),
#     ]
#     plot_image_with_annotation(lines, [line1annotations, line1annotations], [line1annotations],
#                                show=False, save_file_name='d:/tfile.png')


def main():
    ddr = gdp.ddr_of('sh510900')
    ddr = ddr.tail(200)
    days = [ddr.days[1],ddr.days[3],ddr.days[7],   ddr.days[9] ]
    plot_ddr_with_marker(ddr, days)

if __name__ == '__main__':
    main()
