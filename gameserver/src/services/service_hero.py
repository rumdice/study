# -*- coding: utf-8 -*-
from math import ceil

from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


class ServiceHero(object):
    def __init__(self, context):
        self.TIER_MAX_LEVEL = {
            1: int(context.table.const_info.get(GAMECOMMON.TIER_1_MAX).value),
            2: int(context.table.const_info.get(GAMECOMMON.TIER_2_MAX).value),
            3: int(context.table.const_info.get(GAMECOMMON.TIER_3_MAX).value),
            4: int(context.table.const_info.get(GAMECOMMON.TIER_4_MAX).value),
            5: int(context.table.const_info.get(GAMECOMMON.TIER_5_MAX).value)
        }

    def _getLevel(self, grade, exp):
        calc_value = (exp / self.table.const_exp[grade] / self.table.const_info.get(GAMECOMMON.EXP_CONST).value)
        return int(pow(calc_value, 0.5) + 1)

    def _find_table_passive_skill(_jclass, _table):
        return [e for e in _table if e['jclass'] == _jclass]

    def _find_table_potential_info(_kind, _grade, _table):
        return [e for e in _table if e['kind'] == _kind and e['grade'] == _grade]

    def _find_table_potential_unlock(_slot_idx, _table):
        return [e for e in _table if e['slot'] == _slot_idx]

    def _getMaxExp(self, max_lv, grade):
        max_exp = pow(max_lv - 1, 2) * self.table.const_exp[grade] * self.table.const_info.get(GAMECOMMON.EXP_CONST).value
        return int(max_exp)

    def _gacha_stat(self, kind, grade):
        # slot_kind, grade로 하나의 row를 구함
        row = ServiceHero._find_table_potential_info(
            kind,
            grade,
            self.table.potential_info
        )

        # 4가지 스텟 중 1개를 뽑음.
        products = {
            'atk': row[0].prob_atk,
            'df': row[0].prob_df,
            'hp': row[0].prob_hp,
            'mg': row[0].prob_mg,
        }

        productrange = []
        productresult = []

        for product in products:
            if not productrange:
                productresult.append(product)
                productrange.append(products[product])
            else:
                productresult.append(product)
                productrange.append(productrange[-1] + products[product])

        count = 10000
        for j in range(0, count):
            tempresult = random.randrange(1,productrange[-1]+1)

        tempcnt = 0
        result = ''
        for i in productrange:
            if tempresult <= i:
                result = productresult[tempcnt]
                break
            else:
                tempcnt=tempcnt+1

        # 뽑은 하나의 속성에서 최대 최소값을 구하고 그 사이 렌덤값을 구함.
        min_str = result+"_min"
        max_str = result+"_max"
        min_val = row[0][min_str]
        max_val = row[0][max_str]

        stat_dict = {
            "atk": Define.POTENTIAL_STAT_ATK,
            "df": Define.POTENTIAL_STAT_DF,
            "hp": Define.POTENTIAL_STAT_HP,
            "mg": Define.POTENTIAL_STAT_MG,
        }

        stat_type = stat_dict[result]
        stat_value = random.randint(min_val, max_val)
        return (stat_type, stat_value)

    def _cousume_stone(self, slot_idx, element, is_exchange):
        error_code = None

        # 1: 불 2: 물 3: 풀 4: 빛 5: 어둠 
        # 속성석 ID - 60000091 ~ 60000095
        # 속성 id 값에 해당하는 속성석이 뭔지 테이블 내부 룰로 찾아야 함. 테이블 구조로 연결되어 있지는 않음.
        attribute_item_id = int("6000009" + str(element))
     
        row_unlock = ServiceHero._find_table_potential_unlock(
            slot_idx + 1,
            self.table.potential_unlock
        )

        if row_unlock == None:
            error_code = Response.INVALID_GAMEDATA
            return error_code

        attribute_consume_cnt = row_unlock[0].price_open
        if (is_exchange == True):
            attribute_consume_cnt = row_unlock[0].price_change

        
        # 가지고 있는지 체크
        etc_item = self.w_db['etcinven'].find_item(self.userid, attribute_item_id)
        if not etc_item:
            error_code = Response.ITEM_COUNT_LACK
            return error_code

        if etc_item.item_count < attribute_consume_cnt:
            error_code = Response.ITEM_COUNT_LACK
            return error_code

        # 재화를 소모한다
        update_item_cnt = etc_item.item_count - attribute_consume_cnt
        self.w_db['etcinven'].update_item_count(self.userid, attribute_item_id, update_item_cnt)
        return error_code

    def _affect_hero(self, _db_hero, slot_idx, target_uid, _str):
        # 영웅에 적용 시킴 - (어떤 슬롯에 어떤 스텟의 어느 벨류)
        # 기존에 가지고 있는 값을 가져와서 위치 시킬 인덱스를 고려하여 stat_dict를 만듬
        # 없으면 추가. 있으면 교체
        potential_list = ""
        if (_db_hero.potential_stat_list == None):
            potential_list = _str
        else:
            potential_str = _db_hero.potential_stat_list.decode('utf-8')
            potential_list = potential_str.split(',')
            if (len(potential_list) == slot_idx): # 새로 추가되는 경우
                potential_list.append(_str)
            else:
                potential_list[slot_idx] = _str
            _str = ','.join(potential_list)

        # 영웅에 장착(적용한다)
        self.w_db['heroinven'].update_hero_potential(self.userid, target_uid, _str)
        return

    def HeroExp(self, request, response):
        db_profile = self.w_db['profile'].select_column(self.userid, "money")
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        db_hero = self.w_db['heroinven'].find_item(self.userid, request.hero_exp.target_hero_uid)
        if not db_hero:
            response.result = Response.ITEM_INVALID
            return

        hero_data = self.table.hero.get(db_hero.item_id)
        if not hero_data:
            response.result = Response.INVALID_RESOURCE
            return

        tier_max_lv = self.TIER_MAX_LEVEL.get(db_hero.tier, None)
        if not tier_max_lv:
            response.result = Response.INVALID_RESOURCE
            return

        db_use_item = self.w_db['etcinven'].find_item(self.userid, GAMECOMMON.ITEM_HERO_EXP)
        if not db_use_item:
            response.result = Response.ITEM_INVALID
            return

        item_data = self.table.item.get(GAMECOMMON.ITEM_HERO_EXP)
        if not item_data:
            response.result = Response.ITEM_INVALID
            return

        update_count = db_use_item.item_count - request.hero_exp.item_count
        if 0 > update_count:
            response.result = Response.ITEM_COUNT_LACK
            return

        use_gold = self.table.const_info.get(GAMECOMMON.LEVELUP_GOLD).value * request.hero_exp.item_count
        update_money = int(db_profile.money - use_gold)
        if 0 > update_money:
            response.result = Response.MONEY_LACK
            return

        response.hero_exp.use_item_count = request.hero_exp.item_count
        response.hero_exp.money = int(use_gold)

        total_exp = request.hero_exp.item_count
        total_exp = db_hero.exp + total_exp

        tier_max_exp = ServiceHero._getMaxExp(self, tier_max_lv, hero_data.grade)
        if tier_max_exp < total_exp:
            total_exp = tier_max_exp

        self.w_db['heroinven'].update_exp(self.userid, db_hero.uid, total_exp)
        self.w_db['etcinven'].update_item_count(self.userid, GAMECOMMON.ITEM_HERO_EXP, update_count)
        self.w_db['profile'].update_money(self.userid, update_money)

        response.hero_exp.result_hero.uid = db_hero.uid
        response.hero_exp.result_hero.item_id = db_hero.item_id
        response.hero_exp.result_hero.exp = total_exp

        response.result = Response.SUCCESS
        return


    def HeroPromotion(self, request, response):
        db_profile = self.w_db['profile'].select_column(self.userid, "money")
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        db_hero = self.w_db['heroinven'].find_item(self.userid, request.hero_promotion.target_uid)
        if not db_hero:
            response.result = Response.ITEM_INVALID
            return

        tier_level_max = self.TIER_MAX_LEVEL.get(db_hero.tier, None)
        if not tier_level_max:
            response.result = Response.INVALID_RESOURCE
            return

        hero_data = self.table.hero.get(db_hero.item_id, None)
        if not hero_data:
            response.result = Response.INVALID_RESOURCE
            return

        use_gold = int(pow(db_hero.tier, 2) * pow(2, hero_data.grade) * self.table.const_info.get(GAMECOMMON.PROMOTION_GOLD).value)
        update_money = db_profile.money - use_gold
        if 0 > update_money:
            response.result = Response.MONEY_LACK
            return

        hero_level = ServiceHero._getLevel(self, hero_data.grade, db_hero.exp)
        if tier_level_max != hero_level:
            response.result = Response.LEVEL_LACK
            return

        promotion_data = self.table.promotion.get(hero_data.promotion_group, None)
        if not promotion_data:
            response.result = Response.INVALID_RESOURCE
            return

        material_data = promotion_data.get(db_hero.tier + 1, None)
        if not material_data:
            response.result = Response.INVALID_RESOURCE
            return

        db_material_info = self.w_db['etcinven'].find_item_list(self.userid, material_data.material_list)
        if not db_material_info:
            response.result = Response.ITEM_INVALID
            return

        if len(db_material_info) != len(material_data.material_list):
            response.result = Response.ITEM_INVALID
            return

        response.hero_promotion.target_uid = db_hero.uid
        response.hero_promotion.tier = db_hero.tier + 1
        response.hero_promotion.money = update_money

        update_item_dict = {}
        for item in db_material_info:
            update_count = item.item_count - material_data.material_data[item.item_id]
            if 0 > update_count:
                response.result = Response.LEVEL_LACK
                return

            packet_item = response.hero_promotion.material_list.add()
            packet_item.item_id = item.item_id
            packet_item.count = update_count
            update_item_dict[item.item_id] = update_count

        if 0 < len(update_item_dict):
            for key, value in update_item_dict.items():
                self.w_db['etcinven'].update_item_count(self.userid, key, value)

        self.w_db['heroinven'].hero_promotion(self.userid, db_hero.uid, db_hero.tier + 1)
        self.w_db['profile'].update_money(self.userid, update_money)

        response.result = Response.SUCCESS
        return

    def HeroLock(self, request, response):
        db_info = self.w_db['heroinven'].find_item(self.userid, request.hero_lock.uid)
        if not db_info:
            response.result = Response.ITEM_INVALID
            return

        if db_info.auid != self.userid:
            response.result = Response.ITEM_INVALID
            return

        self.w_db['heroinven'].update_lock(self.userid, request.hero_lock.uid, request.hero_lock.lock_flag)

        response.hero_lock.uid = db_info.uid
        response.hero_lock.lock_flag = request.hero_lock.lock_flag
        response.result = Response.SUCCESS
        return


    def HeroReturn(self, request, response):
        response.hero_return.hero_uids.extend(request.hero_return.hero_uids)
        db_hero = self.w_db['heroinven'].find_item_list(self.userid, request.hero_return.hero_uids)
        if not db_hero:
            response.hero_return.add_return_point = 0
            response.result = Response.SUCCESS
            return

        total_point = 0
        for hero in db_hero:
            hero_data = self.table.hero[hero.item_id]
            total_point += self.table.return_point[hero_data.grade]

        self.w_db['heroinven'].del_item_list(self.userid, request.hero_return.hero_uids)
        etc_item = self.w_db['etcinven'].find_item(self.userid, GAMECOMMON.ITEM_RETURN_POINT)
        if not etc_item:
            self.w_db['etcinven'].add_item(self.userid, GAMECOMMON.ITEM_RETURN_POINT, total_point)
        else:
            etc_count = etc_item.item_count + total_point
            self.w_db['etcinven'].update_item_count(self.userid, GAMECOMMON.ITEM_RETURN_POINT, etc_count)

        response.hero_return.add_return_point = total_point
        response.result = Response.SUCCESS
        return

    def GetHeroPassiveSkill(self, request, response):
        use_hero_uid = request.get_hero_passive_skill.use_hero_uid
        target_hero_uid = request.get_hero_passive_skill.target_hero_uid

        # 적용 영웅이 인벤에 있는지 체크
        target_hero = self.w_db['heroinven'].find_item(self.userid, target_hero_uid)
        if not target_hero:
            response.result = Response.ITEM_INVALID
            return

        # 재료 영웅이 인벤에 있는지 체크
        use_hero = self.w_db['heroinven'].find_item(self.userid, use_hero_uid)
        if not use_hero:
            response.result = Response.ITEM_INVALID
            return

        # 재료 영웅을 날린다
        self.w_db['heroinven'].del_item(self.userid, use_hero_uid)

        # 적용 영웅의 클래스와 등급을 알아온다. 
        # hero.csv 테이블에 정해진 태생등급 
        # ex) 10114000 의 경우 grade : 1 jclass : 1
        hero_data = self.table.hero.get(target_hero.item_id)
        if not hero_data:
            response.result = Response.INVALID_GAMEDATA
            return

        # 클래스와 등급을 토대로 passive_skill.csv/reward_group.csv 를 통하여 reward_group_id를 얻음. 
        # ex) 30010511
        row = ServiceHero._find_table_passive_skill(
            hero_data.jclass,
            self.table.passive_skill
        )
        gradeStr = 'grade' + str(hero_data.grade)
        reward_group_id = row[0][gradeStr]

        group_reward = self.table.reward_group.get(reward_group_id, None)

        # 30010511 그룹의 6개 중에서 본인이 장착한 것 제외.(0개 최대 2개)
        item_id_list = []
        for v in group_reward:
            if (v.item_id == target_hero.passive_skill_id1) or (v.item_id == target_hero.passive_skill_id2):
                continue
            item_id_list.append(v.item_id) 

        # 대상에서 렌덤으로 뽑음
        _random = random.Random()
        _seed = random.randint(1, 100000000)
        _random.seed(_seed)
        new_passive_skill_id = _random.choice(item_id_list)

        response.get_hero_passive_skill.passive_skill_id = new_passive_skill_id
        response.result = Response.SUCCESS
        return

    def ConfirmHeroPassiveSkill(self, request, response):
        target_hero_uid = request.confirm_hero_passive_skill.target_hero_uid
        passive_skill_id = request.confirm_hero_passive_skill.passive_skill_id
        slot = request.confirm_hero_passive_skill.slot
        
        # 적용 영웅이 인벤에 있는지 체크
        db_hero = self.w_db['heroinven'].find_item(self.userid, target_hero_uid)
        if not db_hero:
            response.result = Response.ITEM_INVALID
            return

        # 적용 영웅에 패시브 id를 장착 시킨다. (해당 슬롯에 장착)
        if slot == 1 :
            self.w_db['heroinven'].update_hero_passive_skill_id1(self.userid, target_hero_uid, passive_skill_id)
        else:
            self.w_db['heroinven'].update_hero_passive_skill_id2(self.userid, target_hero_uid, passive_skill_id)

        # 적용 후 영웅 결과값
        after_hero = self.w_db['heroinven'].find_item(self.userid, target_hero_uid)

        # 아이템인데 영웅 타입에 맞게 res packet 구조 만들어서 response packet 만들어서 돌려준다. 
        response.confirm_hero_passive_skill.result_hero.uid = after_hero.uid
        response.confirm_hero_passive_skill.result_hero.item_id = after_hero.item_id
        response.confirm_hero_passive_skill.result_hero.tier = after_hero.tier
        response.confirm_hero_passive_skill.result_hero.exp = after_hero.exp
        response.confirm_hero_passive_skill.result_hero.dispatch_flag = after_hero.dispatch_flag
        response.confirm_hero_passive_skill.result_hero.lock_flag = after_hero.lock_flag
        response.confirm_hero_passive_skill.result_hero.passive_skill_id1 = after_hero.passive_skill_id1
        response.confirm_hero_passive_skill.result_hero.passive_skill_id2 = after_hero.passive_skill_id2

        if after_hero.potential_stat_list != None:
            potential_list = str(after_hero.potential_stat_list, 'utf-8').split(',')
            for info in potential_list:
                    statData = response.confirm_hero_passive_skill.result_hero.potential_stat_list.add()
                    data = str(info).split(':')
                    statData.type = int(data[0])
                    statData.value = int(data[1])

        response.result = Response.SUCCESS
        return

    def ExtractHeroExp(self, request, response):
        db_profile = self.w_db['profile'].select_column(self.userid, "money")
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        target_hero_uid = request.extract_hero_exp.target_hero_uid

        # 경험치 추출할 영웅이 인벤에 있는지 체크
        db_hero = self.w_db['heroinven'].find_item(self.userid, target_hero_uid)
        if not db_hero:
            response.result = Response.ITEM_INVALID
            return

        # 추출할 경험치 (소수점 올림)
        extracted_exp = int(ceil(db_hero.exp * 0.75))

        # 골드 상수 값
        extractor_gold = int(self.table.const_info.get(GAMECOMMON.EXTRACTOR_GOLD).value)

        # 소비할 골드량을 계산함
        consume_gold = db_hero.exp * extractor_gold
        if db_profile.money < consume_gold:
            response.result = Response.MONEY_LACK
            return

        self.w_db['profile'].decrease_money(self.userid, consume_gold)

        # 영웅의 현재 티어에 해당하는 승급 재료를 가져옴 
        # 영웅 테이블 id 
        # 현재 티어가 2 = 
        # 현재 티어가 3 = 
        # 현재 티어가 3이면 3티어 까지 달성한 승급재료를 전부 누적 시켜야 함
        hero_data = self.table.hero[db_hero.item_id]

        # 승급재료 구함
        promotion_data = self.table.promotion.get(hero_data.promotion_group, None)
        material_data_list = []
        for tier in range(2, db_hero.tier + 1): # 3티어인 경우 2, 3
            data = promotion_data.get(tier, None)
            material_data_list.append(data)

        update_item_dict = {}
        # 기획서상 레벨업만 하고 승급은 안한 영웅도 분해 가능 - 단지 승급한 재료가 안나올 뿐
        for material in material_data_list:
            for item_id, item_cnt in material.material_data.items():
                # 추출할 아이템 (소수점 올림)
                add_item_count = int(ceil(item_cnt / 2))

                item = self.w_db['etcinven'].find_item(self.userid, item_id)
                if not item:
                    self.w_db['etcinven'].add_item(self.userid, item.item_id, add_item_count)
                else:
                    update_count = item.item_count + add_item_count
                    update_item_dict[item.item_id] = update_count

                packet_item = response.extract_hero_exp.reward_item.add()
                packet_item.item_id = item_id
                packet_item.count = add_item_count


        # 경험치 석 지급
        packet_item = response.extract_hero_exp.reward_item.add()
        packet_item.item_id = GAMECOMMON.ITEM_HERO_EXP
        packet_item.count = extracted_exp

        etc_item = self.w_db['etcinven'].find_item(self.userid, GAMECOMMON.ITEM_HERO_EXP)
        if not etc_item:
            self.w_db['etcinven'].add_item(self.userid, GAMECOMMON.ITEM_HERO_EXP, extracted_exp)
        else:
            update_exp = etc_item.item_count + extracted_exp
            update_item_dict[GAMECOMMON.ITEM_HERO_EXP] = update_exp

        if 0 < len(update_item_dict):
            for key, value in update_item_dict.items():
                self.w_db['etcinven'].update_item_count(self.userid, key, value)

        # 추출 완료된 영웅 경치 초기화 (렙 1, 경험치 0)
        self.w_db['heroinven'].update_exp(self.userid, db_hero.uid, 0)
        # 티어도 초기화 시킴 (티어 1)
        self.w_db['heroinven'].hero_promotion(self.userid, db_hero.uid, 1)

        # 추출 후 영웅 결과값
        after_hero = self.w_db['heroinven'].find_item(self.userid, target_hero_uid)

        # 아이템인데 영웅 타입에 맞게 respacket 구조 만들어서 돌려준다. 
        response.extract_hero_exp.result_hero.uid = after_hero.uid
        response.extract_hero_exp.result_hero.item_id = after_hero.item_id
        response.extract_hero_exp.result_hero.tier = after_hero.tier
        response.extract_hero_exp.result_hero.exp = after_hero.exp
        response.extract_hero_exp.result_hero.dispatch_flag = after_hero.dispatch_flag
        response.extract_hero_exp.result_hero.lock_flag = after_hero.lock_flag
        response.extract_hero_exp.result_hero.passive_skill_id1 = after_hero.passive_skill_id1
        response.extract_hero_exp.result_hero.passive_skill_id2 = after_hero.passive_skill_id2
        response.extract_hero_exp.consume_gold = consume_gold

        if after_hero.potential_stat_list != None:
            potential_list = str(after_hero.potential_stat_list, 'utf-8').split(',')
            for info in potential_list:
                    statData = response.extract_hero_exp.result_hero.potential_stat_list.add()
                    data = str(info).split(':')
                    statData.type = int(data[0])
                    statData.value = int(data[1])

        response.result = Response.SUCCESS
        return


    def GetHeroPotentialStat(self, request, response):
        req_target_uid = request.get_hero_potential_stat.target_hero_uid
        req_kind = request.get_hero_potential_stat.slot_kind # 
        req_idx = request.get_hero_potential_stat.slot_idx # 0 ~ 5

        # 적용 영웅이 인벤에 있는지 체크
        db_hero = self.w_db['heroinven'].find_item(self.userid, req_target_uid)
        if not db_hero:
            response.result = Response.ITEM_INVALID
            return

        # 적용 영웅의 item_id를 가지고 필요한 데이터인 등급, 속성을 알아냄
        table_hero = self.table.hero.get(db_hero.item_id)
        if not table_hero:
            response.result = Response.INVALID_GAMEDATA
            return

        # 가챠를 돌린다
        define_stat, result_val = ServiceHero._gacha_stat(self, req_kind, table_hero.grade)
        result_str = "{0}:{1}".format(define_stat, result_val)

        # 재화를 소모한다
        error_code = ServiceHero._cousume_stone(self, req_idx, table_hero.element, False)
        if (error_code != None):
            response.result = error_code
            return

        # 영웅에 적용 시킴
        ServiceHero._affect_hero(self, db_hero, req_idx, req_target_uid, result_str)

        # 적용 후 영웅 결과값
        after_hero = self.w_db['heroinven'].find_item(self.userid, req_target_uid)
        response.get_hero_potential_stat.result_hero.uid = after_hero.uid
        response.get_hero_potential_stat.result_hero.item_id = after_hero.item_id
        response.get_hero_potential_stat.result_hero.tier = after_hero.tier
        response.get_hero_potential_stat.result_hero.exp = after_hero.exp
        response.get_hero_potential_stat.result_hero.dispatch_flag = after_hero.dispatch_flag
        response.get_hero_potential_stat.result_hero.lock_flag = after_hero.lock_flag
        response.get_hero_potential_stat.result_hero.passive_skill_id1 = after_hero.passive_skill_id1
        response.get_hero_potential_stat.result_hero.passive_skill_id2 = after_hero.passive_skill_id2

        if after_hero.potential_stat_list != None:
            potential_list = str(after_hero.potential_stat_list, 'utf-8').split(',')
            for info in potential_list:
                statData = response.get_hero_potential_stat.result_hero.potential_stat_list.add()
                data = str(info).split(':')
                statData.type = int(data[0])
                statData.value = int(data[1])

        response.result = Response.SUCCESS
        return
    
    def ExchangeHeroPotentialStat(self, request, response):
        req_target_uid = request.exchange_hero_potential_stat.target_hero_uid
        req_kind = request.exchange_hero_potential_stat.slot_kind
        req_idx = request.exchange_hero_potential_stat.slot_idx # 0 ~ 5

        # 적용 영웅이 인벤에 있는지 체크
        db_hero = self.w_db['heroinven'].find_item(self.userid, req_target_uid)
        if not db_hero:
            response.result = Response.ITEM_INVALID
            return

        # 적용 영웅의 item_id를 가지고 필요한 데이터인 등급, 속성을 알아냄
        table_hero = self.table.hero.get(db_hero.item_id)
        if not table_hero:
            response.result = Response.INVALID_GAMEDATA
            return

        # 가챠를 돌린다
        define_stat, result_val = ServiceHero._gacha_stat(self, req_kind, table_hero.grade)

        # 재화를 소모한다
        error_code = ServiceHero._cousume_stone(self, req_idx, table_hero.element, True)
        if (error_code != None):
            response.result = error_code
            return

        response.exchange_hero_potential_stat.potential_stat_info.type = int(define_stat)
        response.exchange_hero_potential_stat.potential_stat_info.value = int(result_val)
        response.result = Response.SUCCESS
        return
    
    def ConfirmHeroPotentialStat(self, request, response):
        req_target_uid = request.confirm_hero_potential_stat.target_hero_uid
        req_idx = request.confirm_hero_potential_stat.slot_idx
        req_stat = request.confirm_hero_potential_stat.potential_stat.type
        req_val = request.confirm_hero_potential_stat.potential_stat.value

        # 적용 영웅이 인벤에 있는지 체크
        db_hero = self.w_db['heroinven'].find_item(self.userid, req_target_uid)
        if not db_hero:
            response.result = Response.ITEM_INVALID
            return

        result_str = "{0}:{1}".format(req_stat, req_val)

        # 영웅에 적용 시킴
        ServiceHero._affect_hero(self, db_hero, req_idx, req_target_uid, result_str)

        # 적용 후 영웅 결과값
        after_hero = self.w_db['heroinven'].find_item(self.userid, req_target_uid)
        response.confirm_hero_potential_stat.result_hero.uid = after_hero.uid
        response.confirm_hero_potential_stat.result_hero.item_id = after_hero.item_id
        response.confirm_hero_potential_stat.result_hero.tier = after_hero.tier
        response.confirm_hero_potential_stat.result_hero.exp = after_hero.exp
        response.confirm_hero_potential_stat.result_hero.dispatch_flag = after_hero.dispatch_flag
        response.confirm_hero_potential_stat.result_hero.lock_flag = after_hero.lock_flag
        response.confirm_hero_potential_stat.result_hero.passive_skill_id1 = after_hero.passive_skill_id1
        response.confirm_hero_potential_stat.result_hero.passive_skill_id2 = after_hero.passive_skill_id2

        if after_hero.potential_stat_list != None:
            potential_list = str(after_hero.potential_stat_list, 'utf-8').split(',')
            for info in potential_list:
                statData = response.confirm_hero_potential_stat.result_hero.potential_stat_list.add()
                data = str(info).split(':')
                statData.type = int(data[0])
                statData.value = int(data[1])

        response.result = Response.SUCCESS
        return
    