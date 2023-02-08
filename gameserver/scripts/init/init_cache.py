# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime

from context import GameServerContext, init_callback
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import Define
from src.services.service_arena import *
from src.services.service_common import *
from src.services.service_guild import *
from src.tables.table_Base import TableBase


class RedisInitialize(ServiceCommon):
    def __init__(self, context):
        ServiceCommon.__init__(self)
        self.userid = None
        self.begin = None
        self.context = context
        self.table = TableBase()
        self.w_db = context.w_db

        self.cache = context.cache

        self.guild = context.guild

    def redis_flush(self):
        self.cache.clear()

    def update_progress(self, progress, total):
        printProgressBar(progress, total, prefix = 'Progress:', suffix = 'Complete', length = 20, fill = '>')

    def total_account(self):
        account_list = self.w_db['account'].select_all_account()
        total_count = len(account_list)
        print(datetime.now(), "start total_account total_count:" + str(total_count))
        printProgressBar(0, total_count, prefix = 'Progress:', suffix = 'Complete', length = 20)

        for i, account in enumerate(account_list):
            userinfo = self.w_db['profile'].find_profile(account.account_uid)
            if not userinfo:
                print("not userinfo continue")
                continue

            territory_dict = {}
            territory_dict[Define.BUILDING_TYPE_CASTLE] = 1
            territory_dict[Define.BUILDING_TYPE_ALTAR] = 1
            territory_dict[Define.BUILDING_TYPE_FOOD_STORAGE] = self.table.const_info.get(GAMECOMMON.BASE_FOOD_STORAGE).value
            territory_dict[Define.BUILDING_TYPE_IRON_STORAGE] = self.table.const_info.get(GAMECOMMON.BASE_IRON_STORAGE).value
            territory_dict[Define.BUILDING_TYPE_STONE_STORAGE] = self.table.const_info.get(GAMECOMMON.BASE_STONE_STORAGE).value
            territory_dict[Define.BUILDING_TYPE_WOOD_STORAGE] = self.table.const_info.get(GAMECOMMON.BASE_WOOD_STORAGE).value
            territory_dict[Define.BUILDING_TYPE_TRADE_SHIP] = {}
            territory_dict[Define.BUILDING_TYPE_WORKSHOP] = {}

            redis_data = {}
            db_building_list = self.w_db['territory'].select_all_building(account.account_uid)
            for building in db_building_list:
                if building.building_type == Define.BUILDING_TYPE_CASTLE:
                    if 0 != building.level:
                        territory_dict[Define.BUILDING_TYPE_CASTLE] = building.level
                    else:
                        territory_dict[Define.BUILDING_TYPE_CASTLE] = self.check_wait_building(account.account_uid, building.uid)

                elif building.building_type == Define.BUILDING_TYPE_ALTAR:
                    if 0 != building.level:
                        territory_dict[Define.BUILDING_TYPE_ALTAR] = building.level
                    else:
                        territory_dict[Define.BUILDING_TYPE_ALTAR] = self.check_wait_building(account.account_uid, building.uid)

                elif building.building_type == Define.BUILDING_TYPE_LABORATORY:
                    if 0 != building.level:
                        territory_dict[Define.BUILDING_TYPE_LABORATORY] = building.level
                    else:
                        territory_dict[Define.BUILDING_TYPE_LABORATORY] = self.check_wait_building(account.account_uid, building.uid)

                elif building.building_type == Define.BUILDING_TYPE_FOOD_STORAGE:
                    territory_dict[Define.BUILDING_TYPE_FOOD_STORAGE] = self.get_storage_max(building, territory_dict)

                elif building.building_type == Define.BUILDING_TYPE_IRON_STORAGE:
                    territory_dict[Define.BUILDING_TYPE_IRON_STORAGE] = self.get_storage_max(building, territory_dict)

                elif building.building_type == Define.BUILDING_TYPE_STONE_STORAGE:
                    territory_dict[Define.BUILDING_TYPE_STONE_STORAGE] = self.get_storage_max(building, territory_dict)

                elif building.building_type == Define.BUILDING_TYPE_WOOD_STORAGE:
                    territory_dict[Define.BUILDING_TYPE_WOOD_STORAGE] = self.get_storage_max(building, territory_dict)

                elif building.building_type == Define.BUILDING_TYPE_TRADE_SHIP:
                    if 0 != building.level:
                        territory_dict[Define.BUILDING_TYPE_TRADE_SHIP] = {building.uid : building.level}
                    else:
                        territory_dict[Define.BUILDING_TYPE_TRADE_SHIP] = {building.uid : self.check_wait_building(account.account_uid, building.uid)}

                elif building.building_type == Define.BUILDING_TYPE_WORKSHOP:
                    if 0 != building.level:
                        territory_dict[Define.BUILDING_TYPE_WORKSHOP] = {building.uid : building.level}
                    else:
                        territory_dict[Define.BUILDING_TYPE_WORKSHOP] = {building.uid : self.check_wait_building(account.account_uid, building.uid)}

                slot_count = 0
                addHeroSlot = {}
                addHeroSlot['formation'] = 1
                db_info = self.w_db['heroinven'].select_all_item(account.account_uid)
                for hero in db_info:
                    if slot_count == 5:
                        break

                    initHeroRedisData(slot_count, addHeroSlot)

                    slot_count += 1

            start_hero = '{}'
            self.cache.set_user_profile(
                user_id=account.account_uid,
                nickname=account.nick_name,
                last_login=str(account.last_login),
                team_info=str(addHeroSlot),
                level=1,
                exp=0,
                territory_dict=str(territory_dict),
                start_hero=start_hero
            )

            redis_data[GAMECOMMON.R_USER_GUILD_UID] = userinfo.guild_uid
            self.cache.set_user_info_dict(account.account_uid, redis_data)
            self.update_progress(i + 1, total_count)

    def recovery_guild_info_cache(self):
        guild_list = self.w_db["guild"].select_guild_all()
        for i, guild in enumerate(guild_list):
            db_guild_info = self.w_db['guildinfo'].find_guild(guild.guild_uid)
            if not db_guild_info:
                continue

            self.guild.insert_guild_info(
                guild.guild_uid,
                guild.guild_name,
                guild.guild_master,
                guild.guild_bg,
                guild.guild_emblem,
                db_guild_info.join_type,
                db_guild_info.join_level,
                db_guild_info.guild_msg
            )

            member_cnt = self.w_db['guildmember'].guild_member_count(db_guild_info.guild_uid)
            UpdateGuildMemberCount(self, db_guild_info.guild_uid, member_cnt)

    def recovery_guild_uid(self):
        account_list = self.w_db['account'].select_all_account()
        total_count = len(account_list)
        print(datetime.now(), "start recovery_guild_uid total_count:" + str(total_count))
        printProgressBar(0, total_count, prefix = 'Progress:', suffix = 'Complete', length = 20)

        for i, account in enumerate(account_list):
            db_update = []
            value_list = []

            db_update.append('guild_uid')
            value_list.append(0)

            if self.userid == None:
                sys.stdout.write("(null)")
            else:
                self.w_db['profile'].update_user_column(self.userid, db_update, value_list)

            self.update_progress(i + 1, total_count)


        guild_list = self.w_db["guild"].select_guild_all()
        total_count = len(guild_list)
        print(datetime.now(), "start select_guild_all total_count:" + str(total_count))
        printProgressBar(0, total_count, prefix = 'Progress:', suffix = 'Complete', length = 20)

        for i, guild in enumerate(guild_list):
            self.w_db['profile'].guild_join(guild.guild_master, guild.guild_uid)
            redis_data = {}
            redis_data[GAMECOMMON.R_USER_GUILD_UID] = guild.guild_uid
            redis_data[GAMECOMMON.R_USER_GUILD_GRADE] = int(Define.GUILD_GRADE_MASTER)
            self.cache.set_user_info_dict(guild.guild_master, redis_data)

            db_guild_member = self.w_db['guildmember'].guild_member_all(guild.guild_uid)
            for member in db_guild_member:
                if member.auid == guild.guild_master:
                    self.w_db['guildmember'].add_guild_member(guild.guild_uid, guild.guild_master, Define.GUILD_GRADE_MASTER)
                else:
                    member_redis = {}
                    if member.guild_grade > Define.GUILD_GRADE_MEMBER:
                        member_redis[GAMECOMMON.R_USER_GUILD_GRADE] = member.guild_grade
                        self.cache.set_user_info_dict(member.auid, redis_data)
                        continue

                    self.w_db['profile'].guild_join(member.auid, guild.guild_uid)
                    member_redis[GAMECOMMON.R_USER_GUILD_UID] = guild.guild_uid
                    member_redis[GAMECOMMON.R_USER_GUILD_GRADE] = member.guild_grade
                    self.cache.set_user_info_dict(member.auid, redis_data)

            self.update_progress(i + 1, total_count)


    def check_wait_building(self, auid, uid):
        wait_build = self.w_db['territorybuild'].find_territory_build(auid, uid)
        return wait_build.build_level-1

    def get_storage_max(self, db_info, redis_data):
        build_info_dict = self.table.build_create[db_info.building_type]
        if not build_info_dict:
            return 0

        build_level = db_info.level
        if 0 >= db_info.level:
            build_level = self.check_wait_building(db_info.auid, db_info.uid)

        build_material = build_info_dict[build_level]
        if not build_material:
            return 0

        addStorageMax = redis_data[db_info.building_type] + build_material.capacity
        return addStorageMax


if __name__ == '__main__':
    conf_dir = os.path.dirname(os.path.abspath(__file__)) + "/conf/"
    servive_ini = conf_dir + str("service_local.ini")
    print("conf_dir:", conf_dir)
    print("servive_ini:", servive_ini)

    context = GameServerContext(
        inifile=servive_ini,
        after_init=init_callback
    )

    service = RedisInitialize(context)
    service.redis_flush()
    service.recovery_guild_uid()
    service.recovery_guild_info_cache()
    service.total_account()