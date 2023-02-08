# -*- coding: utf-8 -*-
from bisect import bisect_right

from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *
from src.services.service_common import *


class ServiceRegion(object):
    def SaveRegion(self, request, response):
        self.w_db['regioninfo'].update_region_info(
            self.userid, 
            request.save_region.region_num,
            request.save_region.region_difficulty, 
            request.save_region.step
        )

        response.result = Response.SUCCESS
        return

    def StartRegion(self, request, response):
        db_info = self.w_db['profile'].select_column(self.userid, "stamina_cur, stamina_max, stamina_time")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        floor_dict = self.table.region_list.get(request.start_region.region_num, None)
        if not floor_dict:
            response.result = Response.INVALID_RESOURCE
            return

        difficulty_dict = floor_dict.get(0, None)
        if not difficulty_dict:
            response.result = Response.INVALID_RESOURCE
            return

        reward_check = difficulty_dict.get(request.start_region.region_difficulty, None)
        if not reward_check.use_stamina:
            response.result = Response.INVALID_RESOURCE
            return

        stamina, stamina_time = self.get_stamina(db_info, db_info.stamina_max, 0)
        update_stamina = stamina - reward_check.use_stamina

        if 0 > update_stamina:
            response.result = Response.LACK_STAMINA
            return

        if update_stamina < db_info.stamina_max:
            stamina_time = self.begin

        response.start_region.total_stamina = update_stamina
        response.start_region.stamina_time = 0

        db_update = []
        value_list = []

        db_update.append('last_mode')
        value_list.append(GAMECOMMON.PLAY_MODE_REGION)

        db_update.append('stamina_cur')
        value_list.append(update_stamina)

        str_column = "stamina_time=NULL"
        
        stamina_charge_time = int(self.table.const_info.get(GAMECOMMON.STAMINA_TIME).value)
        if stamina_time != None:
            str_column = "stamina_time='%s'" % (stamina_time)
            response.start_region.stamina_time = self.next_charge_second(stamina_time, stamina_charge_time)

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list, str_column)
        self.w_db['regioninfo'].update_region_info(
            self.userid, 
            request.start_region.region_num,
            request.start_region.region_difficulty, 
            0
        )

        response.result = Response.SUCCESS
        return
    
    def RewardRegion(self, request, response):
        db_profile = self.w_db['profile'].select_column(self.userid, "last_mode, cash, money, exp, level")
        if not db_profile:
            response.result = Response.INVALID_PROFILE
            return

        if db_profile.last_mode != GAMECOMMON.PLAY_MODE_REGION:
            response.result = Response.LAST_PLAY_MODE_WRONG
            return

        db_info = self.w_db['regioninfo'].select_region_info(self.userid)
        if not db_info:
            response.result = Response.INVALID_USER
            return

        if db_info.region_step <= 0:
            response.reward_region.CopyFrom(Response.RewardRegion())
            response.result = Response.SUCCESS
            return

        floor_dict = self.table.region_list.get(db_info.region_num, None)
        if not floor_dict:
            response.result = Response.INVALID_RESOURCE
            return

        difficulty_dict = floor_dict.get(0, None)
        if not difficulty_dict:
            response.result = Response.INVALID_RESOURCE
            return

        reward_check = difficulty_dict.get(db_info.region_difficulty, None)
        if not reward_check:
            response.result = Response.INVALID_RESOURCE
            return
        if not reward_check.use_stamina:
            response.result = Response.INVALID_RESOURCE
            return

        item_dict = {}
        reward_step_count = db_info.region_step
        if reward_check.total_step < db_info.region_step:
            response.result = Response.INVALID_RESOURCE
            return

        if reward_step_count == reward_check.total_step:
            db_missin_info = self.w_db['regionmission'].get_region_mission(
                self.userid, 
                db_info.region_num,
                db_info.region_difficulty
            )

            if not db_missin_info:
                self.w_db['regionmission'].add_region_mission(
                    self.userid, 
                    db_info.region_num,
                    db_info.region_difficulty,
                    str([False, False, False, False, False])
                )

            reward_step_count -= 1
            reward_set = self.table.reward_set.get(reward_check.reward_boss, None)
            if not reward_set:
                response.result = Response.INVALID_RESOURCE
                return

            for prob in reward_set:
                self.table.get_reward_prob_item(prob, item_dict)

        reward_set = self.table.reward_set.get(reward_check.reward_step, None)
        if not reward_set:
            response.result = Response.INVALID_RESOURCE
            return

        for i in range(reward_step_count):
            for prob in reward_set:
                self.table.get_reward_item_by_prob(prob, item_dict)

        db_update = []
        value_list = []

        db_update.append('last_mode')
        value_list.append(GAMECOMMON.PLAY_MODE_REGION_REWARD)

        response.reward_region.region_num = db_info.region_num
        response.reward_region.region_difficulty = db_info.region_difficulty
        response.reward_region.region_step = reward_step_count

        for key, item in item_dict.items():
            if item.item_type in ServiceCommon.item_type_stack_list:
                packet_item = response.reward_region.reward_list.add()
                packet_item.item_id = item.item_id
                packet_item.item_type = item.item_type
                packet_item.count = item.count
                if item.item_id == GAMECOMMON.ITEM_RUBY_ID:
                    update_cash = db_profile.cash + item.count
                    db_update.append('cash')
                    value_list.append(update_cash)
                elif item.item_id == GAMECOMMON.ITEM_GOLD_ID:
                    update_money = db_profile.money + item.count
                    db_update.append('money')
                    value_list.append(update_money)
                elif item.item_id == GAMECOMMON.ITEM_USER_EXP:
                    user_redis = self.cache_clone.get_user_profile(self.userid)
                    db_level = db_profile.level
                    next_level_exp = self.table.user_level_exp_list[db_level]
                    update_exp = db_profile.exp + item.count
                    next_level = db_level
                    if next_level_exp < update_exp:
                        next_level = bisect_right(self.table.user_exp_level_list, update_exp)
                        db_update.append('level')
                        value_list.append(next_level)
                        pass
                    if user_redis:
                        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_EXP, update_exp)
                        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_LEVEL, next_level)
                    db_update.append('exp')
                    value_list.append(update_exp)
                else:
                    etc_item = self.w_db['etcinven'].find_item(self.userid, item.item_id)
                    if not etc_item:
                        self.w_db['etcinven'].add_item(self.userid, item.item_id, item.count)
                    else:
                        etc_count = etc_item.item_count + item.count
                        self.w_db['etcinven'].update_item_count(self.userid, item.item_id, etc_count)

            else:
                self.logger.error("Unknown item_type:{}".format(item.item_type))
                pass

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list)
        self.w_db['regioninfo'].update_region_info(self.userid, 0, 0, 0)

        response.result = Response.SUCCESS
        return


    def RegionMissionReward(self, request, response):
        db_profile = self.w_db['profile'].select_column(self.userid, "last_mode, cash, money")
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        if db_profile.last_mode != GAMECOMMON.PLAY_MODE_REGION_REWARD:
            response.result = Response.LAST_PLAY_MODE_WRONG
            return

        db_missin_info = self.w_db['regionmission'].get_region_mission(
            self.userid,
            request.region_mission_reward.region_id,
            request.region_mission_reward.difficulty
        )

        if not db_missin_info:
            response.result = Response.USER_INVALID
            return

        if 5 < len(request.region_mission_reward.clear_list):
            response.result = Response.INVALID_VALUE
            return

        try:
            mission_reward_data = self.table.region_mission_list[db_missin_info.region_id][db_missin_info.difficulty]
        except Exception as e:
            self.logger.exception("region_mission_reward {}".format(e.message))
            response.result = Response.INVALID_VALUE
            return

        before_reward = 0
        clear_list = convert_string_to_array(db_missin_info.reward_list)
        for flag in clear_list:
            if flag:
                before_reward += 1

        after_reward = 0
        for flag in request.region_mission_reward.clear_list:
            if flag:
                after_reward += 1

        if before_reward >= after_reward:
            response.region_mission_reward.CopyFrom(Response.RegionMissionReward())
            response.result = Response.SUCCESS
            return

        reward_list = []
        reward_index = after_reward - before_reward
        for idx in range(reward_index):
            reward_list.append(mission_reward_data[before_reward + idx])

        item_dict = {}
        for reward_id in reward_list:
            reward_set = self.table.reward_set.get(reward_id, None)
            if not reward_set:
                return

            for prob in reward_set:
                self.table.get_reward_item_by_prob(prob, item_dict)

        db_update = []
        value_list = []

        db_update.append('last_mode')
        value_list.append(0)

        self.reward_packet_process_profile(
            item_dict,
            response.region_mission_reward.reward_item,
            db_update,
            value_list,
            db_profile
        )

        self.w_db['regionmission'].update_region_mission(
            self.userid,
            request.region_mission_reward.region_id,
            request.region_mission_reward.difficulty,
            str(request.region_mission_reward.clear_list)
        )

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list)

        response.result = Response.SUCCESS
        return


    def RegionMissionClearInfo(self, response):
        db_missin_info = self.w_db['regionmission'].region_mission_all(self.userid)
        if 1 > len(db_missin_info):
            response.region_mission_clear_info.CopyFrom(Response.RegionMissionClearInfo())
            response.result = Response.SUCCESS
            return

        for info in db_missin_info:
            clearInfo = response.region_mission_clear_info.clear_list.add()
            clearInfo.region_id = info.region_id
            clearInfo.difficulty = info.difficulty
            clear_list = convert_string_to_array(info.reward_list)
            clearInfo.clear_list.extend(clear_list)

        response.result = Response.SUCCESS
        return
    
    def RegionRewardCheck(self, response):
        db_info = self.w_db['profile'].select_column(self.userid, "last_mode")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        response.region_reward_check.checkFlag = 0
        if db_info.last_mode == GAMECOMMON.PLAY_MODE_REGION:
            response.region_reward_check.checkFlag = 1

        response.result = Response.SUCCESS
        return