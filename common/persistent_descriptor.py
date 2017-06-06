import atexit
import pathlib
import shelve


class _PersistentDescriptorBase:
    _db_path = None
    _db = None
    _write_every_time = True

    @classmethod
    def init_db(cls, file_path, write_every_time):
        assert not cls._db, f'Already initiate with {file_path}'
        cls._db_path = file_path
        pathlib.Path(pathlib.Path(file_path).parent).mkdir(parents=True, exist_ok=True)

        cls._db = shelve.open(file_path)
        atexit.register(lambda: cls._db.close())
        cls._write_every_time = write_every_time

    def __init__(self, identifier):
        assert self._db is not None, 'Use it with persistent class creator'
        self.value = None
        self.identifier = identifier
        self._has_read = False

    def __get__(self, instance, owner):
        if not self._has_read:
            self.value = self._db.get(self.identifier, None)
            self._has_read = True
        return self.value

    def __set__(self, instance, value):
        self.value = value
        self._db[self.identifier] = value


def create_persistent_descriptor_class(file_path, write_every_time=True):
    class PersistentField(_PersistentDescriptorBase):
        pass

    PersistentField.init_db(file_path, write_every_time)
    return PersistentField
