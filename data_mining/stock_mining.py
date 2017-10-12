import concurrent.futures

from sklearn.svm import LinearSVC

from common.helper import iterable_extend
from data_mining.kline_features import KlineFeatures
from data_mining.stock_training import cross_train_and_analyse, \
    combine_predict_results
from data_mining.train_data_provider import TrainDataProvider
# def mining_simple_stock_code():
#
#
# class MiningResult:
#     pass
# def svm_mining():
#     codes = rq_data_fetcher.rq_all_stock_code()
#     for code in codes
from stock_data_manager.stock_sector import ksample80


@iterable_extend
def _stock_mining(codes, cross_number=6):
    """ fl_data is feature and lable data """
    date_index, fl_data = TrainDataProvider.provide_single(
        codes,
        [
            KlineFeatures.ochl_features,
            KlineFeatures.day_compare_features,
            # KlineFeatures.volume_percentage,
            # KlineFeatures.fg_day_compare_features_n(1),
        ],
        KlineFeatures.is_close_up)
    model = LinearSVC()
    # model = SVC()
    # val = train_and_analyse(fl_data, cross_number, model)
    val = cross_train_and_analyse(fl_data, cross_number, model)
    return val


def stock_mining(code, cross_number):
    """ For multi-process """
    return _stock_mining(code, cross_number)

def concurrent_run(func, disperse_vals, *args):
    args2 = list(zip(*([args] * len(disperse_vals))))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        val = executor.map(func, disperse_vals, *args2)

    return list(val)


def _print_test_result(result):
    vals = [item[1] for item in result]
    print(vals)


def main():
    codes = ksample80
    codes = codes[0:1]
    # ------- Print run time --------------
    import datetime
    s_time = datetime.datetime.now()
    result = concurrent_run(stock_mining, codes, 5)
    print(datetime.datetime.now() - s_time)

    single_result = [combine_predict_results(item) for item in zip(*result)]
    print(single_result)


if __name__ == '__main__':
    main()
