import math
from unittest import TestCase

from training.training_common import TrainStatistics


class TestTrainCommon(TestCase):
    def test_true_per(self):
        val = TrainStatistics([False, True, True, False, False], [True, False, True, False, False])
        assert math.isclose(val.true_per, 0.5)
        assert math.isclose(val.false_per, 2 / 3.)

        val = TrainStatistics([False, True, True, False, True], [True, False, False, False, True])
        assert math.isclose(val.true_per, 0.5)
        assert math.isclose(val.false_per, 1 / 3.)

        val = TrainStatistics([False], [False])
        assert math.isclose(val.true_per, 0)
        assert math.isclose(val.false_per, 1)

        val = TrainStatistics([True], [True])
        assert math.isclose(val.true_per, 1)
        assert math.isclose(val.false_per, 0)
        val = TrainStatistics([True], [False])
        assert math.isclose(val.true_per, 0)
        assert math.isclose(val.false_per, 0)

        val = TrainStatistics([False], [True])
        assert math.isclose(val.true_per, 0)
        assert math.isclose(val.false_per, 0)

        import numpy as np
        for i in range(10):
            for j in range(100):
                true_vals = np.random.choice([True, False], size=j)
                predict_vals = np.random.choice([True, False], size=j)
                # print(true_vals)
                # print(predict_vals)
                ts = TrainStatistics(true_vals, predict_vals)
                pre_trues = true_vals[predict_vals]
                if len(pre_trues):
                    true_per = sum(pre_trues) / len(pre_trues)
                else:
                    true_per = 0
                pre_falses = true_vals[predict_vals == False]
                if len(pre_falses):
                    false_per = (len(pre_falses) - sum(pre_falses)) / len(pre_falses)
                else:
                    false_per = 0

                assert math.isclose(true_per, ts.true_per)
                assert math.isclose(false_per, ts.false_per)

