class CommMessage:
    def __init__(self, sender, operation, param1, param2, result_queue, msg_time):
        self.sender = sender
        self.operation = operation
        self.param1 = param1
        self.param2 = param2
        self.result_queue = result_queue
        self.msg_dt = msg_time

    def __repr__(self):
        return f'CommMessage{{{self.sender}, {self.operation}, {self.param1}, {self.param2}}}'

    def put_result(self, result):
        self.result_queue.put(result)


def main():
    pass


if __name__ == '__main__':
    main()
