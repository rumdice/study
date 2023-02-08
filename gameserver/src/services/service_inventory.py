# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


class ServiceInventory(object):
    def __init__(self):
         self.get_inven_proc = {
            Define.INVEN_TYPE_HERO: ServiceInventory.get_hero_inven,
            Define.INVEN_TYPE_EQUIP: ServiceInventory.get_equip_inven,
            Define.INVEN_TYPE_ETC: ServiceInventory.get_etc_inven,
        }

    def get_hero_inven(self, response):
        response.get_inventory.inven_type = Define.INVEN_TYPE_HERO
        db_inven_hero = self.w_db['heroinven'].select_all_item(self.userid)
        if not db_inven_hero:
            response.result = Response.SUCCESS
            return

        for item in db_inven_hero:
            heroData = response.get_inventory.item_list.add()
            heroData.uid = item.uid
            heroData.item_id = item.item_id
            heroData.exp = item.exp
            heroData.tier = item.tier
            heroData.dispatch_flag = item.dispatch_flag
            heroData.lock_flag = item.lock_flag
            heroData.passive_skill_id1 = item.passive_skill_id1
            heroData.passive_skill_id2 = item.passive_skill_id2

            if item.potential_stat_list != None:
                potential_list = str(item.potential_stat_list, 'utf-8').split(',')
                for info in potential_list:
                    statData = heroData.potential_stat_list.add()
                    data = str(info).split(':')
                    statData.type = int(data[0])
                    statData.value = int(data[1])

        response.result = Response.SUCCESS

    def get_equip_inven(self, response):
        response.get_inventory.inven_type = Define.INVEN_TYPE_EQUIP
        db_inven_equip = self.w_db['equipinven'].select_all_item(self.userid)
        if not db_inven_equip:
            response.result = Response.SUCCESS
            return

        for item in db_inven_equip:
            EquipData = response.get_inventory.item_list.add()
            EquipData.uid = item.uid
            EquipData.item_id = item.item_id
            EquipData.exp = item.exp
            EquipData.lock_flag = item.lock_flag
            EquipData.dispatch_flag = False
            if item.inven_type == GAMECOMMON.EQUIP_INVEN_TYPE_NORMAL:
                EquipData.dispatch_flag = True
            
        response.result = Response.SUCCESS

    def get_etc_inven(self, response):
        response.get_inventory.inven_type = Define.INVEN_TYPE_ETC
        db_inven_etc = self.w_db['etcinven'].select_all_item(self.userid)
        if not db_inven_etc:
            response.result = Response.SUCCESS
            return

        for item in db_inven_etc:
            itemData = response.get_inventory.item_list.add()
            itemData.item_id = item.item_id
            itemData.count = item.item_count

        response.result = Response.SUCCESS


    def GetInventory(self, request, response):
        if request.get_inventory.inven_type not in self.get_inven_proc:
            response.result = Response.FIELD_MISSING
            return

        self.get_inven_proc[request.get_inventory.inven_type](self, response)
        return

    def ExtendInven(self, request, response):
        db_profile = self.w_db['profile'].select_column(
            self.userid,
            "equip_normal_inven_max, equip_pvp_inven_max, hero_inven_max, cash"
        )
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        extend_hero_max = int(self.table.const_info.get(GAMECOMMON.EXTEND_HERO_MAX).value)
        extend_equip_normal_max = int(self.table.const_info.get(GAMECOMMON.EXTEND_EQUIP_NORMAL_MAX).value)
        extend_equip_pvp_max = int(self.table.const_info.get(GAMECOMMON.EXTEND_EQUIP_PVP_MAX).value)
        
        extend_hero_inven_cash = int(self.table.const_info.get(GAMECOMMON.EXTEND_HERO_INVEN_CASH).value)
        extend_hero_inven_count = int(self.table.const_info.get(GAMECOMMON.EXTEND_HERO_INVEN_COUNT).value)
        
        extend_equip_normal_cash = int(self.table.const_info.get(GAMECOMMON.EXTEND_EQUIP_NORMAL_CASH).value)
        extend_equip_normal_count = int(self.table.const_info.get(GAMECOMMON.EXTEND_EQUIP_NORMAL_COUNT).value)
        
        extend_equip_pvp_cash = int(self.table.const_info.get(GAMECOMMON.EXTEND_EQUIP_PVP_CASH).value)
        extend_equip_pvp_count = int(self.table.const_info.get(GAMECOMMON.EXTEND_EQUIP_PVP_COUNT).value)
        

        response.extend_inven.inven_type = request.extend_inven.inven_type
        if response.extend_inven.inven_type == Define.INVEN_TYPE_HERO:
            buy_count = request.extend_inven.buy_count
            update_max_inven = db_profile.hero_inven_max + (buy_count * extend_hero_inven_count)
            if update_max_inven > extend_hero_max:
                response.result = Response.CAN_NOT_EXTEND_INVEN
                return

            buy_cash = buy_count * extend_hero_inven_cash
            update_cash = db_profile.cash - buy_cash
            if update_cash < 0:
                response.result = Response.CASH_LACK
                return

            self.w_db['profile'].extend_hero_inven(self.userid, update_max_inven, update_cash)

            response.extend_inven.use_cash = buy_cash
            response.extend_inven.max_inven_size = update_max_inven

        elif response.extend_inven.inven_type == Define.INVEN_TYPE_EQUIP:
            update_max_inven = db_profile.equip_normal_inven_max + extend_equip_normal_count
            if update_max_inven > extend_equip_normal_max:
                response.result = Response.CAN_NOT_EXTEND_INVEN
                return

            update_cash = db_profile.cash - extend_equip_normal_cash
            if 0 > update_cash:
                response.result = Response.CASH_LACK
                return

            self.w_db['profile'].extend_equip_normal_inven(self.userid, update_max_inven, update_cash)

            response.extend_inven.use_cash = extend_equip_normal_cash
            response.extend_inven.max_inven_size = update_max_inven


        elif response.extend_inven.inven_type == Define.INVEN_TYPE_EQUIP_PVP:
            update_max_inven = db_profile.equip_pvp_inven_max + extend_equip_pvp_count
            if update_max_inven > extend_equip_pvp_max:
                response.result = Response.CAN_NOT_EXTEND_INVEN
                return

            update_cash = db_profile.cash - extend_equip_pvp_cash
            if 0 > update_cash:
                response.result = Response.CASH_LACK
                return

            self.w_db['profile'].extend_equip_pvp_inven(self.userid, update_max_inven, update_cash)

            response.extend_inven.use_cash = extend_equip_pvp_cash
            response.extend_inven.max_inven_size = update_max_inven

        response.result = Response.SUCCESS
        return