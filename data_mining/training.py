import numpy as np

from common_stock.stock_helper import p_repr


class PredictResult:
    def __init__(self, real, predict):
        self.real = real
        self.predict = predict
        self.true_per = 0.
        self.false_per = 0.
        # noinspection PyTypeChecker
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


def divide_train_and_test(data, percentage, is_random):
    feature, label = data

    data_len = len(feature)
    train_len = int(data_len * percentage)

    if is_random:
        indexes = np.arange(data_len)
        np.random.shuffle(indexes)
        train_index = indexes[:train_len]
        test_index = indexes[train_len:]

        return (feature[train_index], label[train_index]), (feature[test_index], label[test_index])
    else:
        return (feature[:train_len], label[:train_len]), (feature[train_len:], label[train_len:])


def train_and_analyse(train_data, test_data, train_model):
    model = train_model.fit(train_data)

    train_predict = model.predict(train_data[0])
    train_predict_result = PredictResult(train_predict, train_data[1])

    test_predict = model.predict(test_data[0])
    test_predict_result = PredictResult(test_predict, test_data[1])

    return train_predict_result, test_predict_result
