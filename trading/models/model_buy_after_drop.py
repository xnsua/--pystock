from common.log_helper import mylog

logger = mylog


class ModelBuyAfterDrop:
    def __init__(self, trade_context, param_dict):
        self.context = trade_context
        self.stocks = None
        self.param_dict = param_dict
        pass

    def init_model(self):
        pass

    def before_trading(self):
        pass

    def handle_bar(self):
        pass

    def trading_break(self):
        pass

    def after_trading(self):
        pass
