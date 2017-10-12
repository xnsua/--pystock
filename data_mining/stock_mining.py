import numpy as np
from sklearn.svm import LinearSVC

from data_mining.kline_features import KlineFeatures
from data_mining.stock_training import cross_train_and_analyse
from data_mining.train_data_provider import TrainDataProvider


# def mining_simple_stock_code():
#
#
# class MiningResult:
#     pass
# def svm_mining():
#     codes = rq_data_fetcher.rq_all_stock_code()
#     for code in codes
def stock_mining(stock_codes):
    stock_codes = np.asarray([stock_codes]).flatten()
    predict_results = []
    for code in stock_codes:
        data = TrainDataProvider.provide_single(
            code,
            [
                # KlineFeatures.ochl_features,
                KlineFeatures.day_compare_features,
            ],
            KlineFeatures.is_close_up)
        model = LinearSVC()
        val = cross_train_and_analyse(data,6, model)
        predict_results.append(val)
    return predict_results
val = stock_mining(['510900.XSHG'])
print(val)
1/0

def main():
    codes = ['159915.XSHE', '510050.XSHG','510090.XSHG', '510900.XSHG', '000039.XSHG']
    codes = codes[:2]
    for code in codes:
        data = TrainDataProvider.provide_single(
            code,
            [
                # KlineFeatures.ochl_features,
             KlineFeatures.day_compare_features,
             ],
            KlineFeatures.is_close_up)
        model = LinearSVC()
        # train_data, test_data = divide_train_and_test(data, percentage=0.7, is_random=True)
        # val = train_and_analyse_true(train_data, test_data , model)
        # ------- Print run time --------------
        import datetime
        s_time = datetime.datetime.now()
        val = cross_train_and_analyse(data, 6, model)
        print(datetime.datetime.now() - s_time)


        print(val)
        # ddr = read_ddr_fast(code)
        # val = ddr.close_nparr - np_shift(ddr.close_nparr,1, fill_value=0) >0
        # print(sum(val) / len(val))



if __name__ == '__main__':
    main()
