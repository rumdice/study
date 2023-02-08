from src.common.util import load_csvfile

area = []
distance = []
hero_gather = []
gather_reward = {}

class Resource(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load_area(self):
        table = load_csvfile(self, "resource_area")
        for row in table:
            level = int(row["area_level"])
            prob = int(row["prob"])
            amount = int(row["amount"])
            min_lv = int(row["hero_level"])
            area.append(
                Resource(
                    level = level,
                    prob = prob,
                    amount = amount,
                    min_lv = min_lv
                )
            )

    def load_hero_gather(self):
        table = load_csvfile(self, "hero_gather")
        for row in table:
            grade = int(row["hero_star"])
            move_speed = float(row["move_speed"])
            gather_speed = int(row["gather_speed"])
            hero_gather.append(
                Resource(
                    grade = grade,
                    move_speed = move_speed,
                    gather_speed = gather_speed
                )
            )
    
    def load_distance(self):
        table = load_csvfile(self, "area_distance")
        for row in table:
            min = int(row["distance_Min"])
            max = int(row["distance_Max"])
            prob = int(row["prob"])
            distance.append(
                Resource(
                    min = min,
                    max = max,
                    prob = prob
                )
            )

    def load_gather_reward(self):
        table = load_csvfile(self, "gather_reward")
        for row in table:
            area_type = int(row["area_type"])
            reward_set = int(row["reward_set"])

            if not gather_reward.get(area_type, None):
                level_reward_list = []
                level_reward_list.append(reward_set)
                gather_reward[area_type] = level_reward_list
            else:
                gather_reward[area_type].append(reward_set)


    def get_area(self):
        return area

    def get_hero_gather(self):
        return hero_gather

    def get_distance(self):
        return distance

    def get_gather_reward(self):
        return gather_reward

