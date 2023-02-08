# -*- coding: utf-8 -*-
import csv
import os
from datetime import datetime

from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.context import *
from src.services.service_common import *
from src.tables.table_Base import *


class RaidRewardService():
    def __init__(self, context):
        self.context = context
        self.table = TableBase()
        self.w_db = context.w_db
        self.cache = context.cache
        self.cache_clone = context.cache_clone

    def redis_flush(self):
        for i in range(10):
            self.w_db['guildraiddamage'].guild_damage_reset(i)

    # def raid_win_process(self, guild_uid, boss_maxhp):
    #     member_damage_list = self.w_db['guildraiddamage'].get_guild_damage_list(guild_uid)
    #     ranking = [[0, 0], [0, 0], [0, 0]]
    #     member_grade_dict = {}
    #     for member in member_damage_list:
    #         for index, rank in enumerate(ranking):
    #             if rank[1] < member.total_damage:
    #                 ranking.insert(index, [member.auid, member.total_damage])
    #                 break
    #
    #         if 3 < len(ranking):
    #             del ranking[3]
    #
    #         db_member = self.w_db['guildmember'].get_guild_member(guild_uid, member.auid)
    #         if not db_member:
    #             continue
    #
    #         grade = 7
    #         percent = int(member.total_damage / boss_maxhp * 100)
    #         for damage_grade in self.table.raid_damage:
    #             if damage_grade.win_damage_min <= percent and percent <= damage_grade.win_damage_max:
    #                 member_grade_dict[member.auid] = damage_grade.grade
    #                 break
    #
    #     for rank, rankinfo in enumerate(ranking):
    #         rank_user = member_grade_dict.get(rankinfo[0], None)
    #         if not rank_user:
    #             continue
    #
    #         if rank_user == 4:
    #             member_grade_dict[rankinfo[0]] = rank+1


    def raid_fail_process(self, db_guildinfo, boss_maxhp):
        member_damage_list = self.w_db['guildraiddamage'].get_guild_damage_list(db_guildinfo.guild_uid)
        ranking = [[0, 0], [0, 0], [0, 0]]
        for member in member_damage_list:
            if member.total_damage <= 0:
                self.w_db['guildmember'].guild_raid_reward_grade(db_guildinfo.guild_uid, member.auid, 0)
                continue

            for index, rank in enumerate(ranking):
                if rank[1] < member.total_damage:
                    ranking[index] = [member.auid, member.total_damage]
                    break

            db_member = self.w_db['guildmember'].get_guild_member(db_guildinfo.guild_uid, member.auid)
            if not db_member:
                continue

            redis_info = self.cache_clone.get_user_data(member.auid, GAMECOMMON.R_USER_CHECK_UPDATE)
            if redis_info:
                check_list = convert_string_to_array(redis_info)
                check_list[GAMECOMMON.UPDATE_GUILD_RAID] = 1
                self.cache.set_user_info(member.auid, GAMECOMMON.R_USER_CHECK_UPDATE, str(check_list))

            reward_grade = 7
            percent = int(member.total_damage / boss_maxhp * 100)
            for damage_grade in self.table.raid_damage:
                print("damage_grade.fail_damage_min:", damage_grade.fail_damage_min)
                if damage_grade.fail_damage_min <= percent:
                    if damage_grade.rank > 0:
                        index = 0
                        for rank in ranking:
                            index += 1
                            if rank[0] == member.auid:
                                reward_grade = index
                                break
                    else:
                        reward_grade = damage_grade.grade
                    self.w_db['guildmember'].guild_raid_reward_grade(db_guildinfo.guild_uid, member.auid, reward_grade, member.total_damage)
                    break

        self.w_db['guildraidresult'].update_raid_result(
            db_guildinfo.guild_uid,
            db_guildinfo.raid_monster,
            db_guildinfo.raid_element,
            db_guildinfo.raid_monster_hp,
            db_guildinfo.raid_monster_level,
            str(ranking)
        )

    def clear_record_process(self, db_guildinfo):
        print("clear_record_process")
        db_member_list = self.w_db['guildmember'].guild_member_all(db_guildinfo.guild_uid)
        for member in db_member_list:
            self.w_db['guildmember'].guild_raid_record_clear(db_guildinfo.guild_uid, member.auid)

    def regen_raid_monster(self, guild_uid, win_flag, win_count, cur_level, cur_element):
        element = cur_element + 1

        if len(self.table.raid_monster) < element:
            element = 1

        if win_flag:
            win_count += 1
        else:
            win_count = 0

        if win_count == 2:
            cur_level += 1
            win_count = 0
        elif win_flag == False:
            cur_level -= 1

        if 1 > cur_level:
            cur_level = 1

        if 15 < cur_level:
            cur_level = 15


        element_boss = self.table.raid_monster[element]
        rand = random.Random()
        boss_info = element_boss[rand.randint(0, len(element_boss)-1)]
        boss_data = self.table.hero.get(boss_info.boss_id, None)
        if not boss_data:
            self.logger.error("not find raid monster :{}".format(boss_info.boss_id))
            return
        boss_class_stat_const = self.table.raid_const_stat.get(boss_data.jclass, None)
        if not boss_class_stat_const:
            self.logger.error("not find boss_class_stat_const:{}".format(boss_data.jclass))
            return

        boss_hp = int(boss_data.hp + (boss_class_stat_const.hp * (cur_level - 1)))
        self.w_db['guildinfo'].regen_raid_monster(guild_uid, element, boss_info.boss_id, boss_hp, cur_level, win_count)
        return


    def raid_process(self):
        guild_list = self.w_db['guild'].select_guild_all()
        total_count = len(guild_list)
        print(datetime.now(), "start guild raid / " + str(total_count))

        for i, guild in enumerate(guild_list):
            print("guild.guild_uid:", guild.guild_uid)
            db_guildinfo = self.w_db['guildinfo'].find_guild(guild.guild_uid)
            if not db_guildinfo:
                continue

            print("db_guildinfo.raid_monster_hp:", db_guildinfo.raid_monster_hp)
            if 0 >= db_guildinfo.raid_monster_hp:
                self.regen_raid_monster(
                    guild.guild_uid,
                    True,
                    db_guildinfo.raid_complete_count,
                    db_guildinfo.raid_monster_level,
                    db_guildinfo.raid_element
                )
                continue

            boss_info_list = self.table.raid_monster.get(db_guildinfo.raid_element, None)
            if not boss_info_list:
                print("!! not boss_info_list")
                print("db_guildinfo.raid_element:", db_guildinfo.raid_element)
                print("self.table.raid_monster:", self.table.raid_monster)
                boss_info_list = self.table.raid_monster[1]
            print("boss_info_list:", boss_info_list)

            boss_info = boss_info_list[0]
            for boss in boss_info_list:
                if boss.boss_id == db_guildinfo.raid_monster:
                    boss_info = boss
                    break
            print("boss_info:", boss_info)

            boss_data = self.table.hero.get(boss_info.boss_id, None)
            if not boss_data:
                print("!! not boss_data")
                self.logger.error("not find raid monster :{}".format(boss_info.boss_id))
                return
            print("boss_data:", boss_data)

            boss_class_stat_const = self.table.raid_const_stat.get(boss_data.jclass, None)
            if not boss_class_stat_const:
                print("!! not boss_class_stat_const")
                self.logger.error("not find raid monster :{}".format(boss_data.jclass))
                return
            print("boss_class_stat_const:", boss_class_stat_const)

            boss_maxhp = boss_data.hp + boss_class_stat_const.hp * (db_guildinfo.raid_monster_level - 1)
            print("boss_maxhp:",  boss_maxhp)
            print("boss_data.hp:",  boss_data.hp)
            print("boss_class_stat_const.hp:",  boss_class_stat_const.hp)
            print("db_guildinfo.raid_monster_level:",  db_guildinfo.raid_monster_level)

            if 0 < db_guildinfo.raid_monster_hp:
                print("raid_fail_process main")
                self.raid_fail_process(db_guildinfo, boss_maxhp)

            print("clear_record_process main")
            self.clear_record_process(db_guildinfo)
            self.regen_raid_monster(
                guild.guild_uid,
                False,
                db_guildinfo.raid_complete_count,
                db_guildinfo.raid_monster_level,
                db_guildinfo.raid_element
            )


conf_dir = os.path.dirname(os.path.abspath(__file__)) + "/conf/"
service_ini = conf_dir + "service_local.ini"

if __name__ == '__main__':
    context = GameServerContext(
        inifile=service_ini,
        after_init=init_callback
    )

    service = RaidRewardService(context)
    service.raid_process()
    service.redis_flush()
