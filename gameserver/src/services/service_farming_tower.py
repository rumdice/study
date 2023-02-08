# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


def addFarmingTower(self):
    cur_time = datetime.now()
    uid_idx = int(cur_time.hour / 4)
    
    farming_tower_hour = [24, 4, 8, 12, 16, 20]
    tower_uid = farming_tower_hour[uid_idx]
    db_tower = self.w_db['farmingtower'].find_tower(self.userid, tower_uid)
    if not db_tower:
        generatorFarmingTower(self, tower_uid, True)
        return

    if db_tower.end_time <= cur_time:
        generatorFarmingTower(self, tower_uid)

def generatorFarmingTower(self, tower_uid, add_flag=False):
    db_tower = self.w_db['farmingtower'].select_all_tower(self.userid)
    if not db_tower:
        db_tower = {}

    remove_faming_id = []
    for tower in db_tower:
        if tower.end_time > datetime.now():
            remove_faming_id.append(tower.tower_id)

    farming_list = []
    randomMax = 0
    for key, value in self.table.farming_tower.items():
        if value.farming_id in remove_faming_id:
            continue

        farming_list.append([value.farming_id, randomMax + value.prob])
        randomMax += value.prob

    prob_value = random.randint(0, randomMax)
    generator_id = 0
    for value in farming_list:
        if value[1] >= prob_value:
            generator_id = value[0]
            break

    cur_time = datetime.now()
    end_time = datetime(cur_time.year, cur_time.month, cur_time.day) + timedelta(
        hours=(tower_uid + 10))

    if add_flag:
        self.w_db['farmingtower'].add_farming_tower(self.userid, tower_uid, generator_id, end_time)
    else:
        self.w_db['farmingtower'].update_farming_tower(self.userid, tower_uid, generator_id, end_time)


class ServiceFarmingTower(object):
    def GetFarmingTower(self, response):
        addFarmingTower(self)

        db_tower = self.w_db['farmingtower'].select_all_tower(self.userid)
        if not db_tower:
            return

        for tower in db_tower:
            if tower.end_time <= self.begin:
                continue

            farmingInfo = response.get_farming_tower.farming_list.add()
            farmingInfo.tower_uid = tower.tower_uid
            farmingInfo.tower_id = tower.tower_id
            farmingInfo.remain_time = time_diff_in_seconds(tower.end_time)
            farmingInfo.clear_floor = tower.clear_floor

        response.result = Response.SUCCESS
        return

    def StartFarmingTower(self, request, response):
        db_info = self.w_db['profile'].select_column(self.userid, "stamina_cur, stamina_max, stamina_time")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        db_tower = self.w_db['farmingtower'].find_tower(self.userid, request.start_farming_tower.tower_uid)
        if not db_tower:
            response.result = Response.INVALID_TOWER
            return

        if db_tower.end_time <= self.begin:
            response.result = Response.TIME_OUT_TOWER
            return

        tower_data = self.table.farming_tower.get(db_tower.tower_id, None)
        if not tower_data:
            response.result = Response.INVALID_RESOURCE
            return

        if len(tower_data.floor_info) < request.start_farming_tower.start_floor:
            response.result = Response.INVALID_RESOURCE
            return

        floor_info = tower_data.floor_info[request.start_farming_tower.start_floor - 1]
        stamina, stamina_time = self.get_stamina(db_info, db_info.stamina_max, 0)
        update_stamina = stamina - floor_info.use_stamina

        if 0 > update_stamina:
            response.result = Response.LACK_STAMINA
            return

        if update_stamina < db_info.stamina_max:
            stamina_time = self.begin

        response.start_farming_tower.total_stamina = update_stamina
        response.start_farming_tower.stamina_time = 0

        db_update = []
        value_list = []

        db_update.append('last_mode')
        value_list.append(GAMECOMMON.PLAY_MODE_FARMING_TOWER)

        db_update.append('stamina_cur')
        value_list.append(update_stamina)

        str_column = "stamina_time=NULL"
        stamina_charge_time = int(self.table.const_info.get(GAMECOMMON.STAMINA_TIME).value)
        if stamina_time != None:
            str_column = "stamina_time='%s'" % (stamina_time)
            response.start_farming_tower.stamina_time = self.next_charge_second(
                stamina_time,
                stamina_charge_time
            )

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list, str_column)
        self.w_db['farmingtower'].update_clear_floor(
            self.userid,
            db_tower.tower_uid,
            request.start_farming_tower.start_floor
        )
        response.result = Response.SUCCESS
        return

    def ClearFarmingTower(self, request, response):
        db_info = self.w_db['profile'].select_column(self.userid, "last_mode, cash, money, level, exp")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        if db_info.last_mode != GAMECOMMON.PLAY_MODE_FARMING_TOWER:
            response.result = Response.LAST_PLAY_MODE_WRONG
            return

        db_tower = self.w_db['farmingtower'].find_tower(self.userid, request.clear_farming_tower.tower_uid)
        if not db_tower:
            response.result = Response.INVALID_TOWER
            return

        if request.clear_farming_tower.clear_floor != db_tower.clear_floor:
            response.result = Response.LAST_PLAY_MODE_WRONG
            return

        tower_info = self.table.farming_tower.get(db_tower.tower_id, None)
        if not tower_info:
            response.result = Response.INVALID_RESOURCE
            return

        floor_info = tower_info.floor_info[request.clear_farming_tower.clear_floor - 1]

        db_update = []
        db_update.append('last_mode')
        
        value_list = []
        value_list.append(0) #종료되었으므로 원래상태로 되돌림
        
        item_dict = self.get_reward_list(floor_info.reward)
        self.reward_packet_process_profile(
            item_dict,
            response.clear_farming_tower.reward_items,
            db_update,
            value_list,
            db_info
        )

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list)
        self.w_db['farmingtower'].update_clear_floor(
            self.userid,
            db_tower.tower_uid,
            request.clear_farming_tower.clear_floor
        )

        response.clear_farming_tower.tower_uid = db_tower.tower_uid
        response.clear_farming_tower.clear_floor = request.clear_farming_tower.clear_floor
        response.result = Response.SUCCESS
        return