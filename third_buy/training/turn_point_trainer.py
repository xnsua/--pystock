from sklearn import svm

from common_stock.stock_data.stock_constant import ksz50_com
from stock_data_updater.data_provider import ddr_pv
from third_buy.training.turn_point_data import get_up_turn_train_data


# X = [(0, 0), (1, 1)]
# y = [0, 1]
# clf = svm.SVC()
# val = clf.fit(X, y)
# print(type(val))
# val = clf.predict([[0., 0.], [2., 2.]])
# print(val)
# # val = clf.decision_function([[1.,0.]])
# # print(val)
# joblib.dump(clf, 'd:/tt.model')
#
# model2 = joblib.load('d:/tt.model')
# val = clf.predict([[0., 0.], [2., 2.]])
# print(val)


def train_model(data):
    clf = svm.SVC()
    model = clf.fit([*data[0], *data[1]],
                    [*[0] * len(data[0]), *[1] * len(data[1])])
    return model


def train_turn_point_sz50(save_path):
    # sz50 成分股
    sz50 = ksz50_com
    sz50 = sz50[:1]
    for code in sz50:
        ddr = ddr_pv.ddr_of(code)
        train_data = get_up_turn_train_data(ddr, window_len=5)
        model = train_model(train_data)
        print(len(train_data[0]))
        print(len(train_data[1]))
        p1 = model.decision_function(train_data[0])
        print(p1)
        # joblib.dump(model, 'd:/tt.model')
        break



def main():
    train_turn_point_sz50('d:/tt.model')


if __name__ == '__main__':
    main()
