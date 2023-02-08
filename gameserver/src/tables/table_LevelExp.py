from src.common.util import load_csvfile

user_level_exp = {}
user_level_exp_list = []
user_exp_level_list = []

class LevelExp(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

    def load(self):
        table = load_csvfile(self, "user_level_exp")
        user_level_exp_list.append(0)
        user_exp_level_list.append(0)
        for row in table:
            user_level = int(row["user_level"])
            next_level_exp_sum = int(row["next_level_exp_sum"])
            max_stamina = int(row["max_stamina"])
            reward_set_id = int(row["reward_set_id"])

            user_level_exp_list.append(next_level_exp_sum)
            user_exp_level_list.append(next_level_exp_sum) # 왜 이런 구조로 쓰는지 알 수가 없으나 고치려면 많은 부분의 수정되야 함. user_level_exp.csv 테이블이 유용한가?
            user_level_exp[user_level] = LevelExp(
                user_level = user_level,
                next_level_exp_sum = next_level_exp_sum,
                max_stamina = max_stamina,
                reward_set_id = reward_set_id
            )

    def get_user_level_exp_list(self):
        return user_level_exp_list

    def get_user_exp_level_list(self):
        return user_exp_level_list

    def get_user_level_exp(self):
        return user_level_exp

    