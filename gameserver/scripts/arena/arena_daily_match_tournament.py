# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime
from pprint import pprint

# 두단계 상위 폴더로 이동
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from context import GameServerContext, init_callback
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.services.service_common import *


class RedisInitialize(ServiceCommon):
    def __init__(self, context):
        ServiceCommon.__init__(self)
        self.userid = None
        self.begin = None
        self.context = context
        self.w_db = context.w_db

        self.arena_tournament = context.arena_tournament
        self.arena_tournament_clone = context.arena_tournament_clone_

    def update_progress(self, progress, total):
        print("[{0:10}] {1:2}%".format('#' * int(round(progress * 10.0 / total)), int(round(progress * 100.0 / total))))

    def final_round(self, group, match_list, redis_data):
        print(datetime.now(), "start arena tournament final")

        final_rank = 1
        for matchs in match_list:
            match_1 = self.w_db['arenatournament'].get_arena_tournament(matchs[0])
            match_2 = self.w_db['arenatournament'].get_arena_tournament(matchs[1])

            if not match_1 and not match_2:  # 둘다 npc
                final_rank += 2
            elif not match_1 and match_2:  # 부전승
                self.w_db['arenatournament'].update_arena_tournament_rank(match_2.auid, final_rank)
                final_rank += 2

            elif match_1 and not match_2:  # 부전승
                self.w_db['arenatournament'].update_arena_tournament_rank(match_1.auid, final_rank)
                final_rank += 2
            else:
                if match_1.point < match_2.point:  # 포인트 높은사람
                    self.w_db['arenatournament'].update_arena_tournament_rank(match_2.auid, final_rank)
                    final_rank += 1
                    self.w_db['arenatournament'].update_arena_tournament_rank(match_1.auid, final_rank)
                    final_rank += 1
                elif match_1.point > match_2.point:  # 포인트 높은사람
                    self.w_db['arenatournament'].update_arena_tournament_rank(match_1.auid, final_rank)
                    final_rank += 1
                    self.w_db['arenatournament'].update_arena_tournament_rank(match_2.auid, final_rank)
                    final_rank += 1
                else:  # 포인트가 같을때
                    if match_1.battle_turn < match_2.battle_turn:  # 배틀 턴을 덜쓴애
                        self.w_db['arenatournament'].update_arena_tournament_rank(match_1.auid, final_rank)
                        final_rank += 1
                        self.w_db['arenatournament'].update_arena_tournament_rank(match_2.auid, final_rank)
                        final_rank += 1
                    elif match_1.battle_turn > match_2.battle_turn:  # 배틀 턴을 덜쓴애
                        self.w_db['arenatournament'].update_arena_tournament_rank(match_2.auid, final_rank)
                        final_rank += 1
                        self.w_db['arenatournament'].update_arena_tournament_rank(match_1.auid, final_rank)
                        final_rank += 1
                    else:  # 배틀턴까지 같아
                        if match_1.auid < match_2.auid:  # 유저 생성기준
                            self.w_db['arenatournament'].update_arena_tournament_rank(match_1.auid, final_rank)
                            final_rank += 1
                            self.w_db['arenatournament'].update_arena_tournament_rank(match_2.auid, final_rank)
                            final_rank += 1
                        else:  # 유저생성기준
                            self.w_db['arenatournament'].update_arena_tournament_rank(match_2.auid, final_rank)
                            final_rank += 1
                            self.w_db['arenatournament'].update_arena_tournament_rank(match_1.auid, final_rank)
                            final_rank += 1

        self.arena_tournament.set_tournament_info(group, str([]))
        print(datetime.now(), "end arena tournament semi final/ ")

    def semi_final_round(self, group, match_list, redis_data):
        print(datetime.now(), "start arena tournament semi final")

        new_match_list = []
        final_user = []
        semi_final_user = []
        print(match_list)
        for matchs in match_list:
            match_1 = self.w_db['arenatournament'].get_arena_tournament(matchs[0])
            match_2 = self.w_db['arenatournament'].get_arena_tournament(matchs[1])

            if not match_1 and not match_2: # 둘다 npc
                final_user.append(0)
                semi_final_user.append(0)
            elif not match_1 and match_2: # 부전승
                final_user.append(match_2.auid)
                semi_final_user.append(0)
            elif match_1 and not match_2: # 부전승
                final_user.append(match_1.auid)
                semi_final_user.append(0)
            else:
                if match_1.point < match_2.point: # 포인트 높은사람
                    final_user.append(match_2.auid)
                    semi_final_user.append(match_1.auid)
                elif match_1.point > match_2.point: # 포인트 높은사람
                    final_user.append(match_1.auid)
                    semi_final_user.append(match_2.auid)
                else: # 포인트가 같을때
                    if match_1.battle_turn < match_2.battle_turn: # 배틀 턴을 덜쓴애
                        final_user.append(match_1.auid)
                        semi_final_user.append(match_2.auid)
                    elif match_1.battle_turn > match_2.battle_turn: # 배틀 턴을 덜쓴애
                        final_user.append(match_2.auid)
                        semi_final_user.append(match_1.auid)
                    else: # 배틀턴까지 같아
                        if match_1.auid < match_2.auid: # 유저 생성기준
                            final_user.append(match_1.auid)
                            semi_final_user.append(match_2.auid)
                        else: # 유저생성기준
                            final_user.append(match_2.auid)
                            semi_final_user.append(match_1.auid)

        new_match_list.append([final_user[0], final_user[1]])
        new_match_list.append([semi_final_user[0], semi_final_user[1]])
        print(new_match_list)
        self.w_db['arenatournament'].update_arena_tournament(
            final_user[0],
            group,
            final_user[1],
            0,
            int(len(match_list) / 2)
        )
        self.w_db['arenatournament'].update_arena_tournament(
            final_user[1],
            group,
            final_user[0],
            0,
            int(len(match_list) / 2)
        )
        self.w_db['arenatournament'].update_arena_tournament(
            semi_final_user[0],
            group,
            semi_final_user[1],
            1,
            int(len(match_list) / 2)
        )
        self.w_db['arenatournament'].update_arena_tournament(
            semi_final_user[1],
            group,
            semi_final_user[0],
            1,
            int(len(match_list) / 2)
        )

        self.arena_tournament.set_tournament_info(group, str(new_match_list))


    def arena_tourment_battle_result(self):
        print("==============================================================")
        print(datetime.now())
        print("[start arena tournament daily]")

        db_arena_tournament_info = self.w_db['tourmentinfoadmin'].get_arena_tournament_info()
        if not db_arena_tournament_info:
            print("!! not db_arena_tournament_info")
            return

        if db_arena_tournament_info.round_day == 0 and time_diff_in_day(db_arena_tournament_info.start_time) > -2: 
            #self.w_db['tourmentinfoadmin'].update_arena_tournament_day(1)
            print("!! update_arena_tournament_day(0)")
            return

        remain_day = db_arena_tournament_info.day - db_arena_tournament_info.round_day
        print("remain_day:", str(remain_day))
        if remain_day <= 0:
            print("!! remain_day <= 0")
            return

        # for group in range(10):
        print("==============================================================")
        print("[tournament play only one group(1)]")
        group = 0
        print("group:", group)
        redis_data = self.arena_tournament_clone.get_tournament_data(group)
        if not redis_data:
            print("!! not redis_data")
            return

        new_match_list = []
        win_user = []

        match_list = convert_string_to_array(redis_data[GAMECOMMON.R_TOURNAMENT_MATCH_LIST])
        if len(match_list) <= 0:
            print("!! len(match_list):", str(len(match_list)))
            return

        print("==============================================================")
        print("[begin matching arena tournament] remain_day:", remain_day)

        if 2 < remain_day:
            print("2 < remain_day")
            match_index = 0
            total_count = len(match_list)
            printProgressBar(0, total_count, prefix = 'Progress:', suffix = 'Complete', length = 20)
            progress = 0
            for matchs in match_list:
                if 2 <= len(win_user):
                    new_match_list.append([win_user[0], win_user[1]])
                    self.w_db['arenatournament'].update_arena_tournament(win_user[0], group, win_user[1], match_index, int(len(match_list) / 2))
                    self.w_db['arenatournament'].update_arena_tournament(win_user[1], group, win_user[0], match_index, int(len(match_list) / 2))
                    win_user = []
                    match_index += 1
                    # print("matchcount(match_index):", match_index)
                # else:
                #     print("win_user < 2")

                progress = progress + 1
                printProgressBar(progress, total_count, prefix = 'Progress:', suffix = 'Complete', length = 20)

                match_1 = self.w_db['arenatournament'].get_arena_tournament(matchs[0])
                match_2 = self.w_db['arenatournament'].get_arena_tournament(matchs[1])

                reward_rank = int(len(match_list) * 2)

                if not match_1 and not match_2: # 둘다 npc
                    win_user.append(0)
                elif not match_1 and match_2: # 부전승
                    win_user.append(match_2.auid)
                elif match_1 and not match_2: # 부전승
                    win_user.append(match_1.auid)
                else:
                    if match_1.point < match_2.point: # 포인트 높은사람
                        win_user.append(match_2.auid)
                        self.w_db['arenatournament'].update_arena_tournament_rank(match_1.auid, reward_rank)
                    elif match_1.point > match_2.point: # 포인트 높은사람
                        win_user.append(match_1.auid)
                        self.w_db['arenatournament'].update_arena_tournament_rank(match_2.auid, reward_rank)
                    else: # 포인트가 같을때
                        if match_1.battle_turn < match_2.point: # 배틀 턴을 덜쓴애
                            win_user.append(match_1.auid)
                            self.w_db['arenatournament'].update_arena_tournament_rank(match_2.auid, reward_rank)
                        elif match_1.battle_turn > match_2.point: # 배틀 턴을 덜쓴애
                            win_user.append(match_2.auid)
                            self.w_db['arenatournament'].update_arena_tournament_rank(match_1.auid, reward_rank)
                        else: # 배틀턴까지 같아
                            if match_1.auid < match_2.auid: # 유저 생성기준
                                win_user.append(match_1.auid)
                                self.w_db['arenatournament'].update_arena_tournament_rank(match_2.auid, reward_rank)
                            else: # 유저생성기준
                                win_user.append(match_2.auid)
                                self.w_db['arenatournament'].update_arena_tournament_rank(match_1.auid, reward_rank)

            print("end matching arena tournament Group:", group)

            if 2 <= len(win_user):
                new_match_list.append([win_user[0], win_user[1]])
                self.w_db['arenatournament'].update_arena_tournament(
                    win_user[0],
                    group,
                    win_user[1],
                    match_index,
                    int(len(match_list) / 2)
                )
                self.w_db['arenatournament'].update_arena_tournament(
                    win_user[1],
                    group,
                    win_user[0],
                    match_index,
                    int(len(match_list) / 2)
                )
                match_index += 1
                print("matching arena tournament Group : " + str(group) + "match count : " + str(match_index))

            self.arena_tournament.set_tournament_info(group, str(new_match_list))
            # end for matchs in match_list:

        elif 2 == remain_day:
            print("2 == remain_day")
            print("[semi_final_round]")
            self.semi_final_round(group, match_list, redis_data)
            # continue

        elif 1 == remain_day:
            print("1 == remain_day")
            print("[final_round]")
            self.final_round(group, match_list, redis_data)
            # continue


        print("==============================================================")
        print("round_day + 1:", db_arena_tournament_info.round_day + 1)
        print("[update_arena_tournament_day]")
        data_dict = {}
        data_dict[GAMECOMMON.R_TOURNAMENT_ROUND_DAY] = (db_arena_tournament_info.round_day + 1)
        pprint(data_dict)
        self.arena_tournament.set_tournament_data(GAMECOMMON.R_TOURNAMENT_INFO, data_dict)
        self.w_db['tourmentinfoadmin'].update_arena_tournament_day(db_arena_tournament_info.round_day + 1)

        print(datetime.now(), "end arena tournament daily/ ")

conf_dir = os.path.dirname(os.path.abspath(__file__)) + "/conf/"
service_ini = conf_dir + "service_local.ini"

if __name__ == '__main__':
    context = GameServerContext(
        inifile=service_ini,
        after_init=init_callback
    )

    service = RedisInitialize(context)
    #service.redis_flush()
    service.arena_tourment_battle_result()
