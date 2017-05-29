from project_helper.logbook_logger import mylog
from trading.base_structure.trade_constants import ktc_
from trading.base_structure.trade_message import TradeMessage
from trading.models.model_base import AbstractModel
from trading.trade_context import TradeContext


class ModelRunnerThread:
    def __init__(self, trade_context: TradeContext, model: AbstractModel):
        assert not hasattr(trade_context.thread_local, 'name')
        trade_context.thread_local.name = model.name()

        self.trade_context = trade_context
        self.model = model
        self.self_queue = trade_context.current_thread_queue()

        self.model.init_model()

    def run_loop(self):
        mylog.debug('Run loop')

        while True:
            msg = self.self_queue.get()  # type: TradeMessage
            mylog.debug(f'ReceiveMessage: {msg}')
            if msg.operation == ktc_.msg_bid_over:
                self.model.on_bid_over(msg.result)
            elif msg.operation == ktc_.msg_realtime_push:
                self.model.handle_bar(msg.result)
