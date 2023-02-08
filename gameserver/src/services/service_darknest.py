# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


def getDarknestTicket(self, userinfo, ticket_max, increase_ticket):
    add_ticket = 0
    ticket_time = None
    darknest_charge_time = int(self.table.const_info.get(GAMECOMMON.DARKNEST_CHARGE_TIME).value)

    if userinfo.darknest_ticket < ticket_max:
        if userinfo.darknest_ticket_time:
            interval = self.begin - userinfo.darknest_ticket_time if userinfo.darknest_ticket_time else timedelta(
                seconds=ticket_max * darknest_charge_time)
            add_ticket = interval.seconds / darknest_charge_time
            if (userinfo.darknest_ticket + add_ticket) < ticket_max:
                if (userinfo.darknest_ticket + add_ticket + increase_ticket) < ticket_max:
                    add_time = timedelta(
                        seconds=interval.seconds / darknest_charge_time * darknest_charge_time)
                    ticket_time = userinfo.darknest_ticket_time + add_time
            else:
                add_ticket = ticket_max - userinfo.darknest_ticket
                if add_ticket < 0:
                    add_ticket = 0
        else:
            ticket_time = self.begin

    total_ticket= int(userinfo.darknest_ticket + add_ticket + increase_ticket)
    return (total_ticket, ticket_time)


class ServiceDarknest(object):

    def _get_next_darknest(self, curid):
        cur_idx = -1
        for idx, info in enumerate(self.table.darknest):
            if curid == info.id:
                cur_idx = idx
                break
        try:
            return self.table.darknest[cur_idx+1].id
        except:
            return self.table.darknest[0].id


    def _get_darknest_reward(self, curid, level):
        for info in self.table.darknest:
            if curid == info.id:
                for idx, reward in enumerate(info.rewards):
                    if idx == (level-1):
                        return reward
        return 0


    def DarknestInfo(self, response):
        darknest_respawn_time = int(self.table.const_info.get(GAMECOMMON.DARKNEST_RESPAWN_TIME).value)

        db_info = self.w_db['darknest'].get_darknest_info(self.userid)
        if not db_info:
            darknest_id = 1 #초기값 1
            darknest_dict = {}
            darknest_dict[darknest_id] = 1
            self.w_db['darknest'].insert_darknest_info(self.userid, darknest_id, self.begin, str(darknest_dict))

            response.result = Response.USER_INVALID
            return

        darknest_dict = convert_string_to_dict(db_info.boss_infos)
        if db_info.last_clear:
            darknest_dict[db_info.boss_id] += 1
            self.w_db['darknest'].update_darknest_level(self.userid, str(darknest_dict))

        remain_tick = time_diff_in_seconds(db_info.respawn_time)

        res_id = 0
        res_lv = 0
        res_time = 0
        if darknest_respawn_time <= remain_tick:
            # 리스폰 후
            darknest_id = ServiceDarknest._get_next_darknest(self, db_info.boss_id)
            update_time = self.begin - timedelta(seconds = remain_tick % darknest_respawn_time)
            
            level = 1
            if not darknest_dict.get(darknest_id, None):
                darknest_dict[darknest_id] = level
            else:
                level = darknest_dict[darknest_id]

            self.w_db['darknest'].update_darknest_info(self.userid, darknest_id, update_time, str(darknest_dict))

            res_id = darknest_id
            res_lv = level
            res_time = time_diff_in_seconds(update_time)
        else:
            # 리스폰 전
            res_id = db_info.boss_id
            res_lv = darknest_dict[db_info.boss_id]
            res_time = darknest_respawn_time - remain_tick

        response.darknest_info.id = res_id
        response.darknest_info.level = res_lv
        response.darknest_info.remain_time = res_time
        response.result = Response.SUCCESS
        return

    def DarknestStart(self, response):
        db_info = self.w_db['profile'].select_column(self.userid, "darknest_ticket, darknest_ticket_time, level")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        darknest_unlock_lv = int(self.table.const_info.get(GAMECOMMON.DARKNEST_UNLOCK).value)
        if db_info.level < darknest_unlock_lv:
            response.result = Response.CONTENT_LEVEL_LACK
            return

        darknest_ticket_max = int(self.table.const_info.get(GAMECOMMON.DARKNEST_TICKET_MAX).value)

        ticket, ticket_time = getDarknestTicket(self, db_info, darknest_ticket_max, 0)
        if 0 > ticket:
            response.result = Response.LACK_DARKNEST_TICKET
            return

        if not ticket_time:
            ticket_time = self.begin

        db_update = []
        value_list = []

        db_update.append('last_mode')
        value_list.append(GAMECOMMON.PLAY_MODE_DARKNEST)

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list)
        response.result = Response.SUCCESS
        return

    def DarknestEnd(self, response):
        db_info = self.w_db['profile'].select_column(self.userid, "money, last_mode, darknest_ticket, darknest_ticket_time")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        if db_info.last_mode != GAMECOMMON.PLAY_MODE_DARKNEST:
            response.result = Response.LAST_PLAY_MODE_WRONG
            return

        darknest_ticket_max = int(self.table.const_info.get(GAMECOMMON.DARKNEST_TICKET_MAX).value)
        darknest_charge_time = int(self.table.const_info.get(GAMECOMMON.DARKNEST_CHARGE_TIME).value)

        ticket, ticket_time = getDarknestTicket(self, db_info, darknest_ticket_max, 0)
        
        update_ticket = ticket - 1
        if 0 > update_ticket:
            response.result = Response.LACK_DARKNEST_TICKET
            return

        if update_ticket < darknest_ticket_max:
            ticket_time = self.begin

        response.darknest_end.darknest_ticket = update_ticket
        response.darknest_end.darknest_ticket_time = 0

        db_update = []
        value_list = []

        db_update.append('last_mode')
        value_list.append(0)

        db_update.append('darknest_ticket')
        value_list.append(update_ticket)

        str_column = "darknest_ticket_time=NULL"
        if ticket_time != None:
            str_column = "darknest_ticket_time='%s'" % ticket_time
            response.darknest_end.darknest_ticket_time = self.next_charge_second(
                ticket_time,
                darknest_charge_time
            )

        db_darknest = self.w_db['darknest'].get_darknest_info(self.userid)
        if not db_darknest:
            response.result = Response.USER_INVALID
            return

        darknest_dict = convert_string_to_dict(db_darknest.boss_infos)
        level = darknest_dict[db_darknest.boss_id]
        reward_set = ServiceDarknest._get_darknest_reward(self, db_darknest.boss_id, level)

        item_dict = self.get_reward_list(reward_set)
        self.reward_packet_process_profile(
            item_dict,
            response.darknest_end.reward_items,
            db_update,
            value_list,
            db_info
        )

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list, str_column)
        self.w_db['darknest'].update_darknest_clear(self.userid, True)
        response.result = Response.SUCCESS
        return

    def DarknestNextLevel(self, request, response):
        db_darknest = self.w_db['darknest'].get_darknest_info(self.userid)
        if not db_darknest:
            response.result = Response.DB_NOT_EXIST
            return

        if request.darknest_next_level.next_level < -1 or 1 < request.darknest_next_level.next_level:
            response.result = Response.FIELD_MISSING
            return

        darknest_dict = convert_string_to_dict(db_darknest.boss_infos)
        darknest_dict[db_darknest.boss_id] += request.darknest_next_level.next_level

        self.w_db['darknest'].update_darknest_level(self.userid, str(darknest_dict))
        response.result = Response.SUCCESS
        return