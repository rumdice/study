from src.common.util import load_csvfile

reward_normal = []
reward_tournament = {}

class Arena(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load_reward_normal(self):
        table = load_csvfile(self, "pvp_normal_reward")
        for row in table:
            rank_min = int(row["rank_min"])
            rank_max = int(row["rank_max"])
            reward_id = int(row["reward_id"])

            reward_normal.append(
                Arena(
                    rank_min = rank_min, 
                    rank_max = rank_max, 
                    reward_id = reward_id
                )
            )

    def load_reward_tournament(self):
        table = load_csvfile(self, "tourament_reward")
        for row in table:
            group = int(row["group"])
            rank = int(row["rank"])
            reward_id = int(row["reward_id"])

            if not reward_tournament.get(group, None):
                reward_tournament[group] = {}
                reward_tournament[group][rank] = reward_id
            else:
                reward_tournament[group][rank] = reward_id


    def get_reward_normal(self):
        return reward_normal

    def get_reward_tournament(self):
        return reward_tournament

