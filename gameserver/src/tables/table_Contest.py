from src.common.util import load_csvfile

contest = []
contest_monster = {}

# 길드승부
class Contest(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load(self):
        table = load_csvfile(self, "guild_contest")
        for row in table:
            id = int(row["id"])
            point_min = int(row["point_min"])
            point_max = int(row["point_max"])
            monster_level = int(row["monster_level"])
            reward = int(row["reward"])
            contest.append(
                Contest(
                    id = id,
                    point_min = point_min,
                    point_max = point_max,
                    monster_level = monster_level,
                    reward = reward
                )
            )


    def load_monster(self):
        table = load_csvfile(self, "guild_contest_monster")
        for row in table:
            guild_contest_monster_id = int(row["id"])
            id = int(row["id"])
            mob_id = int(row["mob_id"])
            team = int(row["team"])
            weak_gruop_id = int(row["weak_gruop_id"])
            weak_range_min = int(row["weak_range_min"])
            weak_range_max = int(row["weak_range_max"])
            weak_change_turn = int(row["weak_change_turn"])
            if not contest_monster.get(guild_contest_monster_id, None):
                list = []
                list.append(
                    Contest(
                        id = id,
                        mob_id = mob_id,
                        team = team,
                        weak_gruop_id = weak_gruop_id,
                        weak_range_min = weak_range_min,
                        weak_range_max = weak_range_max,
                        weak_change_turn = weak_change_turn
                    )
                )
                contest_monster[guild_contest_monster_id] = list
            else:
                contest_monster[guild_contest_monster_id].append(
                    Contest(
                        id = id,
                        mob_id = mob_id,
                        team = team,
                        weak_gruop_id = weak_gruop_id,
                        weak_range_min = weak_range_min,
                        weak_range_max = weak_range_max,
                        weak_change_turn = weak_change_turn
                    )
                )

    def get(self):
        return contest

    def get_monster(self):
        return contest_monster
