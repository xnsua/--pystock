from common.log_helper import jqd
from trading.base_structure.trade_constants import ktc_
from trading.base_structure.trade_message import TradeMessage
from trading.models.model_base import AbstractModel
from trading.trade_context import TradeContext


class ModelRunnerThread:
    def __init__(self, trade_context: TradeContext, model: AbstractModel):
        assert not hasattr(trade_context.thread_local, 'name')
        trade_context.thread_local.name = type(model).__name__

        self.trade_context = trade_context
        self.model = model
        self.self_queue = trade_context.get_current_thread_queue()

        self.model.init_model()

    def log(self, msg):
        jqd(f'{self.trade_context.thread_local.name}:: {msg}')

    def run_loop(self):
        self.log('Run loop')

        while True:
            msg = self.self_queue.get()  # type: TradeMessage
            self.log(str(msg))
            if msg.operation == ktc_.msg_bid_over:
                self.model.on_bid_over(msg.param1)
            elif msg.operation == ktc_.msg_realtime_push:
                self.model.handle_bar(msg.param1)
            elif msg.operation == ktc_.msg_quit_loop:
                break
