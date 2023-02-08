# -*- coding: utf-8 -*-
import csv
import os
import sys
from datetime import datetime

# TODO : 기능 파악 및 필요하다고 판단 되면 운영툴 이관 작업 필요.
# 두단계 상위 폴더로 이동
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from context import GameServerContext, init_callback
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

        self.cache = context.cache
        self.cache_clone = context.cache_clone

        self.arena = context.arena
        self.arena_clone = context.arena_clone

        self.w_db = context.w_db
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/gamedata/"

    def read_csvfile(self, filename):
        table = []
        with open(self.path + filename + ".csv", encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                table.append(row)

        return table

    def reward_arena_normal_dummy(self, out_list):
        table = self.read_csvfile("pvp_normal_npc_data")
        for row in table:
            rank_min = int(row["rank_start"])
            rank_max = int(row["rank_end"])
            nick = row["nickname"]
            teamid = int(row["team_id"])

            hero_list = []
            for i in range(5):
                read_column = "hero_id_"+str(i+1)
                heroid = int(row[read_column])
                read_column = "hero_lv_"+ str(i+1)
                exp = int(row[read_column])
                read_column = "hero_"+ str(i+1)+"_equ_1"
                equip1 = int(row[read_column])
                read_column = "hero_"+ str(i+1)+"_equ_2"
                equip2 = int(row[read_column])
                hero_list.append(Bunch(heroid=heroid, exp=exp, equip1=equip1, equip2=equip2))

            out_list.append(Bunch(rank_start=rank_min, rank_end=rank_max, nick=nick, teamid=teamid, hero_list=hero_list))

    def redis_flush(self):
        self.arena.flush_db()

    def update_progress(self, progress, total):
        print("[{0:10}] {1:2}%".format('#' * int(round(progress * 10.0 / total)), int(round(progress * 100.0 / total))))

    def add_slot_hero(self, index, teamInfo, hero, equip1, equip2):
        teamInfo[index] = {}
        teamInfo[index]['hero_id'] = hero.heroid
        teamInfo[index]['exp'] = hero.exp
        teamInfo[index]['equip1'] = {}
        teamInfo[index]['equip1']['equip_id'] = equip1
        teamInfo[index]['equip1']['exp'] = 0
        teamInfo[index]['equip2'] = {}
        teamInfo[index]['equip2']['equip_id'] = equip2
        teamInfo[index]['equip2']['exp'] = 0

    # def add_arena_dummy_process(self):
    #     dummy_list = []
    #     self.rewad_arena_normal_dummy(dummy_list)

    #     total_count = 0

    #     for dummy in dummy_list:
    #         total_count = dummy.rank_end

    #     print(datetime.now(), "start arena normal dummy / " + str(total_count))

    #     process_count = 0
    #     start_uid = 4200000000
    #     start_rank = 0
    #     for dummy in dummy_list:

    #         teamInfo = {}
    #         teamInfo['formation'] = dummy.teamid
    #         loop_count = (dummy.rank_end - dummy.rank_start) + 1
    #         start_rank = dummy.rank_start
    #         for i in range(loop_count):
    #             nick_name = dummy.nick + "_" + str(process_count)
    #             slot_index = 0
    #             for hero in dummy.hero_list:
    #                 self.add_slot_hero(slot_index, teamInfo, hero, hero.equip1, hero.equip2)
    #                 slot_index += 1

    #             # for hero in dummy.hero_list: end
    #             territory_dict = {}

    #             start_hero = {*()}

    #             #self.w_db['arenanormal'].insert_arena_info(start_uid, start_rank, datetime.now(), datetime.now())
    #             self.arena.set_arena_normal_rank(start_uid, start_rank)
    #             self.cache.set_user_profile(start_uid, nick_name, str(datetime.now()), str(teamInfo),
    #                                                1, 0, str(territory_dict), str(start_hero))

    #             self.update_progress(process_count, total_count)
    #             process_count += 1
    #             start_uid += 1
    #             start_rank += 1

    #         #for i in range(loop_count): end
    #     #for dummy in dummy_list: end

    def arena_normal_recovery(self):

        # dummy init once
        dummy_list = []
        self.reward_arena_normal_dummy(dummy_list)

        dummy_total_count = 0

        for dummy in dummy_list:
            dummy_total_count = dummy.rank_end

        print(datetime.now(), "start arena normal dummy / " + str(dummy_total_count))

        process_count = 0
        # start_uid = 4200000000
        # init_arena_normal_dummy.py 에서 생성된 더미 데이터 아이디들과 일치 시킴
        start_uid = 4100000000
        for dummy in dummy_list:
            loop_count = (dummy.rank_end - dummy.rank_start) + 1
            for i in range(loop_count):
                arena_db = self.w_db['arenanormal'].get_arena_info(start_uid)
                if not arena_db:
                    continue

                self.arena.set_arena_normal_rank(start_uid, arena_db.rank)
                print("uid.rank:", start_uid, arena_db.rank)

                self.update_progress(process_count, dummy_total_count)
                process_count += 1
                start_uid += 1

        account_list = self.w_db['account'].select_all_account()
        account_total_count = len(account_list)
        print(datetime.now(), "start init cache / " + str(account_total_count))

        for i, account in enumerate(account_list):
            userinfo = self.w_db['profile'].find_profile(account.account_uid)
            if not userinfo:
                continue

            arena_db = self.w_db['arenanormal'].get_arena_info(account.account_uid)
            if not arena_db:
                continue

            self.arena.set_arena_normal_rank(account.account_uid, arena_db.rank)
            print("uid.rank:", account.account_uid, arena_db.rank)

            self.update_progress(i + 1, account_total_count)

if __name__ == '__main__':
    context = GameServerContext(
        inifile="./conf/service_local.ini",
        after_init=init_callback
    )

    service = RedisInitialize(context)
    service.redis_flush()
    #service.add_arena_dummy_process()
    service.arena_normal_recovery()