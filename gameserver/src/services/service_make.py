# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *
from src.services.service_research import *


#제작 (아이템)
class ServiceMake(object):
    def MakeItem(self, request, response):
        redis_info = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO)
        if not redis_info:
            response.result = Response.USER_INVALID
            return

        redis_territory = convert_string_to_dict(redis_info)
        self.wait_build_process(redis_territory)

        db_building = self.w_db['territory'].find_building(self.userid, request.make_item.building_uid)
        if not db_building:
            response.result = Response.BUILDING_INVALID
            return

        if db_building.building_type != Define.BUILDING_TYPE_WORKSHOP:
            response.result = Response.BUILDING_INVALID
            return

        db_makeItem = self.w_db['makeitem'].find_make_item(self.userid, request.make_item.building_uid)
        db_function = self.w_db['makeitem'].update_make_item
        if not db_makeItem:
            db_function = self.w_db['makeitem'].add_make_item
        else:
            feild_make_item = "make_itemid" + str(request.make_item.slot)
            if 0 < db_makeItem[feild_make_item]:
                response.result = Response.CAN_NOT_MAKE_ITEM
                return

        makeItemData = self.table.recipe.get(request.make_item.make_itemid, None)
        if not makeItemData:
            response.result = Response.INVALID_RESOURCE
            return

        if db_building.level < makeItemData.check_lv:
            response.result = Response.LEVEL_LACK
            return

        db_profile = self.w_db['profile'].select_column(self.userid, "money, cash")
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        consume_money = makeItemData.use_money
         # 연구소 효과 적용
        reduce_money = ReserchAffectMakeItemCost(self, consume_money)
        consume_money = consume_money - reduce_money
        
        update_money = db_profile.money - consume_money
        if 0 > update_money:
            response.result = Response.MONEY_LACK
            return

        useItem = response.make_item.use_items.add()
        useItem.item_id = GAMECOMMON.ITEM_GOLD_ID
        useItem.count = consume_money

        db_update = []
        db_update.append('money')
        
        value_list = []
        value_list.append(update_money)
        
        update_item_dict = {}
        update_item_dict[GAMECOMMON.ITEM_GOLD_ID] = update_money

        material_ids = list(makeItemData.material_list.keys())
        db_material = self.w_db['etcinven'].find_item_list(self.userid, material_ids)
        if not db_material:
            response.result = Response.ITEM_INVALID
            return

        if len(db_material) != len(material_ids):
            response.result = Response.ITEM_COUNT_LACK
            return

        direct_inven = True
        wait_second = 1
        build_info = self.table.build_create[Define.BUILDING_TYPE_WORKSHOP][db_building.level]
        if 0 < makeItemData.wait_sec:
            direct_inven = False
            wait_second = (int)(makeItemData.wait_sec * ((100 - build_info.produce) * 0.01))
            # 연구소 효과 적용
            reduce_time = ReserchAffectMakeItemTime(self, wait_second)
            wait_second = wait_second - reduce_time

        for material in db_material:
            update_count = material.item_count - makeItemData.material_list[material.item_id]
            if 0 > update_count:
                response.result = Response.ITEM_COUNT_LACK
                return

            useItem = response.make_item.use_items.add()
            useItem.item_id = material.item_id
            useItem.count = makeItemData.material_list[material.item_id]
            update_item_dict[material.item_id] = update_count


        response.make_item.make_item_info.slot = request.make_item.slot
        response.make_item.make_item_info.make_itemid = request.make_item.make_itemid

        if direct_inven:
            response.make_item.reward_item.count = 1
            response.make_item.reward_item.item_id = request.make_item.make_itemid
            response.make_item.make_item_info.remain_time = 0
        else:
            
            end_time = self.begin + timedelta(seconds=wait_second)
            
            if request.make_item.cash_flag:
                use_cash = self.quick_Completion_Cash(wait_second, self.table.const_info.get(GAMECOMMON.QUICK_MAKE_ITEM).value)
                update_cash = db_profile.cash - use_cash
                if 0 > update_cash:
                    response.result = Response.CASH_LACK
                    return

                db_update.append('cash')
                value_list.append(update_cash)

                update_item_dict[GAMECOMMON.ITEM_RUBY_ID] = update_money

                end_time = self.begin

                useItem = response.make_item.use_items.add()
                useItem.item_id = GAMECOMMON.ITEM_RUBY_ID
                useItem.count = use_cash

                wait_second = 0

            db_function(
                self.userid, 
                request.make_item.building_uid, 
                request.make_item.slot,
                request.make_item.make_itemid, 
                end_time
            )


        self.w_db['profile'].update_user_column(self.userid, db_update, value_list)

        for key, value in update_item_dict.items():
            if key == GAMECOMMON.ITEM_GOLD_ID:
                pass
            elif key == GAMECOMMON.ITEM_RUBY_ID:
                pass
            else:
                self.w_db['etcinven'].update_item_count(self.userid, key, value)

        if direct_inven:
            self.w_db['etcinven'].add_item(self.userid, request.make_item.make_itemid, 1)

        response.make_item.make_item_info.remain_time = wait_second
        response.result = Response.SUCCESS
        return
    
    def MakeItemReward(self, request, response):
        building_uid = request.make_item_reward.building_uid
        db_makeItem = self.w_db['makeitem'].find_make_item(self.userid, building_uid)
        if not db_makeItem:
            response.result = Response.REWARD_ITEM_NONE
            return
        slot = request.make_item_reward.slot
        if 0 <= slot:
            make_itemid = db_makeItem["make_itemid" + str(slot)]
            end_time = db_makeItem["end_time" + str(slot)]
            if 0 == make_itemid:
                response.result = Response.INVALID_RESOURCE
                return

            if end_time > self.begin:
                response.result = Response.TIME_ERROR
                return

            itemData = self.table.item.get(make_itemid, None)
            if not itemData:
                response.result = Response.INVALID_RESOURCE
                return

            if itemData.item_type == Define.ITEM_TYPE_EQUIP:
                add_uid = self.w_db['equipinven'].insert_equip(self.userid, make_itemid, itemData.pvp)
                reward_item = response.make_item_reward.reward_items.add()
                reward_item.uid = add_uid
                reward_item.item_id = itemData.id
                reward_item.item_type = itemData.item_type
                reward_item.count = 1
                reward_item.dispatch_flag = (itemData.pvp == GAMECOMMON.EQUIP_INVEN_TYPE_NORMAL)
                response.make_item_reward.reward_slots.append(slot)
            else:
                etc_item = self.w_db['etcinven'].find_item(self.userid, itemData.item_id)
                if not etc_item:
                    self.w_db['etcinven'].add_item(self.userid, itemData.item_id, 1)
                else:
                    etc_count = etc_item.item_count + 1
                    self.w_db['etcinven'].update_item_count(self.userid, itemData.item_id, etc_count)
                reward_item = response.make_item_reward.reward_items.add()
                reward_item.count = 1
                reward_item.item_id = itemData.item_id
                reward_item.item_type = itemData.item_type

            self.w_db['makeitem'].update_make_item(self.userid, request.make_item_reward.building_uid, slot, 0, self.begin)

        else:
            for index in range(6):
                make_itemid = db_makeItem["make_itemid" + str(index)]
                if 0 == make_itemid:
                    continue

                itemData = self.table.item.get(make_itemid, None)
                if not itemData:
                    response.result = Response.INVALID_RESOURCE
                    return

            for index in range(6):
                make_itemid = db_makeItem["make_itemid" + str(index)]
                end_time = db_makeItem["end_time" + str(index)]
                if 0 == make_itemid:
                    continue
                if end_time > self.begin:
                    continue

                itemData = self.table.item.get(make_itemid, None)
                if itemData.item_type == Define.ITEM_TYPE_EQUIP:
                    add_uid = self.w_db['equipinven'].insert_equip(self.userid, make_itemid, itemData.pvp)
                    reward_item = response.make_item_reward.reward_items.add()
                    reward_item.uid = add_uid
                    reward_item.item_id = itemData.id
                    reward_item.item_type = itemData.item_type
                    reward_item.count = 1
                    reward_item.dispatch_flag = (itemData.pvp == GAMECOMMON.EQUIP_INVEN_TYPE_NORMAL)
                else:
                    etc_item = self.w_db['etcinven'].find_item(self.userid, itemData.item_id)
                    if not etc_item:
                        self.w_db['etcinven'].add_item(self.userid, itemData.item_id, 1)
                    else:
                        etc_count = etc_item.item_count + 1
                        self.w_db['etcinven'].update_item_count(self.userid, itemData.item_id, etc_count)

                    reward_item = response.make_item_reward.reward_items.add()
                    reward_item.count = 1
                    reward_item.item_id = itemData.item_id
                    reward_item.item_type = itemData.item_type
                response.make_item_reward.reward_slots.append(index)
                self.w_db['makeitem'].update_make_item(self.userid, request.make_item_reward.building_uid, index, 0, self.begin)
        response.result = Response.SUCCESS
        return

    def MakeItemCancel(self, request, response):
        slot = request.make_item_cancel.slot
        self.w_db['makeitem'].update_make_item(self.userid, request.make_item_cancel.building_uid, slot, 0, self.begin)
        response.result = Response.SUCCESS
        return

    def MakeItemList(self, request, response):
        db_makeItem = self.w_db['makeitem'].make_item_all(self.userid)
        if not db_makeItem:
            response.work_shop_info_list.CopyFrom(Response.WorkShopInfoList())
            response.result = Response.SUCCESS
            return
        for makeItem in db_makeItem:
            shopInfo = response.work_shop_info_list.work_shop_info.add()
            shopInfo.uid = makeItem.building_uid
            for slot in range(6):
                make_item = makeItem["make_itemid" + str(slot)]
                if 0 < make_item:
                    makeItemInfo = shopInfo.make_item_infos.add()
                    makeItemInfo.slot = slot
                    makeItemInfo.make_itemid = makeItem["make_itemid" + str(slot)]
                    remainTime = makeItem["end_time" + str(slot)]
                    remainTime = calc_time_to_seconds(self.begin, remainTime)
                    if 0 > remainTime:
                        remainTime = 0
                    makeItemInfo.remain_time = remainTime
        response.result = Response.SUCCESS
        return

    def MakeQuickComplet(self, request, response):
        use_cash = 0
        slot = request.make_quick_complet.slot
        if request.make_quick_complet.makeFlag:
            if request.make_quick_complet.build_type != Define.BUILDING_TYPE_WORKSHOP:
                response.result = Response.FIELD_MISSING
                return

            db_makeItem = self.w_db['makeitem'].find_make_item(self.userid, request.make_quick_complet.building_uid)
            if not db_makeItem:
                response.result = Response.ITEM_INVALID
                return

            make_itemid = db_makeItem["make_itemid" + str(slot)]
            if 0 == make_itemid:
                response.result = Response.ITEM_INVALID
                return

            end_time = db_makeItem["end_time" + str(slot)]
            if end_time <= self.begin:
                response.result = Response.TIME_ERROR
                return

            db_info = self.w_db['profile'].select_column(self.userid, "cash")
            if not db_info:
                response.result = Response.USER_INVALID
                return

            remain_time = time_diff_in_seconds(end_time)
            use_cash = self.quick_Completion_Cash(remain_time, self.table.const_info.get(GAMECOMMON.QUICK_MAKE_ITEM).value)
            update_cash = db_info.cash - use_cash
            if 0 > update_cash:
                response.result = Response.CASH_LACK
                return

            self.w_db['makeitem'].update_make_item(
                self.userid,
                request.make_quick_complet.building_uid,
                slot,
                make_itemid,
                self.begin
            )

            self.w_db['profile'].update_cash(self.userid, update_cash)

        else:
            db_waitBuild = self.w_db['territorybuild'].find_territory_build(
                self.userid,
                request.make_quick_complet.building_uid
            )

            if not db_waitBuild:
                response.result = Response.BUILDING_INVALID
                return

            build_info_dict = self.table.build_create[request.make_quick_complet.build_type]
            if not build_info_dict:
                response.result = Response.INVALID_RESOURCE
                return

            build_material = build_info_dict[db_waitBuild.build_level]
            if not build_material:
                response.result = Response.INVALID_RESOURCE
                return

            remain_time = time_diff_in_seconds(db_waitBuild.create_time)
            if build_material.build_second < remain_time:
                response.result = Response.TIME_ERROR
                return

            db_info = self.w_db['profile'].select_column(self.userid, "cash")
            if not db_info:
                response.result = Response.USER_INVALID
                return

            remain_time = build_material.build_second - remain_time
            use_cash = self.quick_Completion_Cash(remain_time, self.table.const_info.get(GAMECOMMON.QUICK_MAKE_BUILDING).value)
            # 연구소 효과 적용
            reduce_cost = ReserchAffectMakeQuickItemCost(self, use_cash)
            use_cash = use_cash - reduce_cost
            
            update_cash = db_info.cash - use_cash
            if 0 > update_cash:
                response.result = Response.CASH_LACK
                return

            update_time = db_waitBuild.create_time - timedelta(seconds=build_material.build_second)
            self.w_db['territorybuild'].territory_build_create_time(self.userid, db_waitBuild.uid, update_time)
            self.w_db['profile'].update_cash(self.userid, update_cash)

            redis_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO)
            if not redis_data:
                response.result = Response.USER_INVALID
                return

            redis_territory = convert_string_to_dict(redis_data)
            self.wait_build_process(redis_territory)

        response.make_quick_complet.build_type = request.make_quick_complet.build_type
        response.make_quick_complet.building_uid = request.make_quick_complet.building_uid
        response.make_quick_complet.makeFlag = request.make_quick_complet.makeFlag
        response.make_quick_complet.use_cash = use_cash
        response.make_quick_complet.slot = slot
        response.result = Response.SUCCESS
        return