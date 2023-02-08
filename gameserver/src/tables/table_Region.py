from src.common.util import load_csvfile

check = {}
mission = {}

class Region(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load(self):
        table = load_csvfile(self, "regioncheck")
        for row in table:
            region = int(row["region"])
            floor = int(row["floor"])
            difficulty = int(row["difficulty"])
            _stamina = int(row["stamina"])
            _step = int(row["rewardS"])
            _boss = int(row["rewardB"])
            _total = int(row["totalStep"])

            if not check.get(region, None):
                floor_dict = {}
                difficulty_dict = {}
                difficulty_dict[difficulty] = Region(
                    reward_step = _step,
                    reward_boss = _boss,
                    use_stamina = _stamina,
                    total_step = _total
                )
                floor_dict[floor] = difficulty_dict
                check[region] = floor_dict
            else:
                if not check[region].get(floor, None):
                    difficulty_dict = {}
                    difficulty_dict[difficulty] = Region(
                        reward_step = _step,
                        reward_boss = _boss,
                        use_stamina = _stamina,
                        total_step = _total
                    )
                    check[region][floor] = difficulty_dict
                else:
                    check[region][floor][difficulty] = Region(
                        reward_step = _step,
                        reward_boss = _boss,
                        use_stamina = _stamina,
                        total_step = _total
                    )


    def load_mission(self):
        table = load_csvfile(self, "region_mission_group")
        for row in table:
            region = int(row["region"])
            difficulty = int(row["difficulty"])
            mission_reward = []
            reward_column = ""
            for i in range(5):
                reward_column = "reward" + str(i+1) + "_id"
                mission_reward.append(int(row[reward_column]))

            if not mission.get(region, None):
                difficuly_dict = {}
                difficuly_dict[difficulty] = mission_reward
                mission[region] = difficuly_dict
            else:
                mission[region][difficulty] = mission_reward



    def get(self):
        return check

    def get_mission(self):
        return mission
