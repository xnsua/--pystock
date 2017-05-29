from queue import Queue


class TradeMessage:
    def __init__(self, sender, operation, result, result_queue):
        self.sender = sender
        self.operation = operation
        self.result = result
        self.result_queue = result_queue  # type: Queue

    def __repr__(self):
        return f'CommMessage{{{self.sender}, {self.operation}, *{str(self.result)[0:50]}*, *{str(self.param2)[0:50]}*}}'

    def try_put_result(self, result):
        if self.result_queue:
            self.result_queue.put(result)
            return True
        return False


def test():
    pass
