# -*- coding: utf-8 -*-
import csv
import os
from datetime import datetime

from context import GameServerContext, init_callback
from src.common.util import *
from src.services.service_common import *

# TODO: 아레나 더미 데이터 생성 (NPC) 에 대한 재구현
# redis, rdb 이원화 제거
# 이 기능을 차후 운영툴로 제어 하도록 빼기 (현재 쉘 스크립트가 py 코드를 실행하는 구조)
# 이 밖에도 구현 및 재검토 해야 하는게 상당히 많음.

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

    def rewad_arena_normal_dummy(self, out_list):
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
        start_id = 2100000000
        for i in range(3000):
            self.cache.remove_user_profile(start_id+i)

        start_id = 4100000000
        for i in range(3000):
            self.cache.remove_user_profile(start_id+i)

        start_id = 4200000000
        for i in range(3000):
            self.cache.remove_user_profile(start_id+i)

    def update_progress(self, progress, total):
        printProgressBar(progress, total, prefix = 'Progress:', suffix = 'Complete', length = 20, fill = '>')

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

    def add_arena_dummy_process(self):
        dummy_list = []
        self.rewad_arena_normal_dummy(dummy_list)

        total_count = 0

        for dummy in dummy_list:
            total_count = dummy.rank_end

        print(datetime.now(), "start arena normal dummy / " + str(total_count))

        process_count = 0
        start_uid = 4100000000
        start_rank = 0
        for dummy in dummy_list:
            teamInfo = {}
            teamInfo['formation'] = dummy.teamid
            loop_count = (dummy.rank_end - dummy.rank_start) + 1
            start_rank = dummy.rank_start
            for i in range(loop_count):
                nick_name = dummy.nick + "_" + str(process_count)
                slot_index = 0
                for hero in dummy.hero_list:
                    self.add_slot_hero(slot_index, teamInfo, hero, hero.equip1, hero.equip2)
                    slot_index += 1

                # for hero in dummy.hero_list: end
                territory_dict = {}
                start_hero = '{}'
                self.arena.set_arena_normal_rank(start_uid, start_rank)
                self.cache.set_user_profile(
                    user_id=start_uid,
                    nickname=nick_name,
                    last_login=str(datetime.now()),
                    team_info=str(teamInfo),
                    level=1,
                    exp=0,
                    territory_dict=str(territory_dict),
                    start_hero=start_hero
                )
                # 최초 1회 실행
                self.w_db['arenanormal'].insert_arena_info(start_uid, start_rank, datetime.now(), datetime.now())
                self.w_db['arenanormal'].update_arena_rank(start_uid, start_rank)
                print("dummpy arenanormal insert (start_uid, start_rank)", start_uid, start_rank)

                self.update_progress(process_count, total_count)
                process_count += 1
                start_uid += 1
                start_rank += 1


if __name__ == '__main__':
    context = GameServerContext(
        inifile="./conf/service_local.ini",
        after_init=init_callback
    )

    service = RedisInitialize(context)
    service.redis_flush()
    service.add_arena_dummy_process()