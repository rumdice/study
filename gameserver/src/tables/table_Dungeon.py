from src.common.util import load_csvfile

gimmick = {}
event_rogue_like = {}
join_condition = {}
enter_once = {}

# 고대던전 관련
class Dungeon(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load_gimmick(self):
        table = load_csvfile(self, "dungeon_gimmick")
        for row in table:
            group_id = int(row["group_id"])
            reward_id = int(row["reward_id"])
            stamina_qty = int(row["stamina_qty"])
            if not gimmick.get(group_id):
                floorReward = []
                floorReward.append(
                    Dungeon(
                        reward_id = 0,
                        stamina_qty = 0
                    )
                )
                floorReward.append(
                    Dungeon(
                        reward_id = reward_id,
                        stamina_qty = stamina_qty
                        )
                    )
                gimmick[group_id] = floorReward
            else:
                gimmick[group_id].append(
                    Dungeon(
                        reward_id = reward_id,
                        stamina_qty = stamina_qty
                    )
                )

    def load_reward_event_rogue_like(self):
        table = load_csvfile(self, "roguelike_reward")
        for row in table:
            difficulty = int(row["difficulty"])
            floor = int(row["floor"])
            step = int(row["step"])
            reward = int(row["reward"])

            if not event_rogue_like.get(difficulty, None):
                floor_dict = {}
                step_dict = {}
                step_dict[step] = reward
                floor_dict[floor] = step_dict
                event_rogue_like[difficulty] = floor_dict
            else:
                if not event_rogue_like[difficulty].get(floor, None):
                    step_dict = {}
                    step_dict[step] = reward
                    event_rogue_like[difficulty][floor] = step_dict
                else:
                    event_rogue_like[difficulty][floor][step] = reward

    def load_reward_join_condition(self):
        table = load_csvfile(self, "dungeon_restrict")
        for row in table:
            group = int(row["group_id"])
            floor = int(row["floor"])
            reward = int(row["reward_id"])

            if not join_condition.get(group, None):
                floor_dict = {}
                floor_dict[floor] = reward
                join_condition[group] = floor_dict
            else:
                join_condition[group][floor] = reward

    def load_reward_enter_once(self):
        table = load_csvfile(self, "dungeon_enterOnce")
        for row in table:
            group = int(row["group_id"])
            floor = int(row["floor"])
            reward = int(row["reward_id"])

            if not enter_once.get(group, None):
                floor_dict = {}
                floor_dict[floor] = reward
                enter_once[group] = floor_dict
            else:
                enter_once[group][floor] = reward
        


    def get_gimmick(self):
        return gimmick

    def get_reward_event_rogue_like(self):
        return event_rogue_like

    def get_reward_join_condition(self):
        return join_condition

    def get_reward_enter_once(self):
        return enter_once

