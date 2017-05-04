class CommMessage:
    def __init__(self, sender, operation, param=None):
        self.sender = sender
        self.operation = operation
        self.param = param

    def __repr__(self):
        return f'CommMessage{{{self.sender}, {self.operation}, {self.param}}}'


def main():
    print(CommMessage('a', 'b', 'c'))


if __name__ == '__main__':
    main()
