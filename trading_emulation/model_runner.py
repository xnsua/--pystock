from trading_emulation.account import Account


class ModelRunner:
    def __init__(self, model):
        self.model = model
        rdict = self.model.init()



