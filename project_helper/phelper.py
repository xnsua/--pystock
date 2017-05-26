from common.log_helper import MyLog

mylog = MyLog(filename='py_stock.log', log_begin_end=True)


def jqd(*args):
    err_str = ' '.join(str(v) for v in args)
    mylog.log_with_level(mylog.logger.debug, err_str, outputfilepos=False)
    # mylog.log_with_level(mylog.logger.debug, err_str, outputfilepos=True)
