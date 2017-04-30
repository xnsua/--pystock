import multiprocessing

from common.helper import LogicException, exception_to_logstr, sleep_ms
from common.log_helper import mylog, jqd
from data_server.data_server_constant import k_id_data_server, k_id_trade_loop
from data_server.etf_updater import update_etf


def data_server_loop(**queue_dict):
    data_server = DataServer(queue_dict)
    data_server.run_loop()


def query_etfs():
    etfs = update_etf()
    return etfs


class DataServer:
    def __init__(self, queue_dict):
        self.self_queue = queue_dict[
            k_id_data_server]  # type: multiprocessing.Queue
        self.queue_dict = queue_dict

    def run_loop(self):
        jqd('Data server run loop ...')
        trade_queue = self.queue_dict[k_id_trade_loop]
        trade_queue.put('Dataserver -> Trade queue')
        while 1:
            msg = self.self_queue.get()
            jqd(f'In dataserver: f{msg}')
            sleep_ms(1000)

            # return 1
            # while 1:
            #     msg = self.self_queue.get()
            #     sender, operation, content = msg
            #     self.dispatch_msg(sender, operation, content)

    def dispatch_msg(self, sender, operation, content):
        try:
            func = self.find_func_by_operation(operation)
            out_queue = self.find_out_queue_by_sender(sender)
            result = func(**content)
            out_queue.put((k_data_server_id, (operation, result)))
        except Exception as e:
            out_queue.put((k_data_server_id, (Exception.__name__, e)))
            mylog.error(exception_to_logstr(e))

    def find_out_queue_by_sender(self, sender):
        try:
            return self.queue_dict[sender]
        except:
            raise LogicException(f'Can not find out queue of sender {sender}')

    @staticmethod
    def find_func_by_operation(operation):
        gls = globals()
        for k in gls:
            if k == operation:
                if type(gls[k]) == function:
                    return gls[k]
        raise LogicException(f'Can not find func of name {operation}')


def main():
    # ds = DataServer(myconfig.stock_data_path / 'day/data_server', None)
    # print(DataServer.__dict__['query_etfs']())
    # print(globals())
    # dayhistorys = ds.query_day_history(['000908', '000877'exbb''], ndays_ago(6))
    pass


if __name__ == '__main__':
    main()
