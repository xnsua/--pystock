from queue import Queue


class TradeMessage:
    def __init__(self, sender, operation, param1, param2, result_queue):
        self.sender = sender
        self.operation = operation
        self.param1 = param1
        self.param2 = param2
        self.result_queue = result_queue  # type: Queue

    def __repr__(self):
        return f'CommMessage{{{self.sender}, {self.operation}, *{str(self.param1)[0:50]}*, *{str(self.param2)[0:50]}*}}'

    def try_put_result(self, result):
        if self.result_queue:
            self.result_queue.put(result)


def main():
    pass


if __name__ == '__main__':
    main()
