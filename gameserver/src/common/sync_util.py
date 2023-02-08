# -*- coding: utf-8 -*-
# import time
# from functools import wraps

# from src.common.gamecommon import GAMECOMMON
# from src.noblesse_pb2 import Response

# __author__ = 'tteogi'


# class SyncUtil(object):
#     def __init__(self, update_second, *args):
#         self.__update_time = update_second
#         self.__next_update_time = 0
#         self.__update_functions = args
#         self.__data = None

#     def _force_update_data(self):
#         for update in self.__update_functions:
#             update()

#     def _update_data(self):
#         cur_time = time.time()
#         if cur_time > self.__next_update_time:
#             self.__next_update_time = self.__update_time + cur_time
#             for update in self.__update_functions:
#                 update()


# class RankingSync(SyncUtil):
#     def __init__(self, update_second, ranking_name, ranking_repository):
#         self.__ranking_repository = ranking_repository
#         self.__pvp_route = ranking_name
#         super(RankingSync, self).__init__(update_second, self.__update_ranking, self.__update_ranking_user_count)

#     def get_sync_ranking_users(self, forceSync=True):
#         if forceSync:
#             self._force_update_data()
#         else:
#             self._update_data()
#         return self.__ranking_users

#     def get_ranking_users(self):
#         self._update_data()
#         return self.__ranking_users

#     def get_ranking_user_count(self):
#         self._update_data()
#         return self.__ranking_user_count

#     def __update_ranking(self):
#         rankings = self.__ranking_repository.get_low_rankings(self.__pvp_route.raking_name, 1, 100)
#         user_ids = []
#         user_scores = []
#         for ranking in rankings:
#             user_ids.append((int(ranking[0])))
#             user_scores.append((int(ranking[1])))

#         if len(user_ids) < 1:
#             return

#         # if self.__ranking_name == GAMECOMMON.BEST_WAR_RANKING:
#         self.__add_best_war_user(user_ids, user_scores)

#     def __update_ranking_user_count(self):
#         self.__ranking_user_count = self.__ranking_repository.total_count(self.__pvp_route.raking_name)

#     def __add_best_war_user(self, user_ids, user_scores):
#         users = self.__ranking_repository.get_users_info_keys(
#             user_ids, [GAMECOMMON.USERID, GAMECOMMON.NICKNAME, GAMECOMMON.DELEGATE_AVATAR, self.__pvp_route.power_key
#                 , GAMECOMMON.EXP, self.__pvp_route.win_score_key])

#         self.__ranking_users = Response.GetRankings()
#         for idx, user_dict in enumerate(users):
#             ranking_user = self.__ranking_users.rankings.add()
#             ranking_user.userid = int(user_dict[0])
#             ranking_user.nickname = str(user_dict[1], 'utf-8')
#             ranking_user.score = user_scores[idx]
#             ranking_user.ranking = idx + 1
#             ranking_user.delegate_avatar = int(user_dict[2])
#             ranking_user.attack_power = int(user_dict[3]) if user_dict[3] is not None else 0
#             ranking_user.exp = int(user_dict[4]) if user_dict[4] is not None else 0
#             if user_dict[5] != None:
#                 ranking_user.win_count, ranking_user.lose_count = self.__pvp_route.get_win_count(int(user_dict[5]))
