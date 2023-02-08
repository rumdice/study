from src.common.gamecommon import GAMECOMMON
from src.common.util import load_csvfile

endless = {}
farming = {}

class TowerBunch(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

class EndlessTower(object):
    def __init__(self, floor, reward):
        self.floor = floor
        self.reward = reward

    def load(self):
        table = load_csvfile(self, "endlessTower")
        for row in table:
            floor = int(row["floor"])
            reward = int(row["reward"])
            endless[floor] = EndlessTower(floor, reward)

    def get(self):
        return endless

class FarmingTower(object):
    def __init__(self, id, prob, floor_list):
        self.farming_id = id
        self.prob = prob
        self.floor_info = floor_list

    def read_farming_tower(self):
        table = load_csvfile(self, "farming_tower")
        for row in table:
            id = int(row["id"])
            prob = int(row["probability"])
            farming[id] = FarmingTower(id, prob, [])

    def read_gold_tower(self):
        table = load_csvfile(self, "ft_gold")
        for row in table:
            _stamina = int(row["stamina"])
            _reward = int(row["reward"])
            farming[GAMECOMMON.ITEM_GOLD_ID].floor_info.append(
                TowerBunch(
                    use_stamina = _stamina,
                    reward = _reward
                )
            )

    def read_food_tower(self):
        table = load_csvfile(self, "ft_food")
        for row in table:
            _stamina = int(row["stamina"])
            _reward = int(row["reward"])
            farming[GAMECOMMON.ITEM_FOOD_ID].floor_info.append(
                TowerBunch(
                    use_stamina = _stamina,
                    reward = _reward
                )
            )

    def read_stone_tower(self):
        table = load_csvfile(self, "ft_stone")
        for row in table:
            _stamina = int(row["stamina"])
            _reward = int(row["reward"])
            farming[GAMECOMMON.ITEM_STONE_ID].floor_info.append(
                TowerBunch(
                    use_stamina = _stamina,
                    reward = _reward
                )
            )

    def read_iron_tower(self):
        table = load_csvfile(self, "ft_iron")
        for row in table:
            _stamina = int(row["stamina"])
            _reward = int(row["reward"])
            farming[GAMECOMMON.ITEM_IRON_ID].floor_info.append(
                TowerBunch(
                    use_stamina = _stamina,
                    reward = _reward
                )
            )

    def read_wood_tower(self):
        table = load_csvfile(self, "ft_wood")
        for row in table:
            _stamina = int(row["stamina"])
            _reward = int(row["reward"])
            farming[GAMECOMMON.ITEM_WOOD_ID].floor_info.append(
                TowerBunch(
                    use_stamina = _stamina,
                    reward = _reward
                )
            )

    def read_exp_tower(self):
        table = load_csvfile(self, "ft_exp")
        for row in table:
            _stamina = int(row["stamina"])
            _reward = int(row["reward"])
            farming[GAMECOMMON.ITEM_HERO_EXP].floor_info.append(
                TowerBunch(
                    use_stamina = _stamina,
                    reward = _reward
                )
            )

    def get(self):
        return farming