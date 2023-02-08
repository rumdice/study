from src.common.util import load_csvfile

darknest = []

class Darknest(object):
    def __init__(self, table_id, max_level, rewards):
        self.id = table_id
        self.max_lvel = max_level
        self.rewards = rewards

    def load_monster(self):
        table = load_csvfile(self, "darknest_monster")
        for row in table:
            id = int(row["id"])
            maxLv = int(row["max_level"])
            darknest.append(Darknest(id, maxLv, []))

    def load_reward(self):
        table = load_csvfile(self, "darknest_reward")
        for row in table:
            id = int(row["mob_id"])
            reward_set = int(row["reward_set"])

            for info in darknest:
                if id == info.id:
                    info.rewards.append(reward_set)
                    break
    
    def get(self):
        return darknest

    