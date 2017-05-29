import time
import win32api

import win32con


def message_box_error(*texts):
    texts = map(lambda x: x if isinstance(x, str) else repr(x), texts)
    texts = '\n'.join(texts)
    win32api.MessageBox(None, texts, 'Error', win32con.MB_ICONERROR)


def message_box_error_if(predicate, title, *text):
    if predicate:
        message_box_error(title, *text)


def message_beep(seconds=5):
    for i in range(seconds):
        win32api.MessageBeep()
        time.sleep(1)
