from stock_basic.stock_exception import ParamCheckException


class BsmNdrop:
    def __init__(self, data, drop_count):
        if drop_count < 1:
            raise ParamCheckException()
        self.data = data
        self.drop_count = drop_count
        self.data_len = len(data)
        self.buy_record = [False] * self.data_len

    def isbuy(self, index):
        if index < 0 or index >= self.data_len:
            raise ParamCheckException('Index {} is out of range', index)
        if index < self.drop_count:
            return False
        sub_data = self.data[index - self.drop_count: index]
        if not any(sub_data):
            self.buy_record[index] = True
            return True
        return False

    def calc_buy_array(self):
        for i in range(0, self.data_len):
            self.isbuy(i)
        return self.buy_record
