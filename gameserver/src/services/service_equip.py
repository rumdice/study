# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


class ServiceEquip(object):

    def _getEnchantLevel(self, grade, totalExp):
        calc_value = totalExp / self.table.const_info.get(GAMECOMMON.ENCHANT_EXP_CONST).value / pow(2, grade-1)
        return int(pow(calc_value, 0.5))

    def _equipMaterialExp(self, grade, totalExp):
        calc_value = totalExp / pow(2, (grade-1)) / self.table.const_info.get(GAMECOMMON.ENCHANT_EXP_CONST).value
        equip_level =  int(pow(calc_value, 0.5))

        return int(
            pow((grade - 1), 3) * 
            self.table.const_info.get(GAMECOMMON.ENCHANT_MATERIAL_A).value + 
            pow(equip_level, 2) * 
            pow(2, (grade - 1)) * 
            self.table.const_info.get(GAMECOMMON.ENCHANT_MATERIAL_B).value
        )




    def EquipLock(self, request, response):
        db_info = self.w_db['equipinven'].find_item(self.userid, request.equip_lock.uid)
        if not db_info:
            response.result = Response.ITEM_INVALID
            return

        if db_info.auid != self.userid:
            response.result = Response.ITEM_INVALID
            return

        self.w_db['equipinven'].update_lock(self.userid, request.equip_lock.uid, request.equip_lock.lock_flag)

        response.equip_lock.uid = db_info.uid
        response.equip_lock.lock_flag = request.equip_lock.lock_flag
        response.result = Response.SUCCESS
        return

    def EquipExp(self, request, response):
        if request.equip_exp.target_equip_uid in request.equip_exp.material_list:
            response.result = Response.ITEM_INVALID
            return

        db_info = self.w_db['equipinven'].find_item(self.userid, request.equip_exp.target_equip_uid)
        if not db_info:
            response.result = Response.ITEM_INVALID
            return

        if db_info.auid != self.userid:
            response.result = Response.ITEM_INVALID
            return

        material_list = self.w_db['equipinven'].find_item_list(self.userid, request.equip_exp.material_list)
        if len(material_list) != len(request.equip_exp.material_list):
            response.result = Response.ITEM_INVALID
            return

        total_exp = db_info.exp
        for material in material_list:
            if material.auid != self.userid:
                response.result = Response.ITEM_INVALID
                return

            item_data = self.table.item.get(material.item_id, None)
            if not item_data:
                response.result = Response.INVALID_RESOURCE
                return

            total_exp += ServiceEquip._equipMaterialExp(self, item_data.grade, material.exp)

        self.w_db['equipinven'].update_exp(self.userid, request.equip_exp.target_equip_uid, total_exp)
        self.w_db['equipinven'].del_item_list(self.userid, request.equip_exp.material_list)

        response.equip_exp.resultEquip.uid = db_info.uid
        response.equip_exp.resultEquip.exp = db_info.exp
        if db_info.inven_type == GAMECOMMON.EQUIP_INVEN_TYPE_NORMAL:
            response.equip_exp.resultEquip.dispatch_flag = True
        else:
            response.equip_exp.resultEquip.dispatch_flag = False

        response.equip_exp.material_list.extend(request.equip_exp.material_list)
        response.result = Response.SUCCESS
        return

    def EquipEnchant(self, request, response):
        db_info = self.w_db['profile'].select_column(self.userid, "money")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        db_equip = self.w_db['equipinven'].find_item(self.userid, request.equip_enchant.target_uid)
        if not db_equip:
            response.result = Response.ITEM_INVALID
            return

        db_materials = self.w_db['equipinven'].find_item_list(self.userid, request.equip_enchant.material_list)
        if not db_materials:
            response.result = Response.ITEM_INVALID
            return

        if len(db_materials) != len(request.equip_enchant.material_list):
            response.result = Response.ITEM_INVALID
            return

        add_exp = 0
        use_gold = 0
        for db_item in db_materials:
            item_data = self.table.item.get(db_item.item_id, None)
            if not item_data:
                response.result = Response.ITEM_INVALID
                return

            if db_item.inven_type != db_equip.inven_type:
                response.result = Response.ITEM_INVALID
                return

            get_level = ServiceEquip._getEnchantLevel(self, item_data.grade, db_item.exp)
            add_exp += int(
                pow((item_data.grade + 1), 3) * 100 + 
                pow(get_level, 2) * 
                pow(2, item_data.grade - 1) * 
                self.table.const_info.get(GAMECOMMON.ENCHANT_MATERIAL_B).value
            )


        db_item_data = self.table.item.get(db_equip.item_id, None)
        current_level = ServiceEquip._getEnchantLevel(self, db_item_data.grade, db_equip.exp)
        if current_level >= 10:
            response.result = Response.INVALID_RESOURCE
            return 

        after_level = ServiceEquip._getEnchantLevel(self, db_item_data.grade, db_equip.exp + add_exp)
        if after_level >= 10:
            after_level = 10

        use_gold += int(add_exp * self.table.const_info.get(GAMECOMMON.ENCHANT_GOLD).value)
        update_money = db_info.money - use_gold
        if 0 > update_money:
            response.result = Response.MONEY_LACK
            return

        self.w_db['profile'].update_money(self.userid, update_money)
        self.w_db['equipinven'].del_item_list(self.userid, request.equip_enchant.material_list)
        self.w_db['equipinven'].update_exp(self.userid, db_equip.uid, add_exp + db_equip.exp)

        response.equip_enchant.target_uid = request.equip_enchant.target_uid
        response.equip_enchant.material_list.extend(request.equip_enchant.material_list)
        response.equip_enchant.use_gold = use_gold
        response.equip_enchant.total_exp = add_exp + db_equip.exp

        response.result = Response.SUCCESS
        return