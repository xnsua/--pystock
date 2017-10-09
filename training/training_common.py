import numpy as np
from sklearn import svm

from common_stock.stock_helper import p_repr


class PredictResult:
    def __init__(self, real, predict):
        self.real = real
        self.predict = predict
        self.true_per = 0.
        self.false_per = 0.
        self.error_per = sum(real == predict) / len(predict)

        self.calc()

        self.tp = None
        self.tn = None
        self.fp = None
        self.fn = None

    def calc(self):
        tp = 0
        tn = 0

        fp = 0
        fn = 0

        for x, y in zip(self.real, self.predict):
            if x == y:
                if x:
                    tp += 1
                else:
                    tn += 1
            else:
                if y:
                    fp += 1
                else:
                    fn += 1
        if tp + fp:
            self.true_per = tp / (tp + fp)
        else:
            self.true_per = 0

        if tn + fn:
            self.false_per = tn / (tn + fn)
        else:
            self.false_per = 0

        self.tp, self.tn, self.fp, self.fn = tp, tn, fp, fn

    def __repr__(self):
        return f'ClassifyAccuracy:{{ ' \
               f'True: {p_repr(self.true_per)}, ' \
               f'False: {p_repr(self.false_per)}, ' \
               f'Total: {p_repr(self.error_per)} }}'


def divide_train_and_test(train_data, percentage, is_random):
    feature, label = train_data

    data_len = len(feature)
    train_len = int(data_len * percentage)

    if is_random:
        indexes = np.arange(data_len)
        np.random.shuffle(indexes)
        train_index = indexes[:train_len]
        test_index = indexes[train_len:]

        return (feature[train_index], label[train_index]), (feature[test_index], label[test_index])
    else:
        #
        return (feature[:train_len], label[:train_len]), (feature[train_len:], label[train_len:])


def combine_train_datas(train_datas):
    zip_value = list(zip(*train_datas))
    datas = [val for item in zip_value[0] for val in item]
    labels = [val for item in zip_value[1] for val in item]
    return datas, labels


def train_model(data, is_linear):
    if is_linear:
        clf = svm.LinearSVC()
    else:
        clf = svm.SVC()
    model = clf.fit(data[0], data[1])
    return model


def train_and_analyse_result(data, is_random_data, is_linear_svc, train_percentage):
    fl_train, fl_test = divide_train_and_test(data, is_random=is_random_data,
                                        percentage=train_percentage)
    model = train_model(fl_train, is_linear=is_linear_svc)

    # Calc train result
    train_part = fl_train[0][:200]
    train_label_part = fl_train[1][:200]

    train_predict = model.predict(train_part)
    train_predict_stat = PredictResult(train_label_part, train_predict)

    test_predict = model.predict(fl_test[0])
    test_predict_stat = PredictResult(fl_test[1], test_predict)
    return train_predict_stat, test_predict_stat
