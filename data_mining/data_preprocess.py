import numpy

class MissingValue:
    @staticmethod
    def handle_df_missing_values(df):
        df = df.mask(df < 0.000001, numpy.nan)
        df.fillna(method='ffill', axis=0, inplace=True)
        volume = df.volume
        df.drop('volume', axis=1, inplace=True)
        df.high = df.max(axis=1)
        df.low = df.min(axis=1)
        df['volume'] = volume.values
        return df