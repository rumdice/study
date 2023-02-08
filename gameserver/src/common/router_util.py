# -*- coding: utf-8 -*-
# import ast
# import time
# from src.common.gamecommon import GAMECOMMON
# # from src.noblesse_pb2 import GameStage, RealTimeEvent, Mission, MarketItem
#
# __author__ = 'tteogi'
#
# class Bunch(dict):
#     def __init__(self, *args, **kwds):
#         dict.__init__(self, *args, **kwds)
#         self.__dict__ = self
#
# class PvpRoute(object):
#     __db_keys = { }
#     @staticmethod
#     def get_route(type):
#         key = PvpRoute.__db_keys.get(type)
#         if key == None:
#             route = PvpRoute(type)
#             PvpRoute.__db_keys[type] = route
#             return route
#         return key
#
#     def __init__(self, pvp_type):
#         self.pvp_type = pvp_type
#         if pvp_type == GameStage.MISSION_BIG_WAR_MODE:
#             self.stage_type = GameStage.MISSION_BIG_WAR_MODE
#             self.raking_name = GAMECOMMON.BIG_WAR_RANKING
#             self.expire_key = GAMECOMMON.PVP_EXPIRE
#             self.target_id_key = GAMECOMMON.PVP_USERID
#             self.team_key = GAMECOMMON.PVP_TEAM_SLUG
#             self.score_key = GAMECOMMON.BIG_WAR_SCORE
#             self.power_key = GAMECOMMON.BIG_WAR_ATTACK_POWER
#             self.play_count_key = GAMECOMMON.BIG_WAR_PLAY_COUNT
#             self.remain_time_key = GAMECOMMON.BIG_WAR_REMAIN_TIME
#             self.max_play_count = GAMECOMMON.MAX_PVP_COUNT
#             self.start_mission_type = Mission.BIG_WAR_MISSION_ATTENDED
#             self.charge_ticket_time = GAMECOMMON.PVP_TICKET_CHARGE_SECOND
#             self.win_score_key = GAMECOMMON.BIG_WAR_WIN_SCORE
#         else:
#             self.stage_type = GameStage.MISSION_BEST_WAR_MODE
#             self.raking_name = GAMECOMMON.BEST_WAR_RANKING
#             self.expire_key = GAMECOMMON.BEST_WAR_EXPIRE
#             self.target_id_key = GAMECOMMON.BEST_WAR_USERID
#             self.team_key = GAMECOMMON.BEST_WAR_TEAM_SLUG
#             self.score_key = GAMECOMMON.BEST_WAR_SCORE
#             self.power_key = GAMECOMMON.BEST_WAR_ATTACK_POWER
#             self.play_count_key = GAMECOMMON.BEST_WAR_PLAY_COUNT
#             self.remain_time_key = GAMECOMMON.BEST_WAR_REMAIN_TIME
#             self.max_play_count = GAMECOMMON.MAX_BEST_WAR_COUNT
#             self.start_mission_type = Mission.BEST_WAR_MISSION_ATTENDED
#             self.charge_ticket_time = GAMECOMMON.PVP_TICKET_CHARGE_SECOND
#             self.win_score_key = GAMECOMMON.BEST_WAR_WIN_SCORE
#
#     def get_team_lists(self, team):
#         compose_team_setting = None
#         # if self.pvp_type == GameStage.MISSION_BIG_WAR_MODE:
#         #     compose_team_setting = []
#         #     for idx, team_set in enumerate(team):
#         #         compose_team_setting.append([team_set.slug_ids, team_set.character_id])
#         # elif self.pvp_type == GameStage.MISSION_BEST_WAR_MODE:
#         # [[[team_slot, slug_id],[team_slot, slug_id]], [[team_slot, character_id], [team_slot, character_id]]]
#         # 구조로 디비에 저장 됨
#
#         compose_team_setting =[None] *len(team)
#         for idx, team_set in enumerate(team):
#             # if team_set.slug_ids:
#             #     slugs.append([team_set.team_slot, team_set.slug_ids])
#             # if team_set.character_id:
#             #     characters.append([team_set.team_slot, team_set.character_id])
#             # if team_set.slug_ids == 0 and team_set.character_id == 0:
#             #     raise Exception("empty team info")
#             compose_team_setting[idx] = [team_set.team_slot, team_set.slug_ids, team_set.character_id]
#
#         # slugs =[]
#         # characters =[]
#         # for idx, team_set in enumerate(team):
#         #     if team_set.slug_ids:
#         #         slugs.append([team_set.team_slot, team_set.slug_ids])
#         #     if team_set.character_id:
#         #         characters.append([team_set.team_slot, team_set.character_id])
#         #     if team_set.slug_ids == 0 and team_set.character_id == 0:
#         #         raise Exception("empty team info")
#         # compose_team_setting = [slugs, characters]
#         return compose_team_setting
#
#     # def get_team_list(self, request):
#     #     team = None
#     #     characters = []
#     #     slugs = []
#     #
#     #     valid = [False, False]
#     #     if self.pvp_type == GameStage.MISSION_BIG_WAR_MODE:
#     #         if not request.lobby_pvp.lobby_user or len(request.lobby_pvp.lobby_user) < 1:
#     #             return  None
#     #         team = [[]*1]
#     #         for pair in request.lobby_pvp.lobby_user:
#     #             if pair.slug_uids:
#     #                 valid[0] = True
#     #                 slugs.append(pair.slug_uids)
#     #             if pair.character_uid:
#     #                 characters.append(pair.character_uid)
#     #             team[0].append([pair.slug_uids, pair.character_uid])
#     #         if valid[0] == False:
#     #             return None, None, None
#     #     elif self.pvp_type == GameStage.MISSION_BEST_WAR_MODE:
#     #         if not request.lobby_pvp.lobby_team or len(request.lobby_pvp.lobby_team) < 1:
#     #             return  None
#     #         team = [[]*3]
#     #         for lobby_team in request.lobby_pvp.lobby_team:
#     #             team_slot = lobby_team.team_slot - 1
#     #             for pair in lobby_team.lobby_user:
#     #                 if pair.slug_uids:
#     #                     valid[0] = True
#     #                     slugs.append(pair.slug_uids)
#     #                 if pair.character_uid:
#     #                     valid[1] = True
#     #                     characters.append(pair.character_uid)
#     #                 team[team_slot].append([pair.slug_uids, pair.character_uid])
#     #             if valid != [True, True]:
#     #                 valid = [False, False]
#     #         if valid != [True, True]:
#     #             return None, None, None
#     #     return characters, slugs, team
#
#     def get_win_count(self, win_score_value):
#         value = long(win_score_value)
#         win_count = ( value >> 32 ) & 0xffffffff
#         lose_count = value & 0xffffffff
#         return win_count, lose_count
#
#     def convert_win_score(self, win_count, lose_count):
#         return ( win_count << 32 ) | lose_count
#
#
#     def response_lobby_setting(self, team_setting , response):
#         if self.pvp_type == GameStage.MISSION_BIG_WAR_MODE:
#             for team in team_setting:
#                 for pair in team:
#                     lobby_user = response.lobby_pvp.lobby_user.add()
#                     lobby_user.slug_uids = int(pair[0])
#                     lobby_user.character_uid = int(pair[1])
#         elif self.pvp_type == GameStage.MISSION_BEST_WAR_MODE:
#             for idx, team in enumerate(team_setting):
#                 lobby_team = response.lobby_pvp.lobby_team.add()
#                 lobby_team.team_slot = idx + 1
#                 for pair in team:
#                     lobby_user = lobby_team.lobby_user.add()
#                     lobby_user.slug_uids = int(pair[0])
#                     lobby_user.character_uid = int(pair[1])
#
#
# class MarketRoute(object):
#     __db_keys = { }
#     __event_markets = [GAMECOMMON.MONTHLY_PURCHASE_EVENT, GAMECOMMON.ANNIVERSARY_EVENT, GAMECOMMON.PURCHASE_EVENT]
#     @staticmethod
#     def get_route(market_type):
#         key = MarketRoute.__db_keys.get(market_type)
#         if key == None:
#             market_route = MarketRoute(market_type)
#             MarketRoute.__db_keys[market_type] = market_route
#             return market_route
#         return key
#
#     def __init__(self, market_type):
#         if market_type in MarketRoute.__event_markets: # 이벤트용
#             self.market_type = market_type
#             self.type_key = market_type + "_uid"
#             self.buys_key = self.type_key + "_count"
#         # elif market_type >= MarketItem.PREMIUM_CAPSULE_MARKET or market_type <= MarketItem.GOLD_CAPSULE_MARKET:
#         #     self.market_type = market_type
#         #     self.type_key = 'market' + str(market_type)
#         #     self.expire_key = self.type_key + "_expire"
#         #     self.buys_key = self.type_key + "_buys"
#         #     self.cool_time = self.type_key + "cool_time"
#         else:
#             self.market_type = market_type
#             self.type_key = 'market' + str(market_type)
#             self.items_key = self.type_key + "_items"
#             self.expire_key = self.type_key + "_expire"
#             self.buys_key = self.type_key + "_buys"