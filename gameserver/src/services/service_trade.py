# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


class ServiceTrade(object):
    def __init__(self):
        self.GetTradeItem = {
            1: lambda tradeItem: (tradeItem.trade_item1, "trade_item1"),
            2: lambda tradeItem: (tradeItem.trade_item2, "trade_item2"),
            3: lambda tradeItem: (tradeItem.trade_item3, "trade_item3"),
            4: lambda tradeItem: (tradeItem.trade_item4, "trade_item4"),
        }


    def _get_buy_item(self):
        rand_value = util_get_rand_range(1, 10000)
        prob_value = 0
        for item in self.trade_item_buy:
            if (prob_value + item.prob) >= rand_value:
                return item.item_id

            prob_value += item.prob

        return 0

    def _get_sell_item(self):
        rand_value = util_get_rand_range(1, 10000)
        prob_value = 0
        for item in self.trade_item_sell:
            if (prob_value + item.prob) >= rand_value:
                return item.item_id

            prob_value += item.prob

        return 0

    def _get_trade_id(self):
        rand_value = util_get_rand_range(1, 10000)
        prob_value = 0
        for goods in self.trade_goods_list:
            if not goods:
                continue

            if (prob_value + goods.prob) >= rand_value:
                return goods.table_id

            prob_value += goods.prob

        return 0

    def _refreshTradeItems(self, level, building_uid, response, updateTime):
        build_info = self.table.build_create[Define.BUILDING_TYPE_TRADE_SHIP]
        itemcount = build_info[level].produce

        update_list = []
        update_list.append([0, 0, 0, 0])
        update_list.append([0, 0, 0, 0])
        update_list.append([0, 0, 0, 0])
        update_list.append([0, 0, 0, 0])

        for count in range(itemcount):
            buy_item = ServiceTrade._get_buy_item(self)
            sell_item = ServiceTrade._get_sell_item(self)
            table_id = ServiceTrade._get_trade_id(self)
            update_list[count][0] = table_id
            update_list[count][1] = sell_item
            update_list[count][2] = buy_item

        self.w_db['tradeitem'].update_tradeitems(
            self.userid,
            building_uid,
            str(update_list[0]),
            str(update_list[1]),
            str(update_list[2]),
            str(update_list[3]),
            updateTime
        )

        for item in update_list:
            if 0 >= item[0]:
                break

            trade_item = response.trade_item_list.trade_items.add()
            trade_item.table_id = item[0]
            trade_item.sell_item = item[1]
            trade_item.buy_item = item[2]
            trade_item.disable_flag = bool(item[3])

        return


    def TradeItemList(self, request, response):
        redis_info = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO)
        if not redis_info:
            response.result = Response.USER_INVALID
            return

        redis_territory = convert_string_to_dict(redis_info)
        self.wait_build_process(redis_territory)

        build_dict = redis_territory[Define.BUILDING_TYPE_TRADE_SHIP]
        building_lv = build_dict.get(request.trade_item_list.building_uid, None)
        if not building_lv:
            response.trade_item_list.next_refresh_time = GAMECOMMON.TRADE_REFRESH_SECOND
            response.result = Response.SUCCESS
            return

        db_tradeitem = self.w_db['tradeitem'].get_tradeitems(self.userid, request.trade_item_list.building_uid)
        if not db_tradeitem:
            self.w_db['tradeitem'].insert_tradeitems(self.userid, request.trade_item_list.building_uid, self.begin)
            ServiceTrade._refreshTradeItems(self, building_lv, request.trade_item_list.building_uid, response, self.begin)
            response.trade_item_list.next_refresh_time = GAMECOMMON.TRADE_REFRESH_SECOND
            response.result = Response.SUCCESS
            return

        remain_time = time_diff_in_seconds(db_tradeitem.refresh_time)
        if remain_time > GAMECOMMON.TRADE_REFRESH_SECOND:
            remain_time = remain_time % GAMECOMMON.TRADE_REFRESH_SECOND
            next_time = GAMECOMMON.TRADE_REFRESH_SECOND - remain_time
            refresh_time = self.begin + timedelta(seconds=next_time)

            ServiceTrade._refreshTradeItems(self, building_lv, request.trade_item_list.building_uid, response, refresh_time)
            response.trade_item_list.next_refresh_time = time_diff_in_seconds(refresh_time)
            response.result = Response.SUCCESS
            return

        trade_items = []
        trade_items.append(convert_string_to_array(db_tradeitem.trade_item1))
        trade_items.append(convert_string_to_array(db_tradeitem.trade_item2))
        trade_items.append(convert_string_to_array(db_tradeitem.trade_item3))
        trade_items.append(convert_string_to_array(db_tradeitem.trade_item4))

        for item in trade_items:
            if 0 >= item[0]:
                break

            trade_item = response.trade_item_list.trade_items.add()
            trade_item.table_id = item[0]
            trade_item.sell_item = item[1]
            trade_item.buy_item = item[2]
            trade_item.disable_flag = bool(item[3])

        gap_time = calc_time_to_seconds(db_tradeitem.refresh_time, self.begin)
        if 0 < gap_time:
            remain_time = GAMECOMMON.TRADE_REFRESH_SECOND - gap_time

        response.trade_item_list.next_refresh_time = remain_time
        response.result = Response.SUCCESS
        return

    def TradeItemBuy(self, request, response):
        db_tradeitem = self.w_db['tradeitem'].get_tradeitems(self.userid, request.trade_item_buy.building_uid)
        if not db_tradeitem:
            response.result = Response.ITEM_INVALID
            return

        try:
            column_value, column_name = self.GetTradeItem[request.trade_item_buy.buy_item_number](db_tradeitem)
        except Exception as e:
            response.result = Response.FIELD_MISSING
            return

        tradeitem = convert_string_to_array(column_value)
        disable_flag = tradeitem[3]
        if disable_flag == True:
            response.result = Response.TRADE_ITEM_DISABLE
            return

        table_id = tradeitem[0]
        trade_data = self.table.trade_goods[table_id]
        if not trade_data:
            response.result = Response.INVALID_RESOURCE
            return

        buy_item_id = tradeitem[2]
        goods_info = trade_data.goods_dict.get(buy_item_id, None)
        if not goods_info:
            response.result = Response.INVALID_RESOURCE
            return

        buy_item_cnt = goods_info.buy_count
        update_count = 0
        db_profile = None
        befor_buy_count = 0
        if buy_item_id == GAMECOMMON.ITEM_GOLD_ID:
            db_profile = self.w_db['profile'].select_column(self.userid, "money")
            if not db_profile:
                response.result = Response.USER_INVALID
                return

            befor_buy_count = db_profile.money
        else:
            db_item = self.w_db['etcinven'].find_item(self.userid, buy_item_id)
            if not db_item:
                response.result = Response.ITEM_COUNT_LACK
                return

            befor_buy_count = db_item.item_count

        update_count = befor_buy_count - buy_item_cnt
        if 0 > update_count:
            response.result = Response.ITEM_COUNT_LACK
            return

        response.trade_item_buy.buy_item_number = request.trade_item_buy.buy_item_number
        response.trade_item_buy.use_item.item_id = buy_item_id
        response.trade_item_buy.use_item.count = buy_item_cnt

        tradeitem[3] = 1

        sell_item_id = tradeitem[1]
        goods_info = trade_data.goods_dict.get(sell_item_id, None)
        if not goods_info:
            response.result = Response.INVALID_RESOURCE
            return

        purchase_info = {}
        purchase_info[buy_item_id] = buy_item_cnt
        
        sell_item_count = goods_info.sell_count
        product_info = {}
        product_info[sell_item_id] = sell_item_count

        if buy_item_id == GAMECOMMON.ITEM_GOLD_ID:
            self.w_db['profile'].update_money(self.userid, update_count)
        else:
            self.w_db['etcinven'].update_item_count(self.userid, buy_item_id, update_count)

        if sell_item_id == GAMECOMMON.ITEM_GOLD_ID:
            self.w_db['profile'].increase_money(self.userid, sell_item_count)
        else:
            redis_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_TERRITORY_INFO)
            if not redis_data:
                response.result = Response.USER_INVALID
                return

            redis_territory = convert_string_to_dict(redis_data)
            try:
                storageMax = self.GetItemMax[sell_item_id](redis_territory)
            except Exception as e:
                self.logger.exception(e.message)
                response.result = Response.INVALID_RESOURCE
                return

            db_item = self.w_db['etcinven'].find_item(self.userid, sell_item_id)
            if db_item:
                if (db_item.item_count + sell_item_count) > storageMax:
                    sell_item_count = storageMax - db_item.item_count

            if 0 < sell_item_count:
                self.w_db['etcinven'].add_item(self.userid, sell_item_id, sell_item_count)
            else:
                sell_item_count = 0

        response.trade_item_buy.buy_item.item_id = sell_item_id
        response.trade_item_buy.buy_item.count = sell_item_count

        self.w_db['tradeitem'].update_tradeitem_column(
            self.userid,
            request.trade_item_buy.building_uid,
            column_name,
            str(tradeitem)
        )

        response.result = Response.SUCCESS
        return