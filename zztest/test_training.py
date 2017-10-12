import numpy as np

from data_mining.stock_training import cross_divide_data, divide_train_and_test, PredictResult, \
    combine_predict_results


def test_cross_divide_train_and_test():
    feature = np.asarray([
        [1., 1.],
        [2., 2.],
        [3., 3.],
        [4., 4.],
        [5., 5.],
        [6., 6.],
        [7., 7.],
    ])
    label = np.asarray([1, 2, 3, 4, 5, 6, 7.])

    val = cross_divide_data((feature, label), 3)

    for item in val:
        f1 = item[0][:, 0]
        assert np.allclose(f1, item[1])

    label2 = np.concatenate(tuple(item[1] for item in val))
    label2.sort()
    assert np.allclose(label2, label)


def test_divide_train_and_test():
    feature = np.asarray([
        [1., 1.],
        [2., 2.],
        [3., 3.],
        [4., 4.],
        [5., 5.],
        [6., 6.],
        [7., 7.],
    ])
    label = np.asarray([1, 2, 3, 4, 5, 6, 7.])

    val = divide_train_and_test((feature, label), 0.6, is_random=True)
    assert len(val) == 2
    train, test = val
    assert len(train[1]) == 4
    assert len(train[1]) + len(test[1]) == len(feature)

    for item in val:
        f1 = item[0][:, 0]
        assert np.allclose(f1, item[1])

    label2 = np.concatenate(tuple(item[1] for item in val))
    label2.sort()
    assert np.allclose(label2, label)


def test_combine_predict_results():
    real1 = [True]
    predict1 = [False]
    predict_result1 = PredictResult(real1, predict1)
    real2 = [True]
    predict2 = [True]
    predict_result2 = PredictResult(real2, predict2)
    predict3 = combine_predict_results((predict_result1, predict_result2))
    print(predict3)


