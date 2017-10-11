from sklearn.svm import LinearSVC

from data_mining.kline_features import KlineFeatures
from data_mining.train_data_provider import TrainDataProvider
from data_mining.training import cross_train_and_analyse


def main():
    data = TrainDataProvider.provide_single(
        '510050.XSHG',
        [
            # KlineFeatures.ochl_features,
         KlineFeatures.day_compare_features,
         ],
        KlineFeatures.is_close_up)
    model = LinearSVC()
    val = cross_train_and_analyse(data, 3, model)
    print(val)

if __name__ == '__main__':
    main()
