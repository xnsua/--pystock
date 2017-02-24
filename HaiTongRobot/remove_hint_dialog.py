from utilities.import_basic import *
import win32api
import win32gui
import win32ui


class RemoveHintDialog:
    def __init__(self):
        self.main_window_cwnd = None

    def find_main_window(self):
        self.main_window_cwnd = win32ui.FindWindow('TdxW_MainFrame_Class', None)
        window_name = self.main_window_cwnd.GetWindowText() # type:str
        assert window_name.find('海通证券彩虹投资(通达信)V1.33') != -1
        print(self.main_window_cwnd.GetWindowText())


remove_hint_dialog = RemoveHintDialog()


def main():
    remove_hint_dialog.find_main_window()


if __name__ == '__main__':
    main()
