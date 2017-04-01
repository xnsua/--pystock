import win32process
import commctrl
import subprocess

from utilities.import_basic import *
import win32api
import win32gui
import win32ui


class MainWindow:
    __win_title = ''

    def __init__(self):
        self.__cwnd = None
        self.__hwnd = None
        self.__uithreadid = None
        self.__processid = None
        self.__threadlist = None
        # 资金股份
        self.__lv_share = None
        # 当日委托
        self.__lv_order = None
        # 当日成交
        self.__lv_volumn = None
        # 历史委托
        self.__lv_hisorder = None
        # 资金流水
        self.__lv_hiscapitalchange = None
        # ListView 切换器
        self.__tv_lvsel = None

    def init_main_window(self):
        self.__cwnd = win32ui.FindWindow('TdxW_MainFrame_Class', None)
        window_name = self.__cwnd.GetWindowText()  # type:str
        # assert window_name.find('海通证券彩虹投资(通达信)V1.33') != -1
        self.__hwnd = self.__cwnd.GetSafeHwnd()
        self.__uithreadid, self.__processid = win32process.GetWindowThreadProcessId(
            self.__hwnd)
        # print(f'{  self.__cwnd.GetSafeHwnd():08x}', window_name)

    def find_function_window(self):
        childwnds = []

        def call_back(hwnd, para):
            childwnds.append(hwnd)

        class WndObj(object):
            def __init__(self):
                self.hwnd = None

            def __repr__(self):
                return f'{self.hwnd:08x}' + str(self.__dict__)

        wobjlist = []
        win32gui.EnumChildWindows(self.__hwnd, call_back, None)
        for wnd in childwnds:
            tobj = WndObj()
            tobj.hwnd = wnd
            tobj.wintext = win32gui.GetWindowText(wnd)
            tobj.winclass = win32gui.GetClassName(wnd)
            wobjlist.append(tobj)

        wndlistview = list(filter(lambda x: x.winclass == 'SysListView32', wobjlist))
        self.__lv_share = wndlistview[0]
        self.__lv_order = wndlistview[3]
        self.__lv_volumn = wndlistview[4]
        # self.__lv_hisorder = wndlistview[]

        wndtreeview = list(filter(lambda x: x.winclass == 'SysTreeView32', wobjlist))
        self.__tv_lvsel = wndtreeview[0]
        child1 = win32api.SendMessage(wndtreeview[0].hwnd, commctrl.TVM_GETNEXTITEM,
                                      commctrl.TVGN_ROOT, 0)
        print('Tree info')
        print(f'{child1:08x}')

        # for val in wndlistview:
        #     print(val)

    def export_listview_to_file(self):
        sysexppath = (hp.Path(__file__)).parent / 'sysexp' / 'sysexp.exe'
        callstr = str(sysexppath) + ' /Handle 0x000113CA' + ' /scomma jqttt.csv'
        # hp.time_exec(lambda :subprocess.call(callstr))
        ss = dt.datetime.now()
        count = win32api.SendMessage(0x000113CA, commctrl.LVM_GETITEMCOUNT, 0, 0)
        headerhwn = win32api.SendMessage(0x000113CA, commctrl.LVM_GETHEADER, 0, 0)
        columncnt = win32api.SendMessage(headerhwn, commctrl.HDM_GETITEMCOUNT, 0, 0)
        print((dt.datetime.now() - ss).microseconds)
        print(headerhwn)

        print(columncnt)
        print(count)

    def find_last_login_window(self, wnd):
        twindows = []

        def call_back(hwnd, para):
            twindows.append(hwnd)

        win32gui.EnumThreadWindows(self.__uithreadid, call_back, None)
        wobjlist = []

        class wndobj(object):
            pass

        for wnd in twindows:
            tobj = wndobj()
            tobj.hwnd = wnd
            tobj.wintext = win32gui.GetWindowText(wnd)
            tobj.winclass = win32gui.GetClassName(wnd)
            wobjlist.append(tobj)
            print(tobj.hwnd, tobj.wintext, tobj.winclass)


main_window = MainWindow()


def main():
    main_window.init_main_window()
    main_window.find_function_window()
    # main_window.export_listview_to_file()


if __name__ == '__main__':
    main()
