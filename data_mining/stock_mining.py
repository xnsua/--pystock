from sklearn.svm import LinearSVC

from data_mining.kline_features import KlineFeatures
from data_mining.train_data_provider import TrainDataProvider
from data_mining.training import cross_train_and_analyse


class MiningResult:
    pass

# def svm_mining():
#     codes = rq_data_fetcher.rq_all_stock_code()
#     for code in codes

def single_stock_mining(stock_code):
    data = TrainDataProvider.provide_single(
        stock_code,
        [
            # KlineFeatures.ochl_features,
            KlineFeatures.day_compare_features,
        ],
        KlineFeatures.is_close_up)
    model = LinearSVC()
    val = cross_train_and_analyse(data,6, model)
    print(sum(val) / len(val))


def main():
    codes = ['159915.XSHE', '510050.XSHG','510090.XSHG', '510900.XSHG', '000039.XSHG']
    codes = codes[:1]
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
        val = cross_train_and_analyse(data,6, model)
        print(val)
        # ddr = read_ddr_fast(code)
        # val = ddr.close_nparr - np_shift(ddr.close_nparr,1, fill_value=0) >0
        # print(sum(val) / len(val))



if __name__ == '__main__':
    main()
