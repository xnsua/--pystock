import numpy as np

from common_stock.stock_helper import p_repr


class PredictResult:
    def __init__(self, real, predict):
        self.real = np.asarray(real)
        self.predict = np.asarray(predict)
        self.true_accuracy = 0.
        self.false_accuracy = 0.
        # noinspection PyTypeChecker
        self.total_accuracy = sum(self.real == self.predict) / len(predict)

        self.predict_true_per = sum(predict) / len(predict)

        self.real_per = sum(real) / len(real)
        self.false_per = 1 - self.predict_true_per

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
            self.true_accuracy = tp / (tp + fp)
        else:
            self.true_accuracy = 0

        if tn + fn:
            self.false_accuracy = tn / (tn + fn)
        else:
            self.false_accuracy = 0

        self.tp, self.tn, self.fp, self.fn = tp, tn, fp, fn

    def __repr__(self):
        return f'ClassifyAccuracy:{{ ' \
               f'TrueA: # {p_repr(self.true_accuracy)} #, ' \
               f'TotalA: {p_repr(self.total_accuracy)},' \
               f'}}'
               # f'FalseA: {p_repr(self.false_accuracy)}, ' \
               # f'RealPer: {p_repr(self.real_per)},' \
               # f'TruePer:{p_repr(self.predict_true_per)} ' \


def combine_predict_results(results):
    reals = np.concatenate([item.real for item in results])
    predicts = np.concatenate([item.predict for item in results])
    val = PredictResult(reals, predicts)
    return val


def divide_train_and_test(data, percentage, *, is_random=True):
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


def cross_divide_data(data, number):
    features, labels = data
    sample_cnt = len(features)
    indexes = np.arange(sample_cnt)
    np.random.shuffle(indexes)
    data_list = []
    seps = np.linspace(0, sample_cnt, num=(number + 1), dtype=np.int64)
    for val in zip(seps, seps[1:]):
        index = indexes[val[0]:val[1]]
        features_copy = features.copy()
        labels_copy = labels.copy()
        np.delete(features_copy, index, axis=0)
        np.delete(labels_copy, index, axis=0)

        data_list.append(((features_copy, labels_copy), (features[index, :], labels[index])))
    return data_list


def train_and_analyse(train_data, test_data, train_model):
    model = train_model.fit(*train_data)

    train_predict = model.predict(train_data[0])
    train_predict_result = PredictResult(train_data[1], train_predict)

    test_predict = model.predict(test_data[0])
    test_predict_result = PredictResult(test_data[1], test_predict)

    return train_predict_result, test_predict_result


def train_PD_curve(train_data, test_data, train_model, ):
    """ Analyse the true percentage according to the distance to the hyperplane """
    model = train_model.fit(*train_data)
    predict_distance = model.decision_function(test_data[0])
    pos = np.argsort(predict_distance)[::-1]
    true_cls = test_data[1][pos]

    true_pers = np.cumsum(true_cls) / np.arange(1, len(true_cls) + 1)
    return true_pers


# noinspection PyPep8Naming
def cross_train_and_analyse(train_data, number, model):
    cross_data = cross_divide_data(train_data, number)
    predicts = []
    for train_data, test_data in cross_data:
        val = train_and_analyse(train_data, test_data, model)
        predicts.append(val)
    return combine_predict_results([item[0] for item in predicts]), \
           combine_predict_results([item[1] for item in predicts])


def cross_train_and_analyse_true_predication(train_data, number, model):
    pass
