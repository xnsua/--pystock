class TradeMessage:
    def __init__(self, sender, operation, param1, param2, result_queue, msg_time):
        self.sender = sender
        self.operation = operation
        self.param1 = param1
        self.param2 = param2
        self.result_queue = result_queue
        self.msg_dt = msg_time

    def __repr__(self):
        return f'CommMessage{{{self.sender}, {self.operation}, {str(self.param1)[0:10]}*, {str(self.param2)[0:10]}*}}'

    def put_result(self, result):
        if self.result_queue:
            self.result_queue.put(result)


def main():
    print(TradeMessage('aa', 'dff', 'dfd', 'd1111111111111111f', 'df', 'fdfd'))


if __name__ == '__main__':
    main()
