# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


class ServiceEventDungeon(object):
    def StartEventDungeon(self, request, response):
        db_info = self.w_db['profile'].select_column(self.userid, "stamina_cur, stamina_max, stamina_time, level")
        if not db_info:
            response.result = Response.INVALID_PROFILE
            return

        dungeon_unlock_lv = int(self.table.const_info.get(GAMECOMMON.DUNGEON_UNLOCK).value)
        if db_info.level < dungeon_unlock_lv:
            response.result = Response.CONTENT_LEVEL_LACK
            return

        db_dungeon = self.w_db['eventdungeonadmin'].get_event_dungeon(request.start_event_dungeon.start_dungeon_uid)
        if not db_dungeon:
            response.result = Response.EVENT_DUNGEON_CLOSE
            return
        if self.begin < db_dungeon.start_time:
            response.result = Response.EVENT_DUNGEON_CLOSE
            return
        if self.begin > db_dungeon.end_time:
            response.result = Response.EVENT_DUNGEON_CLOSE
            return

        checkDungeonTypeList = [
            Define.DUNGEON_TYPE_ROGUELIKE,
            Define.DUNGEON_TYPE_GIMMICK_NORMAL,
            Define.DUNGEON_TYPE_JOIN_CONDITION,
            Define.DUNGEON_TYPE_ENTER_ONCE
        ]

        dungeonType = db_dungeon.dungeon_type
        if dungeonType not in checkDungeonTypeList:
            response.result = Response.INVALID_EVENT_DUNGEON_TYPE
            return

        db_event_dungeon = self.w_db['eventdungeon'].get_event_dungeon(self.userid, request.start_event_dungeon.start_dungeon_uid)
        if not db_event_dungeon:
            response.result = Response.DB_NOT_EXIST
            return

        if dungeonType in [Define.DUNGEON_TYPE_ENTER_ONCE]:
            hero_uids_set = set(request.start_event_dungeon.hero_uids)
            use_ids_set = convert_string_to_set(db_event_dungeon.use_ids)
            exists = use_ids_set.intersection(hero_uids_set)
            if exists:
                response.result = Response.ID_IN_USE
                return

        db_update = []
        value_list = []
        db_update.append('last_mode')
        value_list.append(GAMECOMMON.PLAY_MODE_EVENT_DUNGEON)
        db_update.append('last_stage')
        value_list.append(request.start_event_dungeon.start_dungeon_stage)

        self.w_db['eventdungeon'].update_event_dungeon_difficulty(
            self.userid,
            request.start_event_dungeon.start_dungeon_uid,
            request.start_event_dungeon.param3
        )

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list)

        response.result = Response.SUCCESS
        return

    def EndEventDungeon(self, request, response):
        db_info = self.w_db['profile'].select_column(self.userid, "last_mode, last_stage")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        if db_info.last_mode != GAMECOMMON.PLAY_MODE_EVENT_DUNGEON:
            response.result = Response.LAST_PLAY_MODE_WRONG
            return

        db_dungeon = self.w_db['eventdungeonadmin'].get_event_dungeon(request.end_event_dungeon.end_dungeon_uid)
        if not db_dungeon:
            response.result = Response.EVENT_DUNGEON_CLOSE
            return

        dungeonType = db_dungeon.dungeon_type
        if dungeonType not in [Define.DUNGEON_TYPE_ROGUELIKE, Define.DUNGEON_TYPE_GIMMICK_NORMAL, Define.DUNGEON_TYPE_JOIN_CONDITION, Define.DUNGEON_TYPE_ENTER_ONCE]:
            response.result = Response.INVALID_EVENT_DUNGEON_TYPE
            return

        if dungeonType in [Define.DUNGEON_TYPE_ENTER_ONCE]:
            pass

        if dungeonType in [Define.DUNGEON_TYPE_GIMMICK_NORMAL, Define.DUNGEON_TYPE_JOIN_CONDITION, Define.DUNGEON_TYPE_ENTER_ONCE]:
            if db_info.last_stage != request.end_event_dungeon.param2:
                response.result = Response.LAST_PLAY_MODE_WRONG
                return
            reward_id = 0
            try:
                if dungeonType == Define.DUNGEON_TYPE_GIMMICK_NORMAL:
                    reward_id = self.table.dungeon_gimmick[request.end_event_dungeon.param1][request.end_event_dungeon.param2].reward_id
                elif dungeonType == Define.DUNGEON_TYPE_JOIN_CONDITION:
                    reward_id = self.table.join_condition[request.end_event_dungeon.param1][request.end_event_dungeon.param2]
                elif dungeonType == Define.DUNGEON_TYPE_ENTER_ONCE:
                    reward_id = self.table.enter_once[request.end_event_dungeon.param1][request.end_event_dungeon.param2]
            except Exception as e:
                self.logger.error("event dungeon reward error {}".format(e.message))
                response.result = Response.INVALID_RESOURCE
                return

            use_ids = []
            item_dict = self.get_reward_list(reward_id)

            if dungeonType in [Define.DUNGEON_TYPE_GIMMICK_NORMAL, Define.DUNGEON_TYPE_JOIN_CONDITION]:
                self.w_db['eventdungeon'].update_event_dungeon(
                    self.userid,
                    request.end_event_dungeon.end_dungeon_uid,
                    request.end_event_dungeon.param1,
                    request.end_event_dungeon.param2,
                    str(use_ids)
                )
            elif dungeonType in [Define.DUNGEON_TYPE_ENTER_ONCE]:
                db_user_data = self.w_db['eventdungeon'].get_event_dungeon(
                    self.userid,
                    request.end_event_dungeon.end_dungeon_uid
                )
                if not db_user_data:
                    response.result = Response.EVENT_DUNGEON_CLOSE
                    return

                use_ids_set = convert_string_to_set(db_user_data.use_ids)
                use_ids_set.update(request.end_event_dungeon.hero_uids)
                use_ids_set_str = convert_set_to_string(use_ids_set)

                win_flag = request.end_event_dungeon.win_flag
                if win_flag == True:
                    self.w_db['eventdungeon'].update_event_dungeon(
                        self.userid,
                        request.end_event_dungeon.end_dungeon_uid,
                        request.end_event_dungeon.param1,
                        request.end_event_dungeon.param2,
                        use_ids_set_str
                    )
                else:
                    self.w_db['eventdungeon'].update_event_dungeon_ids(
                        self.userid,
                        request.end_event_dungeon.end_dungeon_uid,
                        use_ids_set_str
                    )
            else:
                self.logger.error("event dungeon type error {}".format(e.dungeonType))
                response.result = Response.INVALID_EVENT_DUNGEON_TYPE
                return

            self.reward_packet_process(
                item_dict,
                response.end_event_dungeon.reward_list
            )
            response.result = Response.SUCCESS
            return

        elif dungeonType in [Define.DUNGEON_TYPE_ROGUELIKE]:
            db_event_dungeon = self.w_db['eventdungeon'].get_event_dungeon(
                self.userid,
                request.end_event_dungeon.end_dungeon_uid
            )

            if not db_event_dungeon:
                response.result = Response.EVENT_DUNGEON_CLOSE
                return

            if db_event_dungeon.param1 < request.end_event_dungeon.param1:
                if 1 != request.end_event_dungeon.param2:
                    response.result = Response.FAILURE
                    return
            else:
                if (db_event_dungeon.param2 + 1) < request.end_event_dungeon.param2:
                    response.result = Response.FAILURE
                    return

            if db_event_dungeon.param1 > request.end_event_dungeon.param1:
                response.result = Response.SUCCESS
                return

            if db_event_dungeon.param2 > request.end_event_dungeon.param2:
                if db_event_dungeon.param1 < request.end_event_dungeon.param1:
                    self.w_db['eventdungeon'].update_event_dungeon(
                        self.userid,
                        request.end_event_dungeon.end_dungeon_uid,
                        request.end_event_dungeon.param1,
                        request.end_event_dungeon.param2,
                        "[]"
                    )
                    response.end_event_dungeon.CopyFrom(Response.EndEventDungeon())
                    response.result = Response.SUCCESS
                    return
                response.result = Response.SUCCESS
                return

            if db_event_dungeon.end_time < self.begin:
                response.result = Response.EVENT_DUNGEON_CLOSE
                return

            self.w_db['eventdungeon'].update_event_dungeon(
                self.userid,
                request.end_event_dungeon.end_dungeon_uid,
                request.end_event_dungeon.param1,
                request.end_event_dungeon.param2, 
                "[]"
            )

            response.end_event_dungeon.CopyFrom(Response.EndEventDungeon())
            response.result = Response.SUCCESS
        else:
            self.logger.error("event dungeon type error {}".format(e.dungeonType))
            response.result = Response.INVALID_EVENT_DUNGEON_TYPE
        
        return


    def GetEventDungeon(self, request, response):
        req_is_entered = request.get_event_dungeon.is_entered # 유저가 고대던전 화면에 들어갔다 나옴에 여부에 대한 값. 들어갔으면 1 아니면 0
        
        # 고대던전들 중 어느것 하나라도 리스폰 되었을때 또는 새로운 던전이 추가가 되었을때. 1. 그 외는 0
        res_is_entered = False
        
        db_dungeons = self.w_db['eventdungeonadmin'].get_event_dungeon_all()
        if not db_dungeons:
            response.get_event_dungeon.CopyFrom(Response.GetEventDungeon())
            response.result = Response.SUCCESS
            return

        for dungeon in db_dungeons:
            # 현재 시간이 던전의 시작 시간 보다 작다 - 만료됨
            if self.begin < dungeon.start_time:
                res_is_entered = True
                continue
            # 현재 시간이 던전의 종료 시간 보다 크다 - 만료됨
            if self.begin >= dungeon.end_time:
                res_is_entered = True
                continue

            dungeonInfo = response.get_event_dungeon.dungeon_list.add()
            dungeonInfo.dungeon_uid = dungeon.uid
            dungeonInfo.dungeon_type = dungeon.dungeon_type
            dungeonInfo.group_id = dungeon.dungeon_id
            dungeonInfo.remain_time = time_diff_in_seconds(dungeon.end_time)
            
            db_dungeon = self.w_db['eventdungeon'].get_event_dungeon(self.userid, dungeonInfo.dungeon_uid)
            if not db_dungeon:
                self.w_db['eventdungeon'].add_event_dungeon(
                    self.userid,
                    dungeonInfo.dungeon_uid,
                    dungeonInfo.group_id,
                    dungeonInfo.dungeon_type,
                    dungeon.end_time
                )
                dungeonInfo.param1 = 0
                dungeonInfo.param2 = 0
                dungeonInfo.param3 = 0
                dungeonInfo.reward = 0
                res_is_entered = True
            else:
                dungeonInfo.param1 = db_dungeon.param1
                dungeonInfo.param2 = db_dungeon.param2
                dungeonInfo.param3 = db_dungeon.param3
                dungeonInfo.reward = db_dungeon.reward_value
                id_list = convert_string_to_array(db_dungeon.use_ids)
                dungeonInfo.use_ids.extend(id_list)

            if req_is_entered == True:
                res_is_entered = False

            dungeonInfo.flag = res_is_entered

        response.result = Response.SUCCESS
        return

    def EventDungeonReward(self, request, response):
        db_event_dungeon = self.w_db['eventdungeon'].get_event_dungeon(self.userid, request.event_dungeon_reward.dungeon_uid)
        if not db_event_dungeon:
            response.result = Response.EVENT_DUNGEON_CLOSE
            return

        if db_event_dungeon.end_time < self.begin:
            response.result = Response.EVENT_DUNGEON_CLOSE
            return

        if db_event_dungeon.dungeon_type == Define.DUNGEON_TYPE_ROGUELIKE:
            if db_event_dungeon.param1 < request.event_dungeon_reward.value1:
                response.result = Response.EVENT_DUNGEON_CLOSE
                return
            else:
                if request.event_dungeon_reward.value1 == db_event_dungeon.param1:
                    if db_event_dungeon.param2 < request.event_dungeon_reward.value2:
                        response.result = Response.EVENT_DUNGEON_CLOSE
                        return

            reward_value = (request.event_dungeon_reward.value1 * 100) + request.event_dungeon_reward.value2
            if reward_value <= db_event_dungeon.reward_value:
                response.result = Response.EVENT_DUNGEON_CLOSE
                return

            self.w_db['eventdungeon'].reward_event_dungeon(
                self.userid,
                request.event_dungeon_reward.dungeon_uid,
                reward_value
            )

            reward_set = self.table.event_rogue_like[db_event_dungeon.param3][request.event_dungeon_reward.value1][request.event_dungeon_reward.value2]
            item_dict = self.get_reward_list(reward_set)
            self.reward_packet_process(
                item_dict,
                response.event_dungeon_reward.reward_item
            )

        response.result = Response.SUCCESS
        return