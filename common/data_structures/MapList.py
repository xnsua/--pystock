class MapList:
    def __init__(self, index, list_):
        assert len(index) == len(list_)
        self.list = list_
        self.index_map = {}
        for i, value in enumerate(index):
            self.index_map[value] = i

    def __getitem__(self, item):
        return self.list[item]
