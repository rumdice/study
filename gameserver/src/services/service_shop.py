# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


class ServiceShop(object):

    def _get_return_point_shop_item(self, shop_id):
        return self.table.shop_return_point.get(shop_id, None)

    def _get_arena_coin_shop_item(self, shop_id):
        return self.table.shop_arena_coin.get(shop_id, None)

    def ReturnPointBuyItem(self, request, response):
        db_info = self.w_db['profile'].select_column(self.userid, "last_mode, money")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        shop_id = request.return_point_buy_item.shop_id
        shop_data = ServiceShop._get_return_point_shop_item(self, shop_id)
        db_item_point = self.w_db['etcinven'].find_item(self.userid, GAMECOMMON.ITEM_RETURN_POINT)
        if not db_item_point:
            response.result = Response.ITEM_COUNT_LACK
            return
        update_point_count = db_item_point.item_count - shop_data.price
        if 0 > update_point_count:
            response.result = Response.ITEM_COUNT_LACK
            return

        self.w_db['etcinven'].update_item_count(
            self.userid,
            GAMECOMMON.ITEM_RETURN_POINT,
            update_point_count
        )

        item_dict = {}
        db_update = []
        value_list = []
        self.table.get_reward_item_by_group_id(shop_data.reward, item_dict)
        self.reward_packet_process_profile(
            item_dict,
            response.return_point_buy_item.reward_items,
            db_update,
            value_list,
            db_info
        )
        response.return_point_buy_item.use_count = shop_data.price
        response.return_point_buy_item.result_value = update_point_count
        response.result = Response.SUCCESS
        return


    def ArenaCoinBuyItem(self, request, response):
        db_info = self.w_db['profile'].select_column(self.userid, "last_mode, money")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        shop_id = request.arena_coin_buy_item.shop_id
        shop_data = ServiceShop._get_arena_coin_shop_item(self, shop_id)
        db_item_point = self.w_db['etcinven'].find_item(self.userid, GAMECOMMON.ITEM_ARENA_COIN)
        if not db_item_point:
            response.result = Response.ITEM_COUNT_LACK
            return
        update_point_count = db_item_point.item_count - shop_data.price
        if 0 > update_point_count:
            response.result = Response.ITEM_COUNT_LACK
            return

        self.w_db['etcinven'].update_item_count(self.userid, GAMECOMMON.ITEM_ARENA_COIN, update_point_count)

        item_dict = {}
        db_update = []
        value_list = []
        self.table.get_reward_item_by_group_id(shop_data.reward, item_dict)
        self.reward_packet_process_profile(
            item_dict,
            response.arena_coin_buy_item.reward_items,
            db_update,
            value_list,
            db_info
        )
        response.arena_coin_buy_item.use_count = shop_data.price
        response.arena_coin_buy_item.result_value = update_point_count
        response.result = Response.SUCCESS
        return