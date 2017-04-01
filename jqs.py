import datetime
import sys
from test import config_for_test


def main():
    pass


if __name__ == '__main__':
    main()

    for k, v in sys.modules.items():
        if k.find('test') != -1:
            print(k, v)
