import pandas

pandas.options.display.max_rows = 8


def set_pandas_max_rows(rows):
    pandas.options.display.max_rows = rows


pdDF = pandas.DataFrame
