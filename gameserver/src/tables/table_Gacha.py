from src.common.util import load_csvfile

gacha = {}

class Gacha(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load(self):
        table = load_csvfile(self, "gacha")
        for row in table:
            gacha_id = int(row["id"])
            summon_type = int(row["type"])
            reward_set = int(row["reward_set"])
            wait_hour = int(row["wait_hours"])
            unlock_level = int(row["unlock_level"])
            need_inven = int(row["inven_need"])
            use_item = []
            use_dict = {}
            for i in range(4):
                read_str = "item"+str(i+1)+"_id"
                item_id = int(row[read_str])
                if 0 >= item_id:
                    continue

                read_str = "item"+str(i+1)+"_qty"
                count = int(row[read_str])
                use_item.append(item_id)
                use_dict[item_id] = count

            gacha[gacha_id] = Gacha(
                gacha_id = gacha_id,
                type = summon_type,
                reward_set = reward_set,
                refresh_hour = wait_hour,
                summon_level = unlock_level,
                use_item = use_item,
                use_dict = use_dict,
                need_inven = need_inven
            )

    def get(self):
        return gacha
