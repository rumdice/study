# -*- coding:utf-8 -*-

# from random import randint

# from src.common.gamecommon import GAMECOMMON
# from src.noblesseRedis.proc.pvp_proc import PvpProc


# class Ranking(object):
#     def __init__(self, factory):
#         self.factory = factory
#         self.pvp_proc = PvpProc(self.factory)

#     def set_pvp_info(self, userid, pvp_point):
#         return self.pvp_proc.set_pvp_info(userid, pvp_point)

#     # def set_chaos_info(self, userid, rank):
#     #     return self.pvp_proc.set_chaos_info(userid, rank)

#     def stamina_battle_point(self, userid, point):
#         return self.pvp_proc.stamina_battle_point(userid, point)

#     def get_stamina_battle_score_rank(self, score):
#         return int(self.pvp_proc.get_stamina_battle_score_rank(score))

#     # def get_pvp_target(self, grade, high, low):
#     #     return self.pvp_proc.get_pvp_target(grade, high, low)

#     # def get_rank_count(self, grade):
#     #     return self.pvp_proc.get_rank_count(grade)

#     # def get_my_rank(self, grade, userid):
#     #     return self.pvp_proc.get_my_rank(grade, userid)

#     # def update_pvp_info(self, userid, key, value):
#     #     return self.pvp_proc.update_pvp_info(userid, key, value)
#     #
#     # def update_pvp_info_dict(self, userid, data):
#     #     return self.pvp_proc.update_pvp_info_dict(userid, data)

#     def update_pvp_point(self, userid, score):
#         return self.pvp_proc.update_pvp_point(userid, score)

#     def get_total_rank(self, userid):
#         return self.pvp_proc.get_total_rank(userid)

#     def get_score_rank(self, score):
#         return self.pvp_proc.get_score_rank(score)

#     def get_my_point(self, userid):
#         return self.pvp_proc.get_my_point(userid)

#     def get_total_rank_count(self):
#         return self.pvp_proc.get_total_rank_count()

#     def total_rank_list(self, high, low):
#         return self.pvp_proc.total_rank_list(high, low)

#     def get_stamina_battle_rank(self, high, low):
#         return self.pvp_proc.get_stamina_battle_rank(high, low)

#     # def get_chaos_rank_count(self):
#     #     return self.pvp_proc.get_chaos_rank_count()

#     def get_stamina_battle_rank_count(self):
#         return self.pvp_proc.get_stamina_battle_rank_count()

#     def stamina_rank_range(self, high, low):
#         return self.pvp_proc.stamina_rank_range(high, low)

#     # def chaos_rank(self, userid):
#     #     return self.pvp_proc.chaos_rank(userid)

#     # def chaos_rank_range(self, high, low):
#     #     return self.pvp_proc.chaos_rank_range(high, low)

#     # def chaos_rank_user(self, rank):
#     #     return self.pvp_proc.chaos_rank_user(rank)

#     def stamina_battle_rank_user(self, rank):
#         return self.pvp_proc.stamina_battle_rank_user(rank)

#     def get_stamina_battle_point(self, userid):
#         return self.pvp_proc.get_stamina_battle_point(userid)

#     # guild battle
#     def set_guild_battle_rank(self, guild_uid, point):
#         return self.pvp_proc.set_guild_battle_rank(guild_uid, point)

#     def get_guild_battle_rank(self, guild_uid):
#         return self.pvp_proc.get_guild_battle_rank(guild_uid)

#     def get_guild_battle_rank_count(self):
#         return self.pvp_proc.get_guild_battle_rank_count()

#     def get_guild_battle_rank_list(self):
#         return self.pvp_proc.get_guild_battle_rank_list()

#     def guild_battle_rank_list(self, high, low):
#         return self.pvp_proc.guild_battle_rank_list(high, low)

#     def incry_guild_battle_rank(self, guild_uid, point):
#         return self.pvp_proc.incry_guild_battle_rank(guild_uid, point)

#     def get_guild_battle_score(self, guild_uid):
#         return self.pvp_proc.get_guild_battle_score(guild_uid)

#     def del_guild_battle_rank(self, guild_uid):
#         self.pvp_proc.del_guild_battle_rank(guild_uid)
#         return

#     def battle_point_rank(self, point):
#         return self.pvp_proc.battle_point_rank(point)

#     def clear(self):
#         return self.pvp_proc.clear()

#     def guild_battle_rank_clear(self):
#         return self.pvp_proc.guild_battle_rank_clear()

#     def set_raid_damage_rank(self, userid, damage):
#         self.pvp_proc.set_raid_damage_rank(userid, damage)
#         return

#     def get_guild_raid_damage_rank_list(self, high, low):
#         return self.pvp_proc.get_guild_raid_damage_rank_list(high, low)

#     def get_guild_raid_damage_rank(self, userid):
#         return self.pvp_proc.get_guild_raid_damage_rank(userid)

#     def get_my_raid_damage(self, userid):
#         return self.pvp_proc.get_my_raid_damage(userid)

#     def guild_raid_damage_rank_clear(self):
#         self.pvp_proc.guild_raid_damage_rank_clear()
#         return
