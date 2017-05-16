from pathlib import Path


class Config:
    project_root = Path(__file__).parent
    config_pathname = project_root / 'config.json'

    stock_data_path = project_root.parent / 'py_stock_data'
    stock_day_data_etf_path = stock_data_path / 'day/etf_data'

    fund_data_path = project_root.parent / 'py_fund_data'
    # todel
    # def __init__(self):
    #     self.stock_data_path.mkdir(parents=True, exist_ok=True)
    #     # self.fund_data_path.mkdir(parents=True, exist_ok=True)
    #
    #     if os.path.exists(self.config_pathname):
    #         jstr = read_string_from_file(self.config_pathname)
    #         self.config_json = json.loads(jstr)
    #     else:
    #         self.config_json = {}
    #
    # def __getitem__(self, item):
    #     return self.config_json[item]
    #
    # def __setitem__(self, key, value):
    #     self.config_json[key] = value
    #     self.save()
    #
    # def save(self):
    #     jstr = json.dumps(self.config_json, ensure_ascii=False)
    #     save_string_to_file(jstr, self.config_pathname)
    #
    # def get_fund_data_path(self):
    #     path = self.project_root.parent / self.fund_data_path
    #     path.mkdir(parents=True, exist_ok=True)
    #     return str(path)


myconfig = Config()

if __name__ == '__main__':
    print(myconfig.project_root)
    print(myconfig.config_pathname)
    print(myconfig.stock_data_path)
    print(myconfig.fund_data_path)
    pass
