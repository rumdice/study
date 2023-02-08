# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


def get_reward(self, reward_id):
    item_dict = {}
    reward_set = self.table.reward_set.get(reward_id, None)
    if not reward_set:
        self.logger.error("reward_set not exists : reward_id({})".format(reward_id))
        return
    for prob in reward_set:
        self.table.get_reward_item_by_prob(prob, item_dict)
    return item_dict


class ServiceEndlessTower(object):
    def GetEndlessTower(self, response):
        db_tower = self.w_db['endlesstower'].select_tower(self.userid)
        clear_floor = 0
        if not db_tower:
            clear_floor = 0
        for tower in db_tower:
            clear_floor = tower.clear_floor
        response.get_endless_tower.clear_floor = clear_floor
        response.result = Response.SUCCESS
        return

    def StartEndlessTower(self, request, response):
        db_tower = self.w_db['endlesstower'].select_tower(self.userid)
        clear_floor = 0
        if not db_tower:
            self.w_db['endlesstower'].add_endless_tower(self.userid)
            clear_floor = 0
        for tower in db_tower:
            clear_floor = tower.clear_floor

        if (clear_floor + 1) != request.start_endless_tower.start_floor:
            response.result = Response.INVALID_VALUE
            return

        self.w_db['profile'].update_last_mode(self.userid, GAMECOMMON.PLAY_MODE_ENDLESS_TOWER)
        response.result = Response.SUCCESS
        return

    def ClearEndlessTower(self, request, response):
        db_info = self.w_db['profile'].select_column(self.userid, "last_mode, cash, money, level, exp")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        if db_info.last_mode != GAMECOMMON.PLAY_MODE_ENDLESS_TOWER:
            response.result = Response.LAST_PLAY_MODE_WRONG
            return

        tower_info = self.table.endless_tower
        if not tower_info:
            response.result = Response.INVALID_TOWER
            return

        db_update = []
        db_update.append('last_mode')
        
        value_list = []
        value_list.append(0)
        
        reward_set = tower_info[request.clear_endless_tower.clear_floor].reward
        item_dict = get_reward(self, reward_set)
        self.reward_packet_process_profile(
            item_dict,
            response.clear_endless_tower.reward_items,
            db_update,
            value_list,
            db_info
        )

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list)
        self.w_db['endlesstower'].update_clear_floor(self.userid, request.clear_endless_tower.clear_floor)

        response.result = Response.SUCCESS
        return