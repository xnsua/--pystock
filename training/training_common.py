import numpy as np
from sklearn import svm


class TrainStatistics:
    def __init__(self, real, predict):
        self.real = real
        self.predict = predict
        self.true_per = 0
        self.false_per = 0

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


def divide_train_and_test(train_data, percentage, is_random):
    feature, label = train_data

    data_len = len(feature)
    train_len = data_len * percentage

    if is_random:
        indexes = np.arange(data_len)
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


def train_model(data):
    clf = svm.LinearSVC()
    model = clf.fit(data[0], data[1])
    return model


def train_and_test(data, is_random):
    train, test = divide_train_and_test(data, is_random=is_random)
    model = train_model(data)
    test_success = model.predict(test[0])
    trstat = TrainStatistics(test[1], test_success)
    return trstat


def main():
    pass


if __name__ == '__main__':
    main()
