import time
import win32api
from inspect import stack, getframeinfo

import win32con


def message_box_error(*texts):
    caller = getframeinfo(stack()[1][0])
    caller_text = caller.filename + ': ' + str(caller.lineno)
    texts = map(lambda x: x if isinstance(x, str) else repr(x), texts)
    texts = '\n'.join(texts)
    texts += '\n' + caller_text
    win32api.MessageBox(None, texts, 'Error',
                        win32con.MB_SYSTEMMODAL | win32con.MB_ICONERROR | win32con.MB_SETFOREGROUND | win32con.MB_TOPMOST)


def message_box_error_if(predicate, title, *text):
    if predicate:
        message_box_error(title, *text)


def message_beep(seconds=5):
    for i in range(seconds):
        win32api.MessageBeep()
        time.sleep(1)
