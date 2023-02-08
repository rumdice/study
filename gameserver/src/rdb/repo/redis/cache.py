# -*- coding: utf-8 -*-

# from src.noblesseRedis.proc.user_proc import UserProc
# from src.noblesseRedis.proc.user_nick_proc import UserNickProc
#
#
# class Cache(object):
#     def __init__(self, factory):
#         self.factory = factory
#         self.user_proc = UserProc(self.factory)
#         self.user_nick_proc = UserNickProc(self.factory)
#         # self.pvp_proc = PvpProc(self.factory)
#
#     def reset(self):
#         self.factory.redis().flushdb()
#
#     def set_user_profile(self, userid, nickname, last_login, team_info, leader_info, level, exp, wave_info, profile):
#         return self.user_proc.set_profile(userid, nickname, last_login, team_info, leader_info, level, exp, wave_info,
#                                           profile)
#
#     def set_user_info(self, userid, key, value):
#         return self.user_proc.set_user_info(userid, key, value)
#
#     def get_user_info(self, userid):
#         return self.user_proc.get_user_profile(userid)
#
#     def remove_user_info(self, userid):
#         return self.user_proc.remove_user_profile(userid)
#
#     def remove_user_nick(self, nickname):
#         return self.user_nick_proc.remove_user_profile(nickname)
#
#     def set_last_login(self, userid, time):
#         self.user_proc.set_last_login(userid, time)
#
#     def set_user_info_dict(self, userid, redis_data):
#         self.user_proc.set_user_info_dict(userid, redis_data)
#
#     def set_user_random_list(self, userid):
#         self.user_nick_proc.set_user_random_list(userid)
#
#     def get_random_user(self, count):
#         return self.user_nick_proc.get_random_user(count)
#
#     def get_userid(self, name):
#         return self.user_proc.get_userid(name)
#
#     def clear(self):
#         self.user_proc.clear()
#         self.user_nick_proc.clear()
