import logging

logger = logging.getLogger('stock.log')
logger.setLevel(logging.DEBUG)
__ch = logging.StreamHandler()
__fh = logging.FileHandler('stock.log')
__formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s. (%(module)s, %(lineno)d)', "%y-%m-%d %H:%M:%S")
__ch.setFormatter(__formatter)
__fh.setFormatter(__formatter)
logger.addHandler(__ch)
logger.addHandler(__fh)
logger.debug('Mlog is imported')
