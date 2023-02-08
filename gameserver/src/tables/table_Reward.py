from src.common.util import load_csvfile

reward_set = {}
reward_prob = {}
reward_group = {}

class RewardSet(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load(self):
        table = load_csvfile(self, "reward_set")
        for row in table:
            id = int(row["id"])
            read_flag = int(row["server"])
            if 1 != read_flag:
                continue

            group_prob_id = []
            for i in range(7):
                column_name = "reward" + str(i+1)
                value = int(row[column_name])
                if 0 < value:
                    group_prob_id.append(value)

            reward_set[id] = group_prob_id


    def get(self):
        return reward_set



class RewardProb(object):
    def __init__(self, group_list, loop_count):
        self.group_list = group_list
        self.loop_count = loop_count

    def load(self):
        table = load_csvfile(self, "reward_prob")
        for row in table:
            id = int(row["id"])
            count = int(row["count"])
            group_prob_list = []
            for i in range(6):
                column_name = "group" + str(i+1) + "_id"
                group_id = int(row[column_name])
                if 0 >= group_id:
                    continue

                column_name = "group" + str(i+1) + "_prob"
                group_prob = int(row[column_name])
                group_prob_list.append(
                    RewardSet(
                        group_id = group_id,
                        group_prob = group_prob
                    )
                )

            reward_prob[id] = RewardProb(group_prob_list, count)

    def get(self):
        return reward_prob


class RewardGroup(object):
    def __init__(self, item_id, table_type, min_count, max_count):
        self.item_id = item_id
        self.table_type = table_type
        self.min_count = min_count
        self.max_count = max_count

    def load(self):
        table = load_csvfile(self, "reward_group")
        for row in table:
            group_id = int(row["group_id"])
            table_type = int(row["table"])
            item_id = int(row["item_id"])
            qty_min = int(row["qty_min"])
            qty_max = int(row["qty_max"])

            if not reward_group.get(group_id):
                item_list = []
                item_list.append(RewardGroup(item_id, table_type, qty_min, qty_max))
                reward_group[group_id] = item_list
            else:
                reward_group[group_id].append(RewardGroup(item_id, table_type, qty_min, qty_max))

    def get(self):
        return reward_group

