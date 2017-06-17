import queue
import sys
import threading


class ExceptionThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__status_queue = queue.Queue()

    def run_with_exception(self):
        super().run()

    def run(self):
        """This method should NOT be overriden."""
        try:
            self.run_with_exception()
        except BaseException:
            self.__status_queue.put(sys.exc_info())
        self.__status_queue.put(None)

    def wait_for_exc_info(self):
        return self.__status_queue.get()

    def join_with_exception(self):
        ex_info = self.wait_for_exc_info()
        if ex_info is None:
            return
        else:
            raise ex_info[1]

    def is_running(self):
        return self.__status_queue.empty()

    def query_exception(self):
        try:
            return self.__status_queue.get(block=False)
        except queue.Empty:
            return None
