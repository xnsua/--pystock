class CommMessage:
    def __init__(self, sender, operation, param, result_queue, msg_time):
        self.sender = sender
        self.operation = operation
        self.param = param
        self.result_queue = result_queue
        self.msg_dt = msg_time

    def __repr__(self):
        return f'CommMessage{{{self.sender}, {self.operation}, {self.param}}}'

    def as_tuple(self):
        return self.sender, self.operation, self.result_queue

    def put_result(self, result):
        self.result_queue.put(result)


def main():
    print(CommMessage('a', 'b', 'c', 'c'))


if __name__ == '__main__':
    main()
