class CommMessage:
    def __init__(self, sender, operation, param=None):
        self.sender = sender
        self.operation = operation
        self.param = param
