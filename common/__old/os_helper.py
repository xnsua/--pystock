# noinspection PyBroadException
import os
import sys

import psutil


def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
    try:
        p = psutil.Process(os.getpid())
        for handler in p.open_files() + p.connections():
            try:
                os.close(handler.fd)
            except Exception:
                print('error')
    except Exception:
        pass

    python = sys.executable
    os.execl(python, python, *sys.argv)
