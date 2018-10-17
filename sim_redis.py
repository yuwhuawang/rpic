# coding: utf-8


class SimRedis:

    R_DICT = {}

    def __init__(self):
        self.dict = self.R_DICT

    def keys(self):
        return self.dict.keys()

    def get(self, key):
        return self.dict.get(key, {})

    def insert(self, key, value):
        if key in self.dict:
            self.update(key, value)
            return
        self.dict[key] = value
        return "INSERTED KEY:{} TO VALUE:{}".format(key, value)

    def update(self, key, value):
        self.dict[key] = value
        return "UPDATED KEY:{} TO VALUE:{}".format(key, value)

    def delete(self, key):
        if key not in self.dict:
            return "KEY {} NOT EXIST".format(key)
        self.dict.pop(key)
        return "DELETE KEY {}".format(key)

    def flush(self):
        self.dict = SimRedis.R_DICT = {}
        return "CACHE EMPTY"


if __name__ == '__main__':
    sr = SimRedis()
    sr.insert("my", "haha")
    sr.keys()
    sr.update("my1", "hoho")
    sr.update("my1", "hehe")
    sr.delete("my3")
    sr.keys()
    sr2 = SimRedis()
    sr.flush()
    sr.keys()
    sr2.keys()
