# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *
from src.services.service_research import *


class ServiceGacha(object):
    def SummonGacha(self, request, response):
        gachaData = self.table.gacha_reward.get(request.summon_gacha.gacha_id, None)
        if not gachaData:
            response.result = Response.INVALID_RESOURCE
            return

        db_profile = self.w_db['profile'].select_column(self.userid, "cash, money, hero_inven_max")
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        hero_count = self.w_db['heroinven'].get_hero_count(self.userid)
        remain_count = db_profile.hero_inven_max - hero_count

        update_item_dict = {}
        update_cash = -1
        # 대기 소환 - 자원으로 뽑는 것
        if gachaData.type == Define.GACHA_TYPE_WAIT:
            if remain_count < gachaData.need_inven:
                response.result = Response.INVEN_SLOT_LACK
                return

            altar_level = 1
            redis_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO)
            if redis_data:
                redis_dict = convert_string_to_dict(redis_data)
                self.wait_build_process(redis_dict)
                altar_level = redis_dict[Define.BUILDING_TYPE_ALTAR]

            if altar_level < gachaData.summon_level:
                response.result = Response.LEVEL_LACK
                return

            db_items = self.w_db['etcinven'].find_item_list(self.userid, gachaData.use_item)
            if not db_items:
                response.result = Response.ITEM_INVALID
                return

            if len(db_items) != len(gachaData.use_item):
                response.result = Response.ITEM_INVALID
                return

            for item in db_items:
                consume_count = gachaData.use_dict[item.item_id]
                # 연구소 효과 적용
                reduce_item = ReserchAffectSummonGachaCost(self, consume_count)
                consume_count = consume_count - reduce_item

                update_count = item.item_count - consume_count
                if 0 > update_count:
                    response.result = Response.ITEM_COUNT_LACK
                    return

                update_item_dict[item.item_id] = update_count

                useItem = response.summon_gacha.use_items.add()
                useItem.item_id = item.item_id
                useItem.count = consume_count

        # 고급 소환 - 바로 뽑음
        elif gachaData.type == Define.GACHA_TYPE_ADVANCED:
            gacha_table = self.table.gacha_reward
            gacha_row = gacha_table.get(gachaData.gacha_id)
            # 보석 뽑기
            item_id = gacha_row['use_item'][0]
            item_qty = gacha_row.use_dict.get(item_id)
            
            if item_id == GAMECOMMON.ITEM_RUBY_ID:
                update_cash = db_profile.cash - gachaData.use_dict[GAMECOMMON.ITEM_RUBY_ID]
                if 0 > update_cash:
                    response.result = Response.CASH_LACK
                    return
            # 소환권 뽑기
            else:
                db_items = self.w_db['etcinven'].find_item(self.userid, item_id)
                if not db_items:
                    response.result = Response.ITEM_INVALID
                    return

                update_count = db_items.item_count - item_qty
                if 0 > update_count:
                    response.result = Response.ITEM_INVALID
                    return

                update_item_dict[GAMECOMMON.ITEM_SUMMON] = update_count

                useItem = response.summon_gacha.use_items.add()
                useItem.item_id = GAMECOMMON.ITEM_SUMMON
                useItem.count = 1
        else:
            pass

        rewardData = self.table.reward_set.get(gachaData.reward_set, None)
        if not rewardData:
            response.result = Response.INVALID_RESOURCE
            return

        db_info = self.w_db['gacha'].get_gacha(self.userid, request.summon_gacha.gacha_id)
        if not db_info:
            self.w_db['gacha'].add_gacha(self.userid, request.summon_gacha.gacha_id, self.begin)

        db_gacha = self.w_db['gacha'].get_gacha(self.userid, request.summon_gacha.gacha_id)
        
        refresh_tick = gachaData.refresh_hour * 60 * 60
        # 연구소 효과 적용 - 43200 (12h) 이면 10%퍼 까서 38880
        reduce_tick = ReserchAffectSummonGachaTime(self, refresh_tick)
        refresh_tick = refresh_tick - reduce_tick

        remain_time = db_gacha.summon_time + timedelta(seconds=refresh_tick)
        remain_time_utc = int(convert_date_to_utc(remain_time))

        response.summon_gacha.gacha_info.gacha_id = request.summon_gacha.gacha_id
        response.summon_gacha.gacha_info.remain_time = remain_time_utc

        update_time = get_pass_time(0, gachaData.refresh_hour, 0)
        self.w_db['gacha'].update_gacha_time(self.userid, request.summon_gacha.gacha_id, update_time)

        item_dict = self.get_reward_list(gachaData.reward_set)

        self.reward_packet_process(
            item_dict,
            response.summon_gacha.reward_list
        )

        if 0 < len(update_item_dict):
            for key, value in update_item_dict.items():
                self.w_db['etcinven'].update_item_count(self.userid, key, value)

        if 0 <= update_cash:
            self.w_db['profile'].update_cash(self.userid, update_cash)

        response.result = Response.SUCCESS
        return


    def SummonGachaList(self, response):
        db_info = self.w_db['gacha'].get_gacha_all(self.userid)
        if not db_info:
            response.result = Response.SUCCESS
            return

        for gacha in db_info:
            gacha_info = response.summon_gacha_list.gacha_info_list.add()
            gacha_info.gacha_id = gacha.gacha_id
            
            refresh_tick = calc_time_to_seconds(self.begin, gacha.summon_time)
            if 0 > refresh_tick:
                refresh_tick = 0

            # 연구소 효과 적용 - 43200 (12h) - 0 이면 10%퍼 까서 38880
            reduce_tick = ReserchAffectSummonGachaTime(self, refresh_tick)
            refresh_tick = refresh_tick - reduce_tick

            remain_time = gacha.summon_time + timedelta(seconds=refresh_tick)
            remain_time_utc = int(convert_date_to_utc(remain_time))

            gacha_info.remain_time = remain_time_utc

        response.result = Response.SUCCESS
        return