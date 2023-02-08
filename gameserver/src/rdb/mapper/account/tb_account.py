# -*- coding: utf-8 -*-
from sqlalchemy import delete, insert, select, update

from src.rdb.sqlsession import Mapper


class AccountDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_account'
        self.taccount = self.tables[table_name]

    def find_web_userid(self, web_userid):
        query = select([self.taccount]).where(
            self.taccount.c.web_userid == web_userid
        )
        return query

    def insert_account(self, account_type, web_userid, nickname, device_info, create_time, email):
        query = insert(self.taccount).values(
            web_userid=web_userid,
            nick_name=nickname,
            account_type=account_type,
            last_login=create_time,
            login_device=device_info,
            create_time=create_time,
            email=email
        )
        return query

    def delete_account(self, userid):
        query = delete(self.taccount).where(
            self.taccount.c.account_uid == userid
        )
        return query

    def update_last_login(self, userid, time):
        query = update(self.taccount).values(
            last_login=time
        ).where(
            self.taccount.c.account_uid == userid
        )
        return query

    def select_all_account(self):
        query = select([self.taccount]).where(
            self.taccount.c.account_uid != 0
        )
        return query

    def find_user_nickname(self, nick_name):
        query = select([self.taccount]).where(
            self.taccount.c.nick_name == nick_name
        )
        return query

    def change_user_nickname(self, userid, change_nickname):
        query = update(self.taccount).values(
            nick_name=change_nickname
        ).where(
            self.taccount.c.account_uid == userid
        )
        return query

    def find_user_id(self, userid):
        query = select([self.taccount]).where(
            self.taccount.c.account_uid == userid
        )
        return query

    def update_alram_agree(self, userid, agree):
        query = update(self.taccount).values(
            push_alram_agree=agree
        ).where(
            self.taccount.c.account_uid == userid
        )
        return query


class ArenaNormalHallOfFameDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_arena_normal_hall_of_fame'
        self.thalloffame = self.tables[table_name]

    def insert_hall_of_fame(self, hall_of_fame_data):
        query = insert(self.thalloffame).values(
            rank_list=hall_of_fame_data
        )
        return query

    def remove_hall_of_fame(self, uid):
        query = delete(self.thalloffame).where(
            self.thalloffame.c.uid == uid
        )
        return query

#
#     def account_link(self, userid, account_type):
#         query = update(self.taccount).values(account_type=account_type).where(
#             self.taccount.c.account_uid == userid)
#         return query
#
#     def account_link_change(self, userid, user_token, account_type):
#         query = update(self.taccount).values(user_token=user_token, account_type=account_type).where(
#             self.taccount.c.account_uid == userid)
#         return query
#
#
# class WithDrawAccountDAO(Mapper):
#     def __init__(self, metadata):
#         Mapper.__init__(self, metadata)
#         self.twithdrawaccount = self.tables['tb_withdraw_account']
#
#     def move_account(self, account_uid, user_token, nick_name, account_type, last_login, state, device_info,
#                      build_info, create_time, email, account_lv):
#         query = insert(self.twithdrawaccount).values(
#             account_uid=account_uid,
#             user_token=user_token,
#             nick_name=nick_name,
#             account_type=account_type,
#             last_login=last_login,
#             state=state,
#             device_info=device_info,
#             build_info=build_info,
#             create_time=create_time,
#             email=email,
#             account_lv=account_lv
#             )
#
#         return query
#
#
# class HallOfFameDAO(Mapper):
#     def __init__(self, metadata):
#         Mapper.__init__(self, metadata)
#         self.thalloffame = self.tables['tb_hall_of_fame']
#
#     '''
#     DB hall_of_fame_idx(PK)
#     1 ~ 3 : PVP
#     4 ~ 6 : WAVE
#     7 ~ 9 : RAID
#     '''
#     def insert_hall_of_fame(self, hall_of_fame_idx, hall_of_fame_grade, hall_of_fame_data):
#         query = insert(self.thalloffame).values(hall_of_fame_idx=hall_of_fame_idx,
#                                                 hall_of_fame_grade=hall_of_fame_grade,
#                                                 hall_of_fame_data=hall_of_fame_data)
#         return query
#
#     def update_hall_of_fame(self, hall_of_fame_idx, hall_of_fame_grade, hall_of_fame_data):
#         query = update(self.thalloffame).values(hall_of_fame_data=hall_of_fame_data).where(
#             and_(self.thalloffame.c.hall_of_fame_idx == hall_of_fame_idx,
#                  self.thalloffame.c.hall_of_fame_grade == hall_of_fame_grade))
#         return query
#
#     def get_hall_of_fame(self, hall_of_fame_idx):
#         query = select([self.thalloffame]).where(self.thalloffame.c.hall_of_fame_idx == hall_of_fame_idx)
#         return query
#
#     def clear_hall_of_fame(self, hall_of_fame_idx):
#         query = update(self.thalloffame).values(hall_of_fame_data='{}').where(
#             self.thalloffame.c.hall_of_fame_idx == hall_of_fame_idx)
#         return query
#
#
# class PowerWarfareDAO(Mapper):
#     def __init__(self, metadata):
#         Mapper.__init__(self, metadata)
#         self.tpowerwarfareinfo = self.tables['tb_power_warfare_info']
#
#     def insert_power_warfare_info(self, power_warfare_uid):
#         # , power_warfare_user_count, daily_score, season_score, daily_rank, season_rank, power_warfare_occupy
#         query = insert(self.tpowerwarfareinfo).values(power_warfare_uid=power_warfare_uid,
#                                                       power_warfare_user_count=0,
#                                                       season_score=0,
#                                                       power_warfare_occupy=0)
#         return query
#
#     def get_power_warfare_info(self, power_warfare_uid):
#         query = select([self.tpowerwarfareinfo]).where(self.tpowerwarfareinfo.c.power_warfare_uid == power_warfare_uid)
#         return query
#
#     def get_all_power_warfare_info(self):
#         return select([self.tpowerwarfareinfo])
#
#     def update_power_warfare_user_count(self, power_warfare_uid, power_warfare_user_count):
#         query = update(self.tpowerwarfareinfo).values(power_warfare_user_count=power_warfare_user_count).where(
#             self.tpowerwarfareinfo.c.power_warfare_uid == power_warfare_uid)
#         return query
#
#     # def update_power_warfare_total_count(self, power_warfare_uid, total_user_count):
#     #     query = update(self.tpowerwarfareinfo).values(total_user_count=total_user_count).where(
#     #         self.tpowerwarfareinfo.c.power_warfare_uid == power_warfare_uid)
#     #     return query
#
#     # def set_power_warfare_user_count(self, power_warfare_uid, power_warfare_user_count, total_user_count):
#     #     query = update(self.tpowerwarfareinfo).values(power_warfare_user_count=power_warfare_user_count).where(
#     #         self.tpowerwarfareinfo.c.power_warfare_uid == power_warfare_uid)
#     #     return query
#
#     def update_power_warfare_season_record(self, power_warfare_uid, season_score, season_occupy):
#         query = update(self.tpowerwarfareinfo).values(season_score=season_score,
#                                                       power_warfare_occupy=season_occupy).where(
#             self.tpowerwarfareinfo.c.power_warfare_uid == power_warfare_uid)
#         return query
#
#     def reset_power_warfare_info(self, power_warfare_uid):
#         query = update(self.tpowerwarfareinfo).values(power_warfare_user_count=0,
#                                                       season_score=0,
#                                                       power_warfare_occupy=0
#                                                       ).where(
#             self.tpowerwarfareinfo.c.power_warfare_uid == power_warfare_uid)
#         return query
#
#
# class PowerWarfareZoneDAO(Mapper):
#     def __init__(self, metadata):
#         Mapper.__init__(self, metadata)
#         self.tpowerwarfarezoneinfo = self.tables['tb_power_warfare_zone_info']
#
#     def insert_power_warfare_zone_info(self, zone_uid):
#         # , zone_daily_score, zone_season_score, first_attack_uid
#         query = insert(self.tpowerwarfarezoneinfo).values(zone_uid=zone_uid,
#                                                           zone_season_score='{1:0, 2:0, 3:0, 4:0}')
#         return query
#
#     def get_zone_info(self, zone_uid):
#         query = select([self.tpowerwarfarezoneinfo]).where(self.tpowerwarfarezoneinfo.c.zone_uid == zone_uid)
#         return query
#
#     def get_all_zone_info(self):
#         return select([self.tpowerwarfarezoneinfo])
#
#     def update_power_warfare_zone(self, zone_uid, zone_season_score):
#         query = update(self.tpowerwarfarezoneinfo).values(zone_season_score=zone_season_score).where(
#             self.tpowerwarfarezoneinfo.c.zone_uid == zone_uid)
#         return query
#
#     def reset_power_warfare_zone(self, zone_uid):
#         query = update(self.tpowerwarfarezoneinfo).values(zone_season_score='{1:0, 2:0, 3:0, 4:0}').where(
#             self.tpowerwarfarezoneinfo.c.zone_uid == zone_uid)
#         return query
