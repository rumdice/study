# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


def getRaidTicket(self, userinfo, ticket_max, increase_ticket):
    add_ticket = 0
    ticket_time = userinfo.guild_raid_ticket_time
    raid_charge_time = int(self.table.const_info.get(GAMECOMMON.RAID_CHARGE_TIME).value)
    
    if userinfo.guild_raid_ticket < ticket_max:
        if userinfo.guild_raid_ticket_time:
            interval = self.begin - userinfo.guild_raid_ticket_time
            add_ticket = int(interval.seconds / raid_charge_time)
            if add_ticket > 0:
                add_time = timedelta(seconds = add_ticket * raid_charge_time)
                ticket_time = userinfo.guild_raid_ticket_time + add_time
        else:
            ticket_time = self.begin
    
    total_ticket= int(userinfo.guild_raid_ticket + add_ticket + increase_ticket)
    if total_ticket >= ticket_max:
        ticket_time = None

    if total_ticket >= ticket_max:
        ticket_time = None

    return (total_ticket, ticket_time)


def raidMonsterReward(self, db_guild):
    boss_info_list = self.table.raid_monster.get(db_guild.raid_element, None)
    if not boss_info_list:
        self.logger.error("raid monster element is null:{}".format(db_guild.raid_element))
        return

    boss_info = boss_info_list[0]
    for boss in boss_info_list:
        if boss.boss_id == db_guild.raid_monster:
            boss_info = boss
            break

    boss_data = self.table.hero.get(boss_info.boss_id, None)
    if not boss_data:
        self.logger.error("not find raid monster:{}".format(boss_info.boss_id))
        return

    boss_class_stat_const = self.table.raid_const_stat.get(boss_data.jclass, None)
    if not boss_class_stat_const:
        self.logger.error("not find raid monster:{}".format(boss_data.jclass))
        return

    boss_maxhp = boss_data.hp + (boss_class_stat_const.hp * (db_guild.raid_monster_level - 1))

    member_damage_list = self.w_db['guildraiddamage'].get_guild_damage_list(db_guild.guild_uid)
    ranking = [[0, 0], [0, 0], [0, 0]]
    for member in member_damage_list:
        if 0 >= member.total_damage:
            self.w_db['guildmember'].guild_raid_reward_grade(db_guild.guild_uid, member.auid, 7, 0)
            continue

        for index, rank in enumerate(ranking):
            if rank[1] < member.total_damage:
                ranking[index] = [member.auid, member.total_damage]
                break

        db_member = self.w_db['guildmember'].get_guild_member(db_guild.guild_uid, member.auid)
        if not db_member:
            continue

        redis_info = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_CHECK_UPDATE)
        if redis_info:
            check_list = convert_string_to_array(redis_info)
            check_list[GAMECOMMON.UPDATE_GUILD_RAID] = 1
            self.cache.set_user_info(member.auid, GAMECOMMON.R_USER_CHECK_UPDATE, str(check_list))

        reward_grade = len(self.table.raid_damage)
        percent = int(member.total_damage / boss_maxhp * 100)

        for damage_grade in self.table.raid_damage:
            if damage_grade.rank > 0:
                index = 0
                for rank in ranking:
                    index += 1
                    if rank[0] == member.auid:
                        reward_grade = index
                        break
            else:
                reward_grade = damage_grade.grade

            self.w_db['guildmember'].guild_raid_reward_grade(db_guild.guild_uid, member.auid, reward_grade, member.total_damage)
            break

    self.w_db['guildraidresult'].update_raid_result(
        db_guild.guild_uid,
        db_guild.raid_monster,
        db_guild.raid_element,
        0,
        db_guild.raid_monster_level,
        str(ranking)
    )

    return



class ServiceGuildRaid(object):
    def GuildRaidInfo(self, response):
        raid_end_hour = int(self.table.const_info.get(GAMECOMMON.RAID_END_HOUR).value)

        db_info = self.w_db['profile'].select_column(self.userid, "guild_uid")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        db_grade = self.w_db['profile'].select_column(self.userid, "guild_grade")
        if db_grade.guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        db_guild_member = self.w_db['guildmember'].get_guild_member(db_info.guild_uid, self.userid)
        if not db_guild_member:
            response.result = Response.NOT_IN_GUILD
            return

        if self.begin.hour == raid_end_hour:
            # 00:00 ~ 00:30
            if 30 < self.begin.minute:
                response.guild_raid_info.element = 0
                response.guild_raid_info.boss_id = 0
                response.guild_raid_info.boss_level = 0
                response.guild_raid_info.cur_hp = 0
                response.guild_raid_info.remain_time = (60 - self.begin.minute) * 60
                response.result = Response.SUCCESS
                return

        db_guild = self.w_db['guildinfo'].find_guild(db_info.guild_uid)
        if not db_guild:
            response.result = Response.GUILD_DO_NOT_EXIST
            return

        response.guild_raid_info.element = db_guild.raid_element
        response.guild_raid_info.boss_id = db_guild.raid_monster
        response.guild_raid_info.boss_level = db_guild.raid_monster_level
        response.guild_raid_info.cur_hp = db_guild.raid_monster_hp
        end_time = datetime(self.begin.year, self.begin.month, self.begin.day, raid_end_hour)
        response.guild_raid_info.remain_time = calc_time_to_seconds(self.begin, end_time)
        response.result = Response.SUCCESS
        return

    def GuildRaidStart(self, response):
        raid_end_hour = int(self.table.const_info.get(GAMECOMMON.RAID_END_HOUR).value)

        if self.begin.hour == raid_end_hour:
            response.result = Response.GUILD_RAID_TIME_OVER
            return

        db_info = self.w_db['profile'].select_column(self.userid, "guild_uid, guild_raid_ticket, guild_raid_ticket_time")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        db_grade = self.w_db['profile'].select_column(self.userid, "guild_grade")
        if db_grade.guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        db_guild = self.w_db['guildinfo'].find_guild(db_info.guild_uid)
        if not db_guild:
            response.result = Response.GUILD_DO_NOT_EXIST
            return

        if 0 >= db_guild.raid_monster_hp:
            response.result = Response.GUILD_RAID_CLOSE
            return

        raid_ticket_max = int(self.table.const_info.get(GAMECOMMON.RAID_TICKET_MAX).value)
        raid_charge_time = int(self.table.const_info.get(GAMECOMMON.RAID_CHARGE_TIME).value)
        ticket, ticket_time = getRaidTicket(self, db_info, raid_ticket_max, 0)
        update_ticket = ticket - 1
        if 0 > update_ticket:
            response.result = Response.LACK_GUILD_RAID_TICKET
            return

        if not ticket_time:
            ticket_time = self.begin

        db_update = []
        value_list = []

        db_update.append('last_mode')
        value_list.append(GAMECOMMON.PLAY_MODE_GUILD_RAID)

        db_update.append('guild_raid_ticket')
        value_list.append(update_ticket)

        str_column = "guild_raid_ticket_time=NULL"
        response.guild_raid_start.raid_ticket_time = 0
        if ticket_time != None:
            str_column = "guild_raid_ticket_time='%s'" % (ticket_time)
            response.guild_raid_start.raid_ticket_time = self.next_charge_second(ticket_time, raid_charge_time)

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list, str_column)
        self.w_db['guildmember'].guild_raid_start(db_info.guild_uid, self.userid, self.begin)

        response.guild_raid_start.raid_ticket = update_ticket
        response.result = Response.SUCCESS
        return

    def GuildRaidEnd(self, request, response):
        if request.guild_raid_end.damage <= 0:
            response.result = Response.SUCCESS
            return

        db_info = self.w_db['profile'].select_column(self.userid, "guild_uid, last_mode")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        if db_info.last_mode != GAMECOMMON.PLAY_MODE_GUILD_RAID:
            response.result = Response.LAST_PLAY_MODE_WRONG
            return

        db_grade = self.w_db['profile'].select_column(self.userid, "guild_grade")
        if db_grade.guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        db_guild = self.w_db['guildinfo'].find_guild(db_info.guild_uid)
        if not db_guild:
            response.result = Response.GUILD_DO_NOT_EXIST
            return

        raid_monster_data = self.table.raid_monster[db_guild.raid_element]
        boss_hp = 0
        for boss in raid_monster_data:
            if boss.boss_id == db_guild.raid_monster:
                boss_data = self.table.hero.get(boss.boss_id, None)
                if not boss_data:
                    self.logger.error("not find raid monster hero_list:{}".format(boss.boss_id))
                    return
                boss_class_stat_const = self.table.raid_const_stat.get(boss_data.jclass, None)
                if not boss_class_stat_const:
                    self.logger.error("not find boss_class_stat_const:{}".format(boss_data.jclass))
                    return

                boss_hp = int(boss_data.hp + (boss_class_stat_const.hp * (db_guild.raid_monster_level - 1)))
                break

        total_damage = self.w_db['guildraiddamage'].get_guild_total_damage(db_info.guild_uid)
        if not total_damage:
            total_damage = 0

        if total_damage >= boss_hp:
            response.result = Response.SUCCESS
            return

        boss_hp -= int(total_damage + request.guild_raid_end.damage)
        if 0 >= boss_hp:
            boss_hp = 0

        db_raid_damage = self.w_db['guildmember'].get_guild_member(db_info.guild_uid, self.userid)
        if not db_raid_damage:
            response.result = Response.NOT_IN_GUILD
            return

        damage_record = convert_string_to_array(db_raid_damage.raid_record)
        damage_record.append([str(self.begin), request.guild_raid_end.damage])

        self.w_db['guildmember'].update_guild_raid_record(db_info.guild_uid, self.userid, str(damage_record))
        self.w_db['guildraiddamage'].add_guild_raid_damage(db_info.guild_uid, self.userid, request.guild_raid_end.damage)
        ret = self.w_db['guildinfo'].update_raid_monster_hp(db_info.guild_uid, int(boss_hp))

        if 0 >= boss_hp and ret:
            raidMonsterReward(self, db_guild)

        response.guild_raid_end.boss_hp = boss_hp
        response.result = Response.SUCCESS
        return

    def GuildRaidDamageList(self, response):
        db_info = self.w_db['profile'].select_column(self.userid, "guild_uid")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        damage_list = self.w_db['guildraiddamage'].get_guild_damage_list(db_info.guild_uid)
        if 1 > len(damage_list):
            response.guild_raid_damage_list.CopyFrom(Response.GuildRaidDamageList())
            response.result = Response.SUCCESS
            return

        for member in damage_list:
            add_member = response.guild_raid_damage_list.guild_member.add()
            add_member.member_name = ""
            add_member.avatar_id = 0
            member_redis = self.cache_clone.get_user_profile(member.auid)
            if member_redis:
                add_member.member_name = member_redis[GAMECOMMON.R_USER_NICK]
                add_member.avatar_id = int(member_redis[GAMECOMMON.R_USER_AVATAR_ID])
                add_member.level = int(member_redis[GAMECOMMON.R_USER_LEVEL])

            add_member.raid_damage = member.total_damage

        response.result = Response.SUCCESS
        return

    def GuildRaidReward(self, response):
        db_info = self.w_db['profile'].select_column(self.userid, "guild_uid")
        if not db_info:
            response.result = Response.USER_DB_NOT_EXIST
            return

        if db_info.guild_uid <= 0:
            response.result = Response.NOT_IN_GUILD
            return

        db_member = self.w_db['guildmember'].get_guild_member(db_info.guild_uid, self.userid)
        if not db_member:
            response.result = Response.NOT_IN_GUILD
            return

        if db_member.reward_flag:
            response.guild_raid_reward.CopyFrom(Response.GuildRaidReward())
            response.result = Response.SUCCESS
            return

        if db_member.reward_grade <= 0:
            response.guild_raid_reward.CopyFrom(Response.GuildRaidReward())
            response.result = Response.SUCCESS
            return

        db_result = self.w_db['guildraidresult'].find_raid_result(db_info.guild_uid)
        if not db_result:
            response.guild_raid_reward.CopyFrom(Response.GuildRaidReward())
            response.result = Response.DB_NOT_EXIST
            return

        grade_reward_list = []
        if 0 < db_result.monster_hp:
            grade_reward_list = self.table.raid_fail_reward[db_result.monster_level - 1]
        else:
            grade_reward_list = self.table.raid_win_reward[db_result.monster_level - 1]

        response.guild_raid_reward.element = db_result.element
        response.guild_raid_reward.boss_id = db_result.raid_monster
        response.guild_raid_reward.boss_level = db_result.monster_level
        response.guild_raid_reward.cur_hp = db_result.monster_hp
        response.guild_raid_reward.reward_grade = db_member.reward_grade
        response.guild_raid_reward.damage = db_member.reward_damage
        
        damage_rank = convert_string_to_array(db_result.damage_record)
        for rank in damage_rank:
            damageInfo = response.guild_raid_reward.damage_list.add()
            damageInfo.name = ""
            r_user_name = self.cache_clone.get_user_data(rank[0], GAMECOMMON.R_USER_NICK)
            if r_user_name:
                damageInfo.name = r_user_name
            damageInfo.damage = int(rank[1])

        item_dict = {}
        reward_info = grade_reward_list[db_member.reward_grade - 1]
        reward_set = self.table.reward_set[reward_info.reward_set]
        for i in range(reward_info.count):
            for group in reward_set:
                self.table.get_reward_prob_item(group, item_dict)

        self.w_db['guildmember'].guild_raid_reward(db_info.guild_uid, self.userid)
        self.reward_packet_process(
            item_dict,
            response.guild_raid_reward.reward_item
        )

        response.result = Response.SUCCESS

        self.w_db['guildmember'].guild_raid_reward_grade(db_info.guild_uid, self.userid, 0, 0)
        r_update_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_CHECK_UPDATE)
        update_list = convert_string_to_array(r_update_data)
        update_list[GAMECOMMON.UPDATE_GUILD_RAID] = False
        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_CHECK_UPDATE, str(update_list))
        return