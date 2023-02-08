from src.common.util import load_csvfile

damage_grade = []
monster = {}
class_stat_const = {}
win_reward = []
fail_reward = []

class ClassStatConst():
    def __init__(self, id, atk, df, hp, correction):
        self.id = id
        self.atk = atk
        self.df = df
        self.hp = hp
        self.correction = correction


# 토벌레이드
class Raid(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load_damage(self):
        table = load_csvfile(self, "guildRaid_grade")
        for row in table:
            grade = int(row["grade"])
            rank = int(row["rank"])
            win_min = int(row["win_damage_min"])
            win_max = int(row["win_damage_max"])
            fail_min = int(row["fail_damage_min"])
            fail_max = int(row["fail_damage_max"])
            damage_grade.append(
                Raid(
                    grade = grade,
                    rank = rank,
                    win_damage_min = win_min, 
                    win_damage_max = win_max,
                    fail_damage_min = fail_min,
                    fail_damage_max = fail_max
                )
            )

    def load_monster(self):
        table = load_csvfile(self, "guildRaid_monster")
        for row in table:
            element = int(row["element_group"])
            mob_id = int(row["mob_id"])
            hp_base = int(row["HP_base"])
            hp_const = int(row["HP_const"])

            if not monster.get(element, None):
                list = []
                list.append(
                    Raid(
                        boss_id = mob_id,
                        hp_base = hp_base,
                        hp_const = hp_const
                    )
                )
                monster[element] = list
            else:
                monster[element].append(
                    Raid(
                        boss_id = mob_id,
                        hp_base = hp_base,
                        hp_const = hp_const
                    )
                )

    def load_stat(self):
        table = load_csvfile(self, "class_stat_const")
        for row in table:
            index = int(row["class_id"])
            atk = int(row["ATK"])
            df = int(row["DF"])
            hp = int(row["HP"])
            correction = int(row["correction"])
            class_stat_const[index] = ClassStatConst(index, atk, df, hp, correction)


    def load_reward_win(self):
        table = load_csvfile(self, "guildRaid_reward_win")
        for row in table:
            reward_grade_list = []
            for i in range(7):
                column = "reward_" + str(i+1)
                reward_id  = int(row[column])
                column = "qty_" + str(i+1)
                loop_count = int(row[column])
                reward_grade_list.append(Raid(reward_set=reward_id, count=loop_count))

            win_reward.append(reward_grade_list)

    def load_reward_fail(self):
        table = load_csvfile(self, "guildRaid_reward_fail")
        for row in table:
            reward_grade_list = []
            for i in range(7):
                column = "reward_" + str(i+1)
                reward_id  = int(row[column])
                column = "qty_" + str(i+1)
                loop_count = int(row[column])
                reward_grade_list.append(Raid(reward_set=reward_id, count=loop_count))

            fail_reward.append(reward_grade_list)


    def get_damage(self):
        return damage_grade

    def get_monster(self):
        return monster

    def get_stat(self):
        return class_stat_const

    def get_reward_win(self):
        return win_reward

    def get_reward_fail(self):
        return fail_reward
