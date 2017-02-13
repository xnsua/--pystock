import json
import os
from datetime import datetime

from common import json_helper
from common import time_helper
from common.helper import save_string_to_file, read_string_from_file
from utilities.base_functions import BaseFunctions


class ManagerInfo(BaseFunctions):
    def __init__(self, names: str = None, start_time=datetime.fromtimestamp(0),
                 end_time=datetime.fromtimestamp(0)):
        if not names:
            names = []
        self.names = names
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__dict__.__str__()


class FundInfo(BaseFunctions):
    def __init__(self):
        self.code = ''
        self.name = ''
        self.start_time = None
        self.managers = []
        self.type = None
        self.rate = None

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__repr__()

    def to_json(self):
        return json.dumps(self, default=json_helper.json_default_encoder, ensure_ascii=False, indent=4)

    def to_file(self, filename):
        save_string_to_file(self.to_json(), filename)

    @classmethod
    def from_file(cls, filename):
        fcontent = read_string_from_file(filename)
        return cls.from_string(fcontent)

    @classmethod
    def from_string(cls, ss):
        info = FundInfo()
        ldict = json.loads(ss)
        info.__dict__ = ldict

        def managerdict2manager(mdict: str):
            manager = ManagerInfo()
            manager.__dict__ = mdict
            manager.start_time = time_helper.parse_time(manager.start_time)
            manager.end_time = time_helper.parse_time(manager.end_time)
            return manager

        info.managers = list(map(managerdict2manager, info.managers))
        return info


if __name__ == '__main__':
    finfo = FundInfo()
    finfo.name = 'name1'
    finfo.managers = []
    finfo.managers.append(ManagerInfo())

    tfname = 'fmanager.test'

    finfo.to_file(tfname)
    finfo2 = FundInfo.from_file(tfname)
    print(tfname)
    os.remove(tfname)

    assert finfo == finfo2
