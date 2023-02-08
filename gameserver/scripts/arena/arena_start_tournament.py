# -*- coding: utf-8 -*-
import math
import os
import random
import sys
from datetime import datetime

# 두단계 상위 폴더로 이동
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from context import GameServerContext, init_callback
from src.common.gamecommon import GAMECOMMON
from src.services.service_common import *


class RedisInitialize(ServiceCommon):
    def __init__(self, context):
        ServiceCommon.__init__(self)
        self.userid = None
        self.begin = None
        self.context = context
        self.w_db = context.w_db

        self.arena_tournament = context.arena_tournament

    def update_progress(self, progress, total):
        pass

    def arena_tourment_setting(self):
        print("[arena_tourment_setting]")
        db_arena_tournament_info = self.w_db['tourmentinfoadmin'].get_arena_tournament_info()
        print("db_arena_tournament_info:", db_arena_tournament_info)
        if not db_arena_tournament_info:
            print("not db_arena_tournament_info")
            return

        if db_arena_tournament_info.start_time <= datetime.now():
            print("It's already over past db_arena_tournament_info.start_time:", db_arena_tournament_info.start_time)
            return

        print(">>>> db_arena_tournament_info.day:", db_arena_tournament_info.day)
        if (7 < db_arena_tournament_info.day):
            print("!! too long day:", db_arena_tournament_info.day)
            return
        # 의도 불분명 (토너먼트 대진표 경우의 수)
        start_group_limit_user_count = math.pow(2, db_arena_tournament_info.day)
        # start_group_limit_user_count = math.pow(db_arena_tournament_info.day, 2)
        print(">>>> start_group_limit_user_count: math.pow(2, day)", start_group_limit_user_count)
        group_dict = {}
        for i in range(db_arena_tournament_info.group):
            group_dict[i] = []

##################### redis
        data_dict = {}
        data_dict[GAMECOMMON.R_TOURNAMENT_END_DAY] = db_arena_tournament_info.day
        data_dict[GAMECOMMON.R_TOURNAMENT_ROUND_DAY] = 1
        self.arena_tournament.set_tournament_data(GAMECOMMON.R_TOURNAMENT_INFO, data_dict)
#####################

        self.w_db['tourmentinfoadmin'].update_arena_tournament_day(0)
        print("update_arena_tournament_day = 0")

        print(datetime.now())
        print("[start init arena tournament]")
        arena_list = self.w_db['arenanormal'].get_arena_all()
        arena_list.sort(key = lambda x:x[1])
        total_count = len(arena_list)
        print("len(account_list):" + str(total_count))

        for i, account in enumerate(arena_list):
            db_arena_info = self.w_db['arenanormal'].get_arena_info(account.auid)
            if not db_arena_info:
                continue

            group_number = 0
            if db_arena_tournament_info.group <= group_number:
                print("!! db_arena_tournament_info.group <= group_number")
                continue
            else:
                pass

            group_dict[group_number].append(int(db_arena_info.auid))

        print(datetime.now())
        print("[matching arena tournament]")
        print("start_group_limit_user_count:", start_group_limit_user_count)
        print("group:", db_arena_tournament_info.group)
        print("start_group_limit_user_count * group", start_group_limit_user_count * db_arena_tournament_info.group)

        total_count = len(group_dict)
        print("len(group_dict):" + str(total_count))

        group_match_dict = {}
        for key, item in group_dict.items():
            print("key:", key)
            print("item:", item)
            group_match_dict[key] = []
            print("<<<< len(item):", len(item))
            print("<<<< start_group_limit_user_count:", start_group_limit_user_count)
            need_count = int(start_group_limit_user_count - len(item))
            print("<<<< need_count(count - len):", need_count)
            if need_count > 0:
                for npc in range(need_count):
                    item.append(0)
            else:
                item = item[:need_count]

            print("shuffle begin...")
            random.shuffle(item)
            print("shuffle end...")

            print("============================================")
            print("len(item) = ", str(int(len(item))))
            print("len(item) / 2 = ", str(int(len(item) / 2)))
            sys.stdout.write("i")
            sys.stdout.flush()

            for i in range(int(len(item) / 2)):
                index = i * 2
                group_match_dict[key].append([item[index],item[index + 1]])
                self.w_db['arenatournament'].update_arena_tournament(item[index], key, item[index + 1], i, start_group_limit_user_count)
                self.w_db['arenatournament'].update_arena_tournament(item[index + 1], key, item[index], i, start_group_limit_user_count)
                sys.stdout.write('i')
                sys.stdout.flush()

            print("group_match_dict[0]):")
            print(str(group_match_dict[key]))
            self.arena_tournament.set_tournament_info(key, str(group_match_dict[key]))
    
        print(datetime.now())
        print("finish update arena tournament")

conf_dir = os.path.dirname(os.path.abspath(__file__)) + "/conf/"
service_ini = conf_dir + "service_local.ini"

if __name__ == '__main__':
    context = GameServerContext(
        inifile=service_ini,
        after_init=init_callback
    )

    service = RedisInitialize(context)
    service.arena_tourment_setting()
