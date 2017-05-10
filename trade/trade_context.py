import queue

from trade.comm_message import CommMessage


class TradeContext:
    def __init__(self):
        self.queue_dict = {}
        self.cabinet_of_wait_result_queue = queue.Queue()

    def fetch_model_queue(self, model_name):
        self.queue_dict[model_name] = queue.Queue()
        return self.queue_dict[model_name]

    def find_queue_by_name(self, name):
        return self.queue_dict[name]

    def send_message(self, sender, dest, operation, param_dict):
        dest_queue = self.find_queue_by_name(dest)
        wait_queue = param_dict[ks_msg_wait_queue]
        msg = CommMessage(sender, operation, param_dict)
