import queue


class ObjectPool:
    def __init__(self, generator, clear_func):
        self.queue = queue.Queue()
        self.generator = generator
        self.clear_func = clear_func

    def fetch_one(self):
        try:
            fetch_result = self.queue.get(block=False)
            return fetch_result
        except queue.Empty:
            return self.generator()

    def put_one(self, obj):
        if self.clear_func:
            self.clear_func(obj)
        self.queue.put(obj)

    # Use with python with statement
    def use_and_return(self):
        class Context:
            def __init__(self, cabinet):
                self.cabinet = cabinet
                self.current_obj = None

            def __enter__(self):
                self.current_obj = self.cabinet.fetch_one()
                return self.current_obj

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.cabinet.put_one(self.current_obj)

        return Context(self)


def test_object_cabinet():
    cab = ObjectPool(list, list.clear)
    assert len(cab.queue.queue) == 0
    with cab.use_and_return() as obj:
        obj.append('a')
        pass
    assert len(cab.queue.queue) == 1
    print(cab.queue.queue)
    assert cab.queue.queue[0] == []
