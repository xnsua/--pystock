import subprocess
import win32api
import win32gui
import win32ui

import win32con

from utilities.import_basic import *


class HtLogin:
    __cwnd = None

    @classmethod
    def login(cls, tradeonly=False):
        cls.init_main_window()
        _childwindowlist = []

        # noinspection PyUnusedLocal
        def _print_child(hwnd, param):
            _childwindowlist.append(hwnd)

        win32gui.EnumChildWindows(cls.__hwnd, _print_child, None)
        for i, wnd in enumerate(_childwindowlist):
            pass

        _standalonetradehwnd = _childwindowlist[17]
        _loginwindow = _childwindowlist[7]

        if tradeonly:
            win32api.SendMessage(_standalonetradehwnd, win32con.WM_LBUTTONDOWN, 0, 0)
            win32api.SendMessage(_standalonetradehwnd, win32con.WM_LBUTTONUP, 0, 0)

        _filecommpass = hp.Path(__file__).parent / 'haitong_login_tongxin.exe'
        hp.time_exec(lambda: subprocess.call(str(_filecommpass)))
        _filetradepass = hp.Path(__file__).parent / 'haitong_login_trade.exe'
        subprocess.call(str(_filetradepass))
        win32api.SendMessage(_loginwindow, win32con.WM_LBUTTONDOWN, 0, 0)
        win32api.SendMessage(_loginwindow, win32con.WM_LBUTTONUP, 0, 0)

    @classmethod
    def init_main_window(cls):
        cls.__cwnd = win32ui.FindWindow('#32770', '海通证券彩虹投资(通达信)V1.33')
        cls.__hwnd = cls.__cwnd.GetSafeHwnd()

    def unlock_mainwindow(self):
        pass


ht_login = HtLogin()


def main():
    ht_login.login()


if __name__ == '__main__':
    main()
