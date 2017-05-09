import threading


class ThreadSafeDict:
    def __init__(self):
        self.lock = threading.Lock()
        self.dict = {}

    def __getitem__(self, item):
        with self.lock:
            return self.dict[item]

    def __setitem__(self, key, value):
        with self.lock:
            self.dict[key] = value
