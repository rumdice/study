# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *
from src.services.service_research import *


def resourceBuildingReward(self, db_territory, build_info_dict, level, packetItem, maxStorage):
    build_reward = build_info_dict[level]
    reward_time = time_diff_in_seconds(db_territory.start_time)
    produce_count = int((reward_time / 60) * build_reward.produce) # 1분당 자원 생산량

    # 연구소 효과 적용
    # 1분당 생산한 생산량이 100 이라 치면 10% 시 110
    add_produce = ReserchAffectTerritoryRewardProduceMin(self, produce_count)
    produce_count = produce_count + add_produce

    # 연구소 효과 적용
    # 1렙 밀농장 100 저장량이면 10% 추가 110
    add_max_qty = ReserchAffectTerritoryRewardMaxQTY(self, build_reward.max_qty)
    build_reward.max_qty = build_reward.max_qty + add_max_qty

    if produce_count > build_reward.max_qty:
        produce_count = build_reward.max_qty

    resItem = packetItem.add()

    build_type_item = {
        Define.BUILDING_TYPE_FIELD: GAMECOMMON.ITEM_FOOD_ID,
        Define.BUILDING_TYPE_MINE: GAMECOMMON.ITEM_IRON_ID,
        Define.BUILDING_TYPE_QUARRY: GAMECOMMON.ITEM_STONE_ID,
        Define.BUILDING_TYPE_LUMBER_MILL: GAMECOMMON.ITEM_WOOD_ID,
    }

    resItem.item_id = build_type_item[db_territory.building_type]
    resItem.count = produce_count

    if 0 < produce_count:
        db_etcitem = self.w_db['etcinven'].find_item(self.userid, resItem.item_id)
        update_count = db_etcitem.item_count + produce_count
        if update_count > maxStorage:
            update_count = maxStorage

        self.w_db['etcinven'].update_item_count(self.userid, resItem.item_id, update_count)


class ServiceTerritory(object):
    def __init__(self):
        self.GetStorageMax = {
            Define.BUILDING_TYPE_FIELD: lambda redis_data: redis_data[Define.BUILDING_TYPE_FOOD_STORAGE],
            Define.BUILDING_TYPE_MINE: lambda redis_data: redis_data[Define.BUILDING_TYPE_IRON_STORAGE],
            Define.BUILDING_TYPE_QUARRY: lambda redis_data: redis_data[Define.BUILDING_TYPE_STONE_STORAGE],
            Define.BUILDING_TYPE_LUMBER_MILL: lambda redis_data: redis_data[Define.BUILDING_TYPE_WOOD_STORAGE]
        }

    def TerritoryBuild(self, request, response):
        db_profile = self.w_db['profile'].select_column(self.userid, "cash, money")
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        redis_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO)
        if not redis_data:
            response.result = Response.USER_INVALID
            return

        redis_territory = convert_string_to_dict(redis_data)
        self.wait_build_process(redis_territory)
        
        build_info_dict = self.table.build_create[request.territory_build.build_type]
        if not build_info_dict:
            response.result = Response.INVALID_RESOURCE
            return

        update_item_dict = {}
        building_level = 1
        db_territory = None
        building_uid = 0
        db_update = []
        value_list = []
        update_cash = 0
        castle_level = redis_territory[Define.BUILDING_TYPE_CASTLE]
        if 0 < request.territory_build.building_uid:
            db_territory = self.w_db['territory'].find_building(self.userid, request.territory_build.building_uid)
            if not db_territory:
                response.result = Response.BUILDING_INVALID
                return

            if db_territory.auid != self.userid:
                response.result = Response.BUILDING_INVALID
                return

            if db_territory.building_type != Define.BUILDING_TYPE_CASTLE:
                if castle_level < (db_territory.level + 1):
                    response.result = Response.CASTLE_LEVEL_LACK
                    return

            building_level = db_territory.level + 1
        else:
            build_unlock = self.table.build_unlock[castle_level]
            if not build_unlock:
                response.result = Response.INVALID_RESOURCE
                return

            building_count = self.w_db['territory'].building_count(self.userid, request.territory_build.build_type)
            if build_unlock[request.territory_build.build_type] <= building_count:
                response.result = Response.BUILD_COUNT_LACK
                return

        build_material = build_info_dict[building_level]
        if not build_material:
            response.result = Response.INVALID_RESOURCE
            return

        consume_meney = build_material.money
        # 연구소 효과 적용
        reduce_money = ReserchAffectTerritoryBuildCost(self, consume_meney)
        consume_meney = consume_meney - reduce_money
        
        update_money = db_profile.money - consume_meney
        if 0 > update_money:
            response.result = Response.MONEY_LACK
            return

        db_update.append('money')
        value_list.append(update_money)

        useItem = response.territory_build.use_items.add()
        useItem.item_id = GAMECOMMON.ITEM_GOLD_ID
        useItem.count = consume_meney

        item_ids = list(build_material.material_list.keys())
        if 0 < len(item_ids):
            db_material = self.w_db['etcinven'].find_item_list(self.userid, item_ids)
            if not db_material:
                response.result = Response.ITEM_INVALID
                return

            if len(db_material) != len(item_ids):
                response.result = Response.ITEM_COUNT_LACK
                return

            for material in db_material:
                cosume_count = build_material.material_list[material.item_id]
                # 연구소 효과 적용
                reduce_count = ReserchAffectTerritoryBuildCost(self, cosume_count)
                cosume_count = cosume_count - reduce_count
                
                update_count = material.item_count - cosume_count
                if 0 > update_count:
                    response.result = Response.ITEM_COUNT_LACK
                    return

                useItem = response.territory_build.use_items.add()
                useItem.item_id = material.item_id
                useItem.count = cosume_count
                
                update_item_dict[material.item_id] = update_count

        if request.territory_build.cash_flag:
            consume_cash = self.quick_Completion_Cash(
                build_material.build_second,
                self.table.const_info.get(GAMECOMMON.QUICK_MAKE_BUILDING).value
            )
            # 연구소 효과 적용
            reduce_cash = ReserchAffectTerritoryBuildQuickCompleteCost(self, consume_cash)
            consume_cash = consume_cash - reduce_cash

            update_cash = db_profile.cash - consume_cash
            if 0 > update_cash:
                response.result = Response.CASH_LACK
                return

            db_update.append('cash')
            value_list.append(update_cash)

            # 건물 짓는데 걸리는 시간 ex) 20초
            consume_build_sec = build_material.build_second
            # 연구소 효과 적용 - 건물 짓는 속도. 10% 효과시 2초
            reduce_time = ReserchAffectTerritoryBuildTime(self, consume_build_sec)
            # 기존 로직과 다르게 현재 시간에서 초를 빼는 방식이므로 
            # 빨리 짓는 효과를 내려면 연구소 효과 값을 더한다. ex) 22초
            consume_build_sec = consume_build_sec + reduce_time
            update_time = self.begin - timedelta(seconds=consume_build_sec)
            
            if 0 < request.territory_build.building_uid:
                try:
                    MaxStorage = self.GetStorageMax[db_territory.building_type](redis_data)
                    resourceBuildingReward(
                        self,
                        db_territory,
                        build_info_dict,
                        db_territory.level,
                        response.territory_build.reward_item,
                        MaxStorage
                    )
                except:
                    pass

                self.w_db['territorybuild'].insert_territory_build(
                    self.userid,
                    db_territory.uid,
                    db_territory.building_type,
                    building_level,
                    update_time
                )

                self.w_db['territory'].territory_level_wait(
                    self.userid,
                    db_territory.uid,
                    0
                )

                building_uid = db_territory.uid
            else:
                building_uid = self.w_db['territory'].insert_territory(
                    self.userid,
                    request.territory_build.build_type,
                    0,
                    update_time,
                    request.territory_build.build_slot
                )

                self.w_db['territorybuild'].insert_territory_build(
                    self.userid, 
                    building_uid,
                    request.territory_build.build_type, 
                    building_level,
                    update_time
                )

            useItem = response.territory_build.use_items.add()
            useItem.item_id = GAMECOMMON.ITEM_RUBY_ID
            useItem.count = consume_cash
            self.wait_build_process(redis_territory)
        else:
            building_uid = request.territory_build.building_uid
            if 0 < request.territory_build.building_uid:
                try:
                    MaxStorage = self.GetStorageMax[db_territory.building_type](redis_data)
                    resourceBuildingReward(
                        self,
                        db_territory,
                        build_info_dict,
                        db_territory.level,
                        response.territory_build.reward_item,
                        MaxStorage
                    )
                except:
                    pass

                self.w_db['territorybuild'].insert_territory_build(
                    self.userid,
                    db_territory.uid,
                    db_territory.building_type,
                    building_level,
                    self.begin
                )
                self.w_db['territory'].territory_level_wait(self.userid, db_territory.uid, 0)
            else:
                building_uid = self.w_db['territory'].insert_territory(
                    self.userid,
                    request.territory_build.build_type,
                    0,
                    self.begin,
                    request.territory_build.build_slot
                )

                self.w_db['territorybuild'].insert_territory_build(
                    self.userid,
                    building_uid,
                    request.territory_build.build_type,
                    building_level,
                    self.begin
                )

        for key, value in update_item_dict.items():
            self.w_db['etcinven'].update_item_count(self.userid, key, value)

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list)
        
        response.territory_build.build_type = request.territory_build.build_type
        response.territory_build.building_uid = building_uid
        response.result = Response.SUCCESS
        return
    

    def TerritoryReward(self, request, response):
        redis_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO)
        if not redis_data:
            response.result = Response.USER_INVALID
            return

        redis_territory = convert_string_to_dict(redis_data)
        self.wait_build_process(redis_territory)

        db_territory = self.w_db['territory'].find_building(self.userid, request.territory_reward.building_uid)
        if not db_territory:
            response.result = Response.BUILDING_INVALID
            return

        if 1 > db_territory.level:
            response.result = Response.BUILD_PROCESSING
            return

        storage_max = self.GetStorageMax[db_territory.building_type](redis_territory)
        if not storage_max:
            self.logger.debug("territory_reward type error : type[{}]".format(db_territory.building_type))
            response.result = Response.BUILDING_INVALID
            return

        # 연구소 효과 적용
        # 저장량 1500 이면 10% 증가시 1500 + 150 = 1650
        add_max_storage = ReserchAffectTerritoryRewardStorageMax(self, storage_max)
        storage_max = storage_max + add_max_storage

        build_info_dict = self.table.build_create[db_territory.building_type]
        if not build_info_dict:
            self.logger.error("wait_build_process build create info invalid : type[{}]".format(db_territory.building_type))
            response.result = Response.BUILDING_INVALID
            return

        resourceBuildingReward(
            self,
            db_territory,
            build_info_dict,
            db_territory.level,
            response.territory_reward.reward_item,
            int(storage_max)
        )

        self.w_db['territory'].update_reward_time(self.userid, db_territory.uid, self.begin)
        response.result = Response.SUCCESS
        return

    def TerritoryBuildList(self, response):
        redis_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO)
        if not redis_data:
            response.result = Response.USER_INVALID
            return

        redis_territory = convert_string_to_dict(redis_data)
        self.wait_build_process(redis_territory)

        db_building_list = self.w_db['territory'].select_all_building(self.userid)
        for building in db_building_list:
            buildingInfo = response.territory_building_list.building_list.add()
            buildingInfo.uid = building.uid
            buildingInfo.building_type = building.building_type
            buildingInfo.level = building.level
            buildingInfo.produce_time = 0
            buildingInfo.upgrade_time = 0
            buildingInfo.build_slot = building.build_slot
            if 0 < buildingInfo.level:
                try:
                    self.GetStorageMax[building.building_type](redis_territory)
                    buildingInfo.produce_time = time_diff_in_seconds(building.start_time)
                except:
                    pass
            else:
                db_build_info = self.w_db['territorybuild'].territory_build_process(self.userid, building.uid)
                if db_build_info:
                    buildingInfo.level = db_build_info.build_level
                    buildingInfo.upgrade_time = time_diff_in_seconds(db_build_info.create_time)

        response.result = Response.SUCCESS
        return