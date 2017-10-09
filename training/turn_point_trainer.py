import numpy as np

from data_mining.train_features import extract_kline_pren_feature
from stock_data_manager.ddr_file_cache import read_ddr_fast
from stock_data_manager.stock_sector import index_components
from training.training_common import divide_train_and_test, train_model


def train_turn_point_sz50():
    # sz50 成分股
    sz50 = index_components('000016')
    # sz50 = sz50[:5]
    suc_per = []
    # sz50 = ['510050.XSHG']
    for code in sz50:
        print(code)
        ddr = read_ddr_fast(code)
        train_data = extract_kline_pren_feature(ddr.df, window=5)
        train_data, test_data = divide_train_and_test(train_data, 0.80)
        model = train_model(train_data)

        test_data = train_data
        p1 = model.decision_function(test_data[0])
        p1 = p1 > 0
        p2 = model.predict(test_data[0])
        equal = (test_data[1] == p1)
        suc_per.append(np.sum(equal) / equal.size)

    return np.cumprod(suc_per)[-1] ** (1 / len(suc_per))


def main():
    val = train_turn_point_sz50()
    print(val)


if __name__ == '__main__':
    main()
