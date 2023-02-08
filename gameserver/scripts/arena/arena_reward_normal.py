# -*- coding: utf-8 -*-
import csv
import os
import sys
from datetime import datetime

# 두단계 상위 폴더로 이동
# TODO : 기능 파악 및 필요하다고 판단 되면 운영툴 이관 작업 필요.
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from context import GameServerContext, init_callback
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.services.service_common import *


class Bunch(dict):
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        self.__dict__ = self

class RedisInitialize(ServiceCommon):
    def __init__(self, context):
        ServiceCommon.__init__(self)
        self.userid = None
        self.begin = None
        self.context = context

        self.w_db = context.w_db

        self.cache = context.cache
        self.cache_clone = context.cache_clone

        self.arena = context.arena
        self.arena_clone = context.arena_clone

        self.rank_reward_dict = []
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/gamedata/"
    

    def read_csvfile(self, filename):
        table = []
        with open(self.path + filename + ".csv", encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                table.append(row)

        return table

    def read_arena_normal_reward(self):
        table = self.read_csvfile("pvp_normal_reward")
        for row in table:
            rank_min = int(row["rank_min"])
            rank_max = int(row["rank_max"])
            reward_id = int(row["reward_id"])

            self.rank_reward_dict.append(Bunch(rank_min=rank_min, rank_max=rank_max, reward_id=reward_id))

    def update_progress(self, progress, total):
        print("[{0:10}] {1:2}%".format('#' * int(round(progress * 10.0 / total)), int(round(progress * 100.0 / total))))

    def arena_normal_process(self):
        self.read_arena_normal_reward()

        total_count = self.arena_clone.get_arena_normal_total()
        print("set_arena_season_count total_count:", total_count)
        self.arena.set_arena_season_count(total_count)

        db_arena_tournament_info = self.w_db['tourmentinfoadmin'].get_arena_tournament_info()
        if not db_arena_tournament_info:
            self.w_db['tourmentinfoadmin'].insert_arena_tournament_info(datetime.now())

        print("update_arena_total_count total_count:", total_count)
        self.w_db['tourmentinfoadmin'].update_arena_total_count(total_count)

        print(datetime.now(), "start arena normal reward / " + str(total_count))

        account_list = self.w_db['account'].select_all_account()
        total_count = len(account_list)
        print("select_all_account total_count:", total_count)

        hall_of_fame = [0, 0, 0, 0, 0]

        user_count = 0

        for i, account in enumerate(account_list):
            db_arena_info = self.w_db['arenanormal'].get_arena_info(account.account_uid)
            if not db_arena_info:
                print("not db_arena_info:", account.account_uid)
                continue

            # reward 지급방법 논의
            # TODO: 시즌 보상 등 해당 스크립트에 대한 운영툴 기능 이관 고려 - 기능 파악
            # self.w_db['arenanormal'].update_arena_season_rank(account.account_uid, db_arena_info.rank)

            if db_arena_info.rank <= 5:
                print("db_arena_info.rank <= 5:", account.account_uid)
                hall_of_fame[db_arena_info.rank-1] = account.account_uid

            if 0 < db_arena_info.rank:
                print("0 < db_arena_info.rank:", account.account_uid)
                user_count += 1

            db_tournament_info = self.w_db['arenatournament'].get_arena_tournament(account.account_uid)
            if not db_tournament_info:
                self.w_db['arenatournament'].insert_arena_tournament(account.account_uid, 0, 0, 0, 0, 0, 0, 0)

            self.update_progress(i + 1, total_count)

        print("tourmentinfoadmin.update_arena_user_count:", user_count)
        self.w_db['tourmentinfoadmin'].update_arena_user_count(user_count)

        season_id = self.w_db['halloffame'].insert_hall_of_fame(str(hall_of_fame))
        print("season_id:", season_id)

        redis_hall_of_fame = self.arena_clone.get_hall_of_fame_data(GAMECOMMON.ARENA_HALL_OF_FAME)
        if not redis_hall_of_fame:
            hall_of_fame_dict = {}
            hall_of_fame_dict[GAMECOMMON.ARENA_LAST_SEASON] = season_id
            rank_list = []
            rank_list.append(hall_of_fame)
            hall_of_fame_dict[GAMECOMMON.ARENA_HALL_OF_FAME_LIST] = str(rank_list)
            self.arena_clone.set_hall_of_fame_data(GAMECOMMON.ARENA_HALL_OF_FAME, hall_of_fame_dict)
            print("hall_of_fame_dict:", hall_of_fame_dict)
        else:
            hall_of_fame_list = convert_string_to_dict(redis_hall_of_fame[GAMECOMMON.ARENA_HALL_OF_FAME_LIST])
            if len(hall_of_fame_list) >= 6:
                del hall_of_fame_list[0]

            redis_hall_of_fame[GAMECOMMON.ARENA_LAST_SEASON] = season_id

            hall_of_fame_list.append(hall_of_fame)
            redis_hall_of_fame[GAMECOMMON.ARENA_HALL_OF_FAME_LIST] = str(hall_of_fame_list)
            self.arena_clone.set_hall_of_fame_data(GAMECOMMON.ARENA_HALL_OF_FAME, redis_hall_of_fame)
            print("hall_of_fame_list:", hall_of_fame_list)

conf_dir = os.path.dirname(os.path.abspath(__file__)) + "/conf/"
service_ini = conf_dir + "service_local.ini"

if __name__ == '__main__':
    context = GameServerContext(
        inifile=service_ini,
        after_init=init_callback
    )

    service = RedisInitialize(context)
    service.arena_normal_process()
