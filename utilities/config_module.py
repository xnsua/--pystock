import json
import os
from pathlib import Path

from common.helper import save_string_to_file, read_string_from_file


class Config:
    project_root = Path(__file__).parent.parent
    config_pathname = project_root / 'config.json'

    stock_data_path = project_root.parent / 'py_stock_data'
    fund_data_path = project_root.parent / 'py_fund_data'

    def __init__(self):
        self.stock_data_path.mkdir(parents=True, exist_ok=True)
        # self.fund_data_path.mkdir(parents=True, exist_ok=True)

        if os.path.exists(self.config_pathname):
            jstr = read_string_from_file(self.config_pathname)
            self.config_json = json.loads(jstr)
        else:
            self.config_json = {}

    def __getitem__(self, item):
        return self.config_json[item]

    def __setitem__(self, key, value):
        self.config_json[key] = value
        self.save()

    def save(self):
        jstr = json.dumps(self.config_json, ensure_ascii=False)
        save_string_to_file(jstr, self.get_config_path())

    def get_fund_data_path(self):
        path = self.project_root.parent / self.kdata_path / self.kfund_path
        path.mkdir(parents=True, exist_ok=True)
        return str(path)


config = Config()

if __name__ == '__main__':
    print(config.project_root)
    print(config.config_pathname)
    print(config.stock_data_path)
    print(config.fund_data_path)
    pass
