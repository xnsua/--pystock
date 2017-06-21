import logging
import pathlib as pl


def get_common_root():
    path = pl.Path(__file__)
    while path.name != 'common':
        path = path.parent
    return path


cmlog = logging.getLogger('common_logger')
cmlog.setLevel(logging.DEBUG)
__ch = logging.StreamHandler()
__ch.setLevel(logging.DEBUG)
__log_path = get_common_root() / 'common.log'
__fh = logging.FileHandler(__log_path, 'a', 'utf-8')
__formatter = logging.Formatter(
    '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s.',
    # '[%(thread)d]%(asctime)s %(levelname)s:%(message)s.',
    "%m-%d %H:%M:%S")
# "%y-%m-%d %H:%M:%S")
__ch.setFormatter(__formatter)
__fh.setFormatter(__formatter)
cmlog.addHandler(__ch)
cmlog.addHandler(__fh)

cmlog.warning('hello')
