# -*- coding: utf-8 -*-
from random import randint

from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


class ServiceArenaTournament(object):
    def __init__(self):
        pass

    def Get_Info(self, response):
        # TODO: 아레나 토너먼트는 차후에 재구현
        remain_day = 0
        redis_data = self.arena_tournament_clone.get_tournament_data(GAMECOMMON.R_TOURNAMENT_INFO)
        if not redis_data:
            response.get_arena_info.season_time = 0
        else:
            end_day = int(redis_data[GAMECOMMON.R_TOURNAMENT_END_DAY])
            round_day = int(redis_data[GAMECOMMON.R_TOURNAMENT_ROUND_DAY])
            remain_day = end_day - round_day
            if remain_day <= 0:
                response.get_arena_info.season_time = 0
            else:
                end_time = datetime.now() + timedelta(days=remain_day)
                season_time = datetime(year=end_time.year, month=end_time.month, day=end_time.day, hour=0, minute=0)
                response.get_arena_info.season_time = time_diff_in_seconds(season_time)

        db_tournament_info = self.w_db['arenatournament'].get_arena_tournament(self.userid)
        if not db_tournament_info:
            response.result = Response.TOURNAMENT_NONE
            return

        mypoint = db_tournament_info.point
        if time_diff_in_seconds(db_tournament_info.battleStartTime) > 300 and db_tournament_info.battleProcessFlag == 1:
            self.w_db['arenatournament'].update_arena_tournament_battle_end(
                db_tournament_info.auid,
                db_tournament_info.point + 1,
                db_tournament_info.battle_turn
            )
            self.w_db['arenatournament'].update_arena_tournament_battle_target_end(
                db_tournament_info.target_auid,
                db_tournament_info.point + 1
            )
            mypoint = mypoint + 1

        db_target_info = self.w_db['arenatournament'].get_arena_tournament(db_tournament_info.target_auid)
        if not db_target_info:
            response.result = Response.SUCCESS
            return

        targetPoint = db_tournament_info.target_point
        if time_diff_in_seconds(db_target_info.battleStartTime) > 300 and db_target_info.battleProcessFlag == 1:
            self.w_db['arenatournament'].update_arena_tournament_battle_end(
                db_target_info.auid,
                db_target_info.point + 1,
                db_target_info.battle_turn
            )
            self.w_db['arenatournament'].update_arena_tournament_battle_target_end(
                self.userid, db_tournament_info.target_point + 1
            )
            targetPoint = targetPoint + 1

        response.get_arena_info.tournament_info.group = db_tournament_info.group
        response.get_arena_info.tournament_info.round = db_tournament_info.round
        response.get_arena_info.tournament_info.my_point =  mypoint
        response.get_arena_info.tournament_info.battle_count = db_tournament_info.battle_count
        response.get_arena_info.tournament_info.end_flag = db_tournament_info.end_flag
        response.get_arena_info.tournament_info.reward_flag = False
        response.get_arena_info.tournament_info.target_nick = ''
        response.get_arena_info.tournament_info.matchIndex = db_tournament_info.match_index
        response.get_arena_info.tournament_info.target_point = targetPoint

        if response.get_arena_info.season_time <= 0:
            response.get_arena_info.tournament_info.my_point = 0
            response.get_arena_info.tournament_info.battle_count = 0
            response.get_arena_info.tournament_info.end_flag = True

        if 0 < db_tournament_info.reward_rank:
            response.get_arena_info.tournament_info.reward_flag = True

        target_nick = self.cache_clone.get_user_data(db_target_info.auid, GAMECOMMON.R_USER_NICK)
        if target_nick:
            response.get_arena_info.tournament_info.target_nick = target_nick

        response.result = Response.SUCCESS
        return











    def reward(self, response):
        db_tournament_info = self.w_db['arenatournament'].get_arena_tournament(self.userid)
        if not db_tournament_info:
            response.result = Response.USER_INVALID
            return

        if False == db_tournament_info.end_flag:
            response.result = Response.TOURNAMENT_NOT_OVER
            return

        if 0 >= db_tournament_info.reward_rank:
            response.result = Response.INVALID_RESOURCE
            return

        try:
            # TODO: 버그 발생 있음 - 코드 체크.
            reward_id = self.reward[db_tournament_info.group+1][db_tournament_info.reward_rank]
        except:
            response.result = Response.INVALID_RESOURCE
            return

        item_dict = self.get_reward_list(reward_id)
        self.reward_packet_process(
            item_dict,
            response.arena_reward.reward_item
        )

        self.w_db['arenatournament'].update_arena_tournament_rank(self.userid, 0)

        response.result = Response.SUCCESS
        return


    def end_battle(self, request, response):
        db_tournament_info = self.w_db['arenatournament'].get_arena_tournament(self.userid)
        if not db_tournament_info:
            response.target_auidresult = Response.USER_INVALID
            return

        db_tournament_target_info = self.w_db['arenatournament'].get_arena_tournament(db_tournament_info.target_auid)
        if request.end_arena_battle.win_flag:
            self.w_db['arenatournament'].update_arena_tournament_battle_end(
                self.userid, db_tournament_info.point + 3,
                db_tournament_info.battle_turn + request.end_arena_battle.battle_turn + 1
            )
            self.w_db['arenatournament'].update_arena_tournament_battle_target_end(
                db_tournament_info.target_auid,
                db_tournament_target_info.target_point + 3
            )
        else:
            self.w_db['arenatournament'].update_arena_tournament_battle_end(
                self.userid,
                db_tournament_info.point + 1,
                db_tournament_info.battle_turn + request.end_arena_battle.battle_turn + 1
            )
            self.w_db['arenatournament'].update_arena_tournament_battle_target_end(
                db_tournament_info.target_auid,
                db_tournament_target_info.target_point + 1
            )

        response.result = Response.SUCCESS
        return


    def start_battle(self, request, response):
        db_tournament_info = self.w_db['arenatournament'].get_arena_tournament(self.userid)
        if not db_tournament_info:
            response.result = Response.USER_INVALID
            return

        if db_tournament_info.battle_count <= 0:
            response.result = Response.ARENA_TICKET_LACK
            return

        if db_tournament_info.target_auid <= 0:
            response.result = Response.ARENA_TICKET_LACK
            return

        self.w_db['arenatournament'].update_arena_tournament_battle_start(self.userid, datetime.now())

        response.result = Response.SUCCESS
        return


    def get_match(self,  response):
        db_tournament_info = self.w_db['arenatournament'].get_arena_tournament(self.userid)
        if not db_tournament_info:
            response.target_auidresult = Response.USER_INVALID
            return

        redis_data = self.cache_clone.get_user_profile(db_tournament_info.target_auid)
        if not redis_data:
            response.result = Response.USER_INVALID
            return

        matchInfo = response.get_arena_match_list.match_users.add()
        matchInfo.rank = db_tournament_info.round
        matchInfo.name = redis_data[GAMECOMMON.R_USER_NICK]
        matchInfo.level = int(redis_data[GAMECOMMON.R_USER_LEVEL])
        matchInfo.avatar_id = int(redis_data[GAMECOMMON.R_USER_AVATAR_ID])
        matchInfo.uid = db_tournament_info.target_auid

        # TODO: redis team info 삭제 예정
        team_info = redis_data[GAMECOMMON.R_USER_TEAM_INFO]

        self.convert_team_data_redis_to_protobuf(matchInfo.team_info, team_info)

        if 0 != int(redis_data[GAMECOMMON.R_USER_GUILD_UID]):
            guild_redis = self.guild_clone.get_guild_info(redis_data[GAMECOMMON.R_USER_GUILD_UID])
            if guild_redis:
                matchInfo.guildinfo.guild_uid = int(redis_data[GAMECOMMON.R_USER_GUILD_UID])
                matchInfo.guildinfo.guild_name = guild_redis[GAMECOMMON.GUILD_NAME]
                matchInfo.guildinfo.guild_bg = int(guild_redis[GAMECOMMON.GUILD_BG])
                matchInfo.guildinfo.guild_emblem = int(guild_redis[GAMECOMMON.GUILD_EMBLEM])

        response.result = Response.SUCCESS
