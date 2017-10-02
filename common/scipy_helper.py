import numpy
import pandas

pandas.options.display.max_rows = 20


def set_pandas_max_rows(rows):
    pandas.options.display.max_rows = rows


pdDF = pandas.DataFrame
pdSr = pandas.Series

nparr = numpy.array
np = numpy

