import os


class Config:
    @property
    def __data_path(self):
        return os.path.abspath('..')

    @property
    def fund_data_path(self):
        path = os.path.join(self.__data_path, 'fund')
        os.makedirs(path, exist_ok=True)
        return path
