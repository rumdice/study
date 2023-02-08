from src.common.util import load_csvfile

group = []
single = []

class CollectionReward(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load_group(self):
        table = load_csvfile(self, "collection_group_reward")
        for row in table:
            grade = int(row["grade"])
            tier = int(row["tier"])
            hero_count = int(row["hero_count"])
            reward_set = int(row["reward_set"])
            group.append(
                CollectionReward(
                    grade = grade, 
                    tier = tier, 
                    hero_count = hero_count,
                    reward_set = reward_set
                )
            )
        

    def load_single(self):
        table = load_csvfile(self, "collection_single_reward")
        for row in table:
            grade = int(row["grade"])
            reward_set = int(row["reward_set"])
            single.append(
                CollectionReward(
                    grade = grade,
                    reward_set = reward_set
                )
            )
        

    def get_group(self):
        return group
    
    def get_single(self):
        return single
