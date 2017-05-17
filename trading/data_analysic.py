import numpy as np

from data_server.day_data_manager import update_etf_histories


def sort_etf_by_amount():
    df_dict = update_etf_histories()
    etf_amount = []
    for etf, df in df_dict.items():
        df30 = df.tail(30)
        amount = np.mean(df30.close * df30.volume)
        etf_amount.append((etf, amount))
    etf_amount.sort(key=np.operator.itemgetter(1))
    print(etf_amount)
