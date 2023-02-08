from src.common.gamecommon import GAMECOMMON
from src.common.util import load_csvfile

_info = []
_class = []
_unlock = []

class Potential(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load_info(self):
        table = load_csvfile(self, "potential")
        for row in table:
            kind = int(row["slot_kind"])
            grade = int(row["grade"])
            prob_atk = int(row["ATK_prob"])
            prob_df = int(row["DF_prob"])
            prob_hp = int(row["HP_prob"])
            prob_mg = int(row["MG_prob"])
            atk_min = int(row["ATK_min"])
            atk_max = int(row["ATK_max"])
            df_min = int(row["DF_min"])
            df_max = int(row["DF_max"])
            hp_min = int(row["HP_min"])
            hp_max = int(row["HP_max"])
            mg_min = int(row["MG_min"])
            mg_max = int(row["MG_max"])
            
            _info.append(
                Potential(
                    kind = kind,
                    grade = grade,
                    prob_atk = prob_atk,
                    prob_df = prob_df,
                    prob_hp = prob_hp,
                    prob_mg = prob_mg,
                    atk_min = atk_min,
                    atk_max = atk_max,
                    df_min = df_min,
                    df_max = df_max,
                    hp_min = hp_min,
                    hp_max = hp_max,
                    mg_min = mg_min,
                    mg_max = mg_max
                )
            )
    
    def load_class(self):
        table = load_csvfile(self, "potential_class")
        for row in table:
            jclass = int(row["class"])
            slot1 = int(row["slot1"])
            slot2 = int(row["slot2"])
            slot3 = int(row["slot3"])
            slot4 = int(row["slot4"])
            slot5 = int(row["slot5"])
            slot6 = int(row["slot6"])

            _class.append(
                Potential(
                    jclass = jclass,
                    slot1 = slot1,
                    slot2 = slot2,
                    slot3 = slot3,
                    slot4 = slot4,
                    slot5 = slot5,
                    slot6 = slot6
                )
            )
    
    
    def load_unlock(self):
        table = load_csvfile(self, "potential_unlock")
        for row in table:
            slot = int(row["slot"])
            level = int(row["level"])
            price_open = int(row["price_open"])
            price_change = int(row["price_change"])

            _unlock.append(
                Potential(
                    slot = slot,
                    level = level,
                    price_open = price_open,
                    price_change = price_change
                )
            )
    

    def get_info(self):
        return _info

    def get_class(self):
        return _class
    
    def get_unlock(self):
        return _unlock