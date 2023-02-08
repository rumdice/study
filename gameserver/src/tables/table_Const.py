from src.common.gamecommon import GAMECOMMON
from src.common.util import load_csvfile

info = {}
exp = {}

class TableConst(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load(self):
        table = load_csvfile(self, "Const")
        for row in table:
            key = row["key"]
            value = float(row["value"])
            info[key] = TableConst(key=key, value=value)
            
            # 테이블을 읽으면서 레벨 데이터를 따로 빼놓음
            if GAMECOMMON.EXP_CONST_1 == key:
                exp[1] = int(value)
            if GAMECOMMON.EXP_CONST_2 == key:
                exp[2] = int(value)
            if GAMECOMMON.EXP_CONST_3 == key:
                exp[3] = int(value)
            if GAMECOMMON.EXP_CONST_4 == key:
                exp[4] = int(value)

    def get(self):
        return info

    def get_exp(self):
        return exp
