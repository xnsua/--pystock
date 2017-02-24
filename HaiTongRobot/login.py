import subprocess
import win32api
import win32gui
import win32ui

import win32con

from utilities.import_basic import *


class HtLogin:
    @staticmethod
    def login():
        _hwnd = win32ui.FindWindow(None, '海通证券彩虹投资(通达信)V1.33')
        _childwindowlist = []

        # noinspection PyUnusedLocal
        def _print_child(hwnd, param):
            _childwindowlist.append(hwnd)

        win32gui.EnumChildWindows(_hwnd.GetSafeHwnd(), _print_child, None)
        for i, wnd in enumerate(_childwindowlist):
            print(i, f'{wnd:_x}')

        _standalonetradehwnd = _childwindowlist[17]
        _loginwindow = _childwindowlist[7]

        win32api.SendMessage(_standalonetradehwnd, win32con.WM_LBUTTONDOWN, 0, 0)
        win32api.SendMessage(_standalonetradehwnd, win32con.WM_LBUTTONUP, 0, 0)

        _filecommpass = hp.Path(__file__).parent / 'haitong_login_tongxin.exe'
        subprocess.call(str(_filecommpass))
        _filetradepass = hp.Path(__file__).parent / 'haitong_login_trade.exe'
        subprocess.call(str(_filetradepass))

        win32api.SendMessage(_loginwindow, win32con.WM_LBUTTONDOWN, 0, 0)
        win32api.SendMessage(_loginwindow, win32con.WM_LBUTTONUP, 0, 0)

    def unlock_mainwindow(self):
        pass

        

def main():
    HtLogin.login()


if __name__ == '__main__':
    main()
