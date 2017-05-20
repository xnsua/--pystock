from trading.models.model_base import AbstractModel
from trading.trade_context import TradeContext
from trading.trade_helper import ktc_


# def thread_model(trade_context, model, **param):
#     try:
#         obj = ThreadModel(trade_context, model, param)
#         obj.run_loop()
#     except Exception:
#         mylog.exception('Trade model exception')
#         alert_exception(10)


class ModelRunnerThread:
    def __init__(self, trade_context: TradeContext, model: AbstractModel):
        assert not hasattr(trade_context.thread_local, 'name')
        trade_context.thread_local.name = type(model).__name__

        self.trade_context = trade_context
        self.model = model
        self.self_queue = trade_context.get_current_thread_queue()

        self.model.init_model()

    def run_loop(self):

        while True:
            msg = self.self_queue.get()

            if msg == ktc_.msg_bid_over:
                self.model.on_bid_over(msg.param1)
            elif msg == ktc_.msg_realtime_push:
                self.model.handle_bar(msg.param1)
