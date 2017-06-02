from common.alert import message_box_error
from project_helper.logbook_logger import mylog, jqd
from trading.base_structure.trade_constants import MsgPushStocks, MsgQuitLoop, MsgBidOver
from trading.base_structure.trade_message import TradeMessage
from trading.models.model_base import AbstractModel
from trading.trade_context import TradeContext


class ModelRunnerThread:
    def __init__(self, trade_context: TradeContext, model: AbstractModel):
        assert not hasattr(trade_context.thread_local, 'name')
        trade_context.thread_local.name = model.name()

        self.trade_context = trade_context
        self.model = model
        self.self_queue = trade_context.current_thread_queue

        self.model.init_model()

    def run_loop(self):
        mylog.debug(f'Model: {self.model.name()} ........')

        while True:
            jqd('self.self_queue:::\n', self.self_queue)
            msg = self.self_queue.get()  # type: TradeMessage
            mylog.info(f'ReceiveMessage: {msg}')
            if isinstance(msg.operation, MsgBidOver):
                self.model.on_bid_over(msg.operation.stocks)
            elif isinstance(msg.operation, MsgPushStocks):
                self.model.handle_bar(msg.operation.stocks)
            elif isinstance(msg.operation, MsgQuitLoop):
                return
            else:
                message_box_error('Unknown message operation: ', msg.operation)
