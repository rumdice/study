# -*- coding: utf-8 -*-
import re

from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


def getGuildInfoType(self, get_info):
    if Define.GUILD_INFO_JOINED == get_info.get_type:
        db_profile = self.w_db['profile'].select_column(self.userid, "guild_uid")
        if not db_profile:
            return None

        return db_profile.guild_uid
    elif Define.GUILD_INFO_NAME == get_info.get_type:
        return self.guild_clone.get_guild_info_name(get_info.guild_name)
    else:
        return get_info.guild_uid


def getGuildSearchList(self, search_key):
    limit_count = int(self.table.const_info.get(GAMECOMMON.GUILD_LIMIT_COUNT).value)
    choice_count = int(self.table.const_info.get(GAMECOMMON.GUILD_CHOICE_COUNT).value)
    db_guild_list = self.w_db['guild'].get_guild_search_list(limit_count, search_key)
    guilds_count = len(db_guild_list)
    if choice_count < guilds_count:
        choice_guild_list = random.sample(db_guild_list, choice_count)
    else:
        choice_guild_list = db_guild_list
    result_list = []
    for guild in choice_guild_list:
        result_list.append(guild.guild_uid)
    return result_list


def getGuildRecommendList(self):
    limit_count = int(self.table.const_info.get(GAMECOMMON.GUILD_LIMIT_COUNT).value)
    choice_count = int(self.table.const_info.get(GAMECOMMON.GUILD_CHOICE_COUNT).value)
    db_guild_list = self.w_db['guild'].get_guild_recommend_list(limit_count)
    guilds_count = len(db_guild_list)
    if choice_count < guilds_count:
        choice_guild_list = random.sample(db_guild_list, choice_count)
    else:
        choice_guild_list = db_guild_list
    result_list = []
    for guild in choice_guild_list:
        result_list.append(guild.guild_uid)
    return result_list


def CreateGuildRaidMonster(self):
    element_boss = self.table.raid_monster[1]
    rand = random.Random()
    boss_info = element_boss[rand.randint(0, len(element_boss)-1)]
    boss_data = self.table.hero.get(boss_info.boss_id)
    boss_hp = boss_data.hp
    return boss_info.boss_id, boss_hp


def guildMasterWithDraw(self, db_guild):
    member_cnt = self.w_db['guildmember'].guild_member_count(db_guild.guild_uid)
    db_members = self.w_db['guildmember'].second_master_list(db_guild.guild_uid)

    if member_cnt == 1:
        # guildDelete(self, self.user_id, db_guild.guild_uid, db_members)
        guildDisable(self, self.userid, db_members)
        return

    if not db_members:
        db_members = self.w_db['guildmember'].guild_member_all(db_guild.guild_uid)
        if not db_members:
            # guildDelete(self, self.user_id, db_guild.guild_uid, db_members)
            guildDisable(self, self.userid, db_members)
            return

    guildMasterChange(self, db_guild, db_members)


def guildMasterChange(self, db_guild, db_members):
    master_member = None

    for member in db_members:
        if member.auid == self.userid:
            continue
        if member.guild_grade > Define.GUILD_GRADE_SECOND_MASTER:
            continue

        member_db = self.w_db['account'].find_user_id(member.auid)
        if not member_db:
            continue
        if time_diff_in_day(member_db.last_login) < -8:
            continue

        master_member = member

    if not master_member :
        for member in db_members:
            if member.auid == self.userid:
                continue
            if member.guild_grade == Define.GUILD_GRADE_SECOND_MASTER:
                continue
            if member.guild_grade >= Define.GUILD_GRADE_WAIT:
                continue

            member_db = self.w_db['account'].find_user_id(member.auid)
            if not member_db:
                continue
            if time_diff_in_day(member_db.last_login) < -8:
                continue

            master_member = member
            break

    if not master_member:
        # guildDelete(self, self.user_id, db_guild.guild_uid, db_members)
        guildDisable(self, self.userid, db_members)
        return

    self.w_db['guildmember'].guild_master_delete(master_member.guild_uid) # delete befor master
    self.w_db['guildmember'].add_guild_member(master_member.guild_uid, master_member.auid, Define.GUILD_GRADE_MASTER)

    master_redis = self.cache_clone.get_user_profile(self.userid)
    if master_redis:
        master_redis[GAMECOMMON.R_USER_GUILD_UID] = 0
        master_redis[GAMECOMMON.R_USER_GUILD_GRADE] = Define.GUILD_GRADE_NONE
        self.cache.set_user_info_dict(self.userid, master_redis)
        self.w_db['profile'].withdraw_guild(self.userid, self.begin)

    redis_data = {}
    redis_data[GAMECOMMON.R_USER_GUILD_GRADE] = Define.GUILD_GRADE_MASTER
    self.cache.set_user_info_dict(master_member.auid, redis_data)

    guild_data = {}
    guild_data[GAMECOMMON.GUILD_MASTER_UID] = master_member.auid
    guild_data[GAMECOMMON.GUILD_MEMBER_COUNT] = db_guild.member_count-1
    self.guild.update_guild_info_dict(db_guild.guild_uid, guild_data)

    self.w_db['guild'].change_master(db_guild.guild_uid, master_member.auid)
    self.w_db['guildinfo'].update_member_count(db_guild.guild_uid, db_guild.member_count-1)
    return


def guildDelete(self, master_uid, guild_uid, db_members):
        redis_data = {}
        master_redis = self.cache_clone.get_user_profile(master_uid)
        if master_redis:
            redis_data[GAMECOMMON.R_USER_GUILD_UID] = 0
            redis_data[GAMECOMMON.R_USER_GUILD_GRADE] = Define.GUILD_GRADE_NONE
            self.cache.set_user_info_dict(master_uid, redis_data)
            self.w_db['profile'].withdraw_guild(master_uid, self.begin)

        for member in db_members:
            if member.auid == master_uid:
                continue
            self.w_db['profile'].guild_out(member.auid)

        self.w_db['guildmember'].del_guild_member_all(guild_uid)
        self.w_db['guild'].delete_guild(guild_uid)
        self.w_db['guildinfo'].del_guild_info(guild_uid)
        self.w_db['guildraidresult'].del_raid_result(guild_uid)
        self.guild.del_guild_info(guild_uid)
        return


def guildDisable(self, master_uid, db_members):
    redis_data = {}
    master_redis = self.cache_clone.get_user_profile(master_uid)
    if master_redis:
        redis_data[GAMECOMMON.R_USER_GUILD_UID] = 0
        redis_data[GAMECOMMON.R_USER_GUILD_GRADE] = Define.GUILD_GRADE_NONE
        self.cache.set_user_info_dict(master_uid, redis_data)
        self.w_db['profile'].withdraw_guild(master_uid, self.begin)

    for member in db_members:
        if member.auid == master_uid:
            continue
        self.w_db['profile'].guild_out(member.auid)
    return


def UpdateGuildMemberCount(self, guild_uid, member_count):
    self.w_db['guildinfo'].update_member_count(guild_uid, member_count)
    self.guild.update_guild_info(guild_uid, GAMECOMMON.GUILD_MEMBER_COUNT, member_count)
    return


class ServiceGuild(object):
    def GuildCreate(self, request, response):
        db_info = self.w_db['profile'].select_column(self.userid, "cash, guild_uid, level")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        if 0 < db_info.guild_uid:
            response.result = Response.MEMBER_OF_THE_GUILD
            return

        guild_create_cash = int(self.table.const_info.get(GAMECOMMON.GUILD_CREATE).value)
        update_cash = db_info.cash - guild_create_cash
        if 0 > update_cash:
            response.result = Response.CASH_LACK
            return

        guild_unlock_lv = int(self.table.const_info.get(GAMECOMMON.GUILD_UNLOCK).value)
        if db_info.level < guild_unlock_lv:
            response.result = Response.CONTENT_LEVEL_LACK 
            return

        pattern = re.compile(r'\s+')
        sentence = re.sub(pattern, '', request.guild_create.create_info.guild_name)

        guild_name_min = int(self.table.const_info.get(GAMECOMMON.MIN_LENGTH_GUILD_NAME).value)
        guild_name_max = int(self.table.const_info.get(GAMECOMMON.MAX_LENGTH_GUILD_NAME).value)

        if guild_name_min > len(sentence.encode('euc-kr')):
            response.result = response.INVALID_GUILD_NAME
            return

        if guild_name_max < len(sentence.encode('euc-kr')):
            response.result = response.INVALID_GUILD_NAME
            return

        try:
            guild_uid = self.w_db['guild'].add_guild(
                sentence,
                self.userid,
                request.guild_create.create_info.guild_bg,
                request.guild_create.create_info.guild_emblem,
                self.begin
            )
        except Exception as e:
            self.logger.exception(e.message)
            response.result = Response.EXIST_GUILD_NAME
            return

        boss_id, boss_hp = CreateGuildRaidMonster(self)
        try:
            self.w_db['guildinfo'].add_guild_info(
                guild_uid,
                request.guild_create.create_info.join_level,
                int(request.guild_create.create_info.join_type),
                request.guild_create.create_info.guild_msg,
                1,
                boss_id,
                boss_hp
            )
        except Exception as e:
            self.logger.exception(e.message)
            self.w_db['guild'].delete_guild(guild_uid)
            response.result = Response.DB_SYSTEM_ERROR
            return

        self.w_db['guildraidresult'].add_raid_result(guild_uid)
        try:
            self.w_db['guildmember'].add_guild_member(guild_uid, self.userid, Define.GUILD_GRADE_MASTER)
        except Exception as e:
            self.logger.exception(e.message)
            self.w_db['guild'].delete_guild(guild_uid)
            self.w_db['guildinfo'].delete_guild(guild_uid)
            response.result = Response.DB_SYSTEM_ERROR
            return

        self.guild.insert_guild_info(
            guild_uid,
            request.guild_create.create_info.guild_name,
            self.userid,
            request.guild_create.create_info.guild_bg,
            request.guild_create.create_info.guild_emblem,
            int(request.guild_create.create_info.join_type),
            request.guild_create.create_info.join_level,
            request.guild_create.create_info.guild_msg
        )

        update_redis = {
            GAMECOMMON.R_USER_GUILD_UID: guild_uid,
            GAMECOMMON.R_USER_GUILD_GRADE: Define.GUILD_GRADE_MASTER
        }
        self.cache.set_user_info_dict(self.userid, update_redis)

        db_update = []
        value_list = []
        
        db_update.append('cash')
        value_list.append(update_cash)

        db_update.append('guild_uid')
        value_list.append(guild_uid)

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list)

        response.result = Response.SUCCESS
        return

    def GuildJoin(self, request, response):
        db_profile = self.w_db['profile'].select_column(self.userid, "level, guild_uid, guild_withdraw_time")
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        if 0 < db_profile.guild_uid:
            response.result = Response.MEMBER_OF_THE_GUILD
            return

        guild_unlock_lv = int(self.table.const_info.get(GAMECOMMON.GUILD_UNLOCK).value)
        if db_profile.level < guild_unlock_lv:
            response.result = Response.CONTENT_LEVEL_LACK 
            return

        db_guild = self.w_db['guildinfo'].find_guild(request.guild_join.guild_uid)
        if not db_guild:
            response.result = Response.GUILD_DO_NOT_EXIST
            return

        if db_profile.level < db_guild.join_level:
            response.result = Response.LEVEL_LACK
            return

        response.guild_join.guild_uid = 0
        guild_member_max_count = self.table.const_info.get(GAMECOMMON.GUILD_MEMBER_MAX_COUNT).value
        if db_guild.member_count >= guild_member_max_count:
            response.result = Response.MEMBER_OF_THE_GUILD
            return

        if db_guild.join_type == Define.GUILD_JOIN_TYPE_OPEN:
            update_redis = {}
            update_redis[GAMECOMMON.R_USER_GUILD_UID] = db_guild.guild_uid
            update_redis[GAMECOMMON.R_USER_GUILD_GRADE] = Define.GUILD_GRADE_MEMBER


            # 탈퇴 후 재가입 할 경우
            db_member = self.w_db['guildmember'].get_guild_member(db_guild.guild_uid, self.userid)
            if not db_member:
                try:
                    self.w_db['guildmember'].add_guild_member(db_guild.guild_uid, self.userid, Define.GUILD_GRADE_MEMBER)
                    UpdateGuildMemberCount(self, db_guild.guild_uid, db_guild.member_count + 1)
                except Exception as e:
                    self.logger.exception(e.message)
                    response.result = Response.DB_SYSTEM_ERROR
                    return
            else:
                self.w_db['guildmember'].update_guild_member_grade(db_guild.guild_uid, self.userid, Define.GUILD_GRADE_MEMBER)

            self.cache.set_user_info_dict(self.userid, update_redis)

            db_update = []
            value_list = []

            db_update.append('guild_uid')
            value_list.append(db_guild.guild_uid)

            db_update.append('guild_grade')
            value_list.append(Define.GUILD_GRADE_MEMBER)

            self.w_db['profile'].update_user_column(self.userid, db_update, value_list)
            response.guild_join.guild_uid = db_guild.guild_uid
        else:
            response.guild_join.guild_uid = 0
            
            try:
                self.w_db['guildmember'].add_guild_member(db_guild.guild_uid, self.userid, Define.GUILD_GRADE_WAIT)
            except Exception as e:
                self.logger.exception(e.message)
                response.result = Response.DB_SYSTEM_ERROR
                return

        response.result = Response.SUCCESS
        return


    def GuildWithDraw(self, request, response):
        db_profile = self.w_db['profile'].select_column(self.userid, "guild_uid")
        if not db_profile:
            response.result = Response.USER_INVALID
            return
        
        db_grade = self.w_db['profile'].select_column(self.userid, "guild_grade")
        if db_grade.guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        db_guild = self.w_db['guildinfo'].find_guild(db_profile.guild_uid)
        if not db_guild:
            self.w_db['guildmember'].del_guild_member(db_profile.guild_uid, self.userid)
            self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_GUILD_UID, 0)
            response.result = Response.GUILD_DO_NOT_EXIST
            return

        db_guild_member = self.w_db['guildmember'].get_guild_member(db_profile.guild_uid, self.userid)
        if not db_guild_member:
            response.result = Response.NOT_IN_GUILD
            return

        # if db_guild.member_count > 1 and db_guild_member.guild_grade == Define.GUILD_GRADE_MASTER:
        #     response.result = Response.GUILD_GUILD_MASTER_LEAVE
        #     return

        if db_guild_member.guild_grade == Define.GUILD_GRADE_WAIT:
            response.result = Response.NOT_IN_GUILD
            return

        if db_guild_member.guild_grade == Define.GUILD_GRADE_MASTER:
            guildMasterWithDraw(self, db_guild)
            response.result = Response.SUCCESS
            return

        update_redis = {}
        update_redis[GAMECOMMON.R_USER_GUILD_UID] = 0
        update_redis[GAMECOMMON.R_USER_GUILD_GRADE] = Define.GUILD_GRADE_NONE

        # try:
        #     self.w_db['guildmember'].del_guild_member(db_profile.guild_uid, self.userid)
        # except Exception as e:
        #     self.logger.exception(e.message)
        #     response.result = Response.DB_SYSTEM_ERROR
        #     return

        # UpdateGuildMemberCount(self, db_guild.guild_uid, db_guild.member_count - 1)

        # 길드 탈퇴시 db 레코드를 삭제하지 않고 상태값만 변경한다.
        self.w_db['guildmember'].update_guild_member_grade(db_profile.guild_uid, self.userid, Define.GUILD_GRADE_QUIT)
        UpdateGuildMemberCount(self, db_guild.guild_uid, db_guild.member_count - 1)

        self.cache.set_user_info_dict(self.userid, update_redis)
        self.w_db['profile'].withdraw_guild(self.userid, self.begin)

        response.result = Response.SUCCESS
        return

    def GuildMemberKick(self, request, response):
        if request.guild_member_kick.member_uid == self.userid:
            response.result = Response.NO_AUTHORITY
            return

        redis_profile = self.cache_clone.get_user_profile(self.userid)
        if not redis_profile:
            response.result = Response.USER_INVALID
            return

        guild_grade = int(redis_profile[GAMECOMMON.R_USER_GUILD_GRADE])
        if guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        guild_uid = int(redis_profile[GAMECOMMON.R_USER_GUILD_UID])
        db_guild = self.w_db['guildinfo'].find_guild(guild_uid)
        if not db_guild:
            response.result = Response.NOT_IN_GUILD
            return

        if guild_grade > Define.GUILD_GRADE_SECOND_MASTER:
            response.result = Response.NO_AUTHORITY
            return

        db_kick_member = self.w_db['guildmember'].get_guild_member(guild_uid, request.guild_member_kick.member_uid)
        if not db_kick_member:
            response.result = Response.USER_INVALID
            return

        if db_kick_member.guild_grade <= guild_grade:
            response.result = Response.NO_AUTHORITY
            return

        redis_data = {}
        redis_data[GAMECOMMON.R_USER_GUILD_UID] = 0
        redis_data[GAMECOMMON.R_USER_GUILD_GRADE] = Define.GUILD_GRADE_KICK
        self.cache.set_user_info_dict(request.guild_member_kick.member_uid, redis_data)

        self.w_db['guildmember'].del_guild_member(guild_uid, request.guild_member_kick.member_uid)
        self.w_db['profile'].guild_kick(request.guild_member_kick.member_uid)

        UpdateGuildMemberCount(self, db_guild.guild_uid, db_guild.member_count - 1)
        response.result = Response.SUCCESS
        return

    def GuildMemberAccept(self, request, response):
        redis_profile = self.cache_clone.get_user_profile(self.userid)
        if not redis_profile:
            response.result = Response.USER_INVALID
            return

        guild_grade = int(redis_profile[GAMECOMMON.R_USER_GUILD_GRADE])
        if guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return        

        guild_uid = int(redis_profile[GAMECOMMON.R_USER_GUILD_UID])
        db_guild = self.w_db['guildinfo'].find_guild(guild_uid)
        if not db_guild:
            response.result = Response.NOT_IN_GUILD
            return

        if guild_grade > Define.GUILD_GRADE_SECOND_MASTER:
            response.result = Response.NO_AUTHORITY
            return

        accept_member_redis = self.cache_clone.get_user_data(
            request.guild_member_accept.member_uid,
            GAMECOMMON.R_USER_GUILD_UID
        )
        if not accept_member_redis:
            response.result = Response.JOIN_CANCEL_MEMBER
            return

        if 0 < int(accept_member_redis):
            response.result = Response.JOIN_CANCEL_MEMBER
            return

        db_member = self.w_db['guildmember'].get_guild_member(guild_uid, request.guild_member_accept.member_uid)
        if not db_member:
            response.result = Response.JOIN_CANCEL_MEMBER
            return

        if db_member.guild_grade != Define.GUILD_GRADE_WAIT:
            response.result = Response.JOIN_CANCEL_MEMBER
            return

        redis_data = {}
        redis_data[GAMECOMMON.R_USER_GUILD_UID] = db_guild.guild_uid
        redis_data[GAMECOMMON.R_USER_GUILD_GRADE] = Define.GUILD_GRADE_MEMBER
        self.cache.set_user_info_dict(request.guild_member_accept.member_uid, redis_data)
        self.w_db['profile'].guild_join(request.guild_member_accept.member_uid, db_guild.guild_uid)
        self.w_db['guildmember'].add_guild_member(
            db_guild.guild_uid,
            request.guild_member_accept.member_uid,
            Define.GUILD_GRADE_MEMBER
        )

        UpdateGuildMemberCount(self, db_guild.guild_uid, db_guild.member_count + 1)
        response.result = Response.SUCCESS
        return

    def GuildMemberRefusal(self, request, response):
        redis_profile = self.cache_clone.get_user_profile(self.userid)
        if not redis_profile:
            response.result = Response.USER_INVALID
            return

        guild_uid = int(redis_profile[GAMECOMMON.R_USER_GUILD_UID])
        guild_grade = int(redis_profile[GAMECOMMON.R_USER_GUILD_GRADE])

        if guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        if guild_grade > Define.GUILD_GRADE_SECOND_MASTER:
            response.result = Response.NO_AUTHORITY
            return

        db_member = self.w_db['guildmember'].get_guild_member(guild_uid, request.guild_member_refusal.member_uid)
        if not db_member:
            response.result = Response.USER_INVALID
            return

        if db_member.guild_grade != Define.GUILD_GRADE_WAIT:
            response.result = Response.JOIN_CANCEL_MEMBER
            return

        self.w_db['guildmember'].del_guild_member(guild_uid, request.guild_member_refusal.member_uid)
        response.result = Response.SUCCESS
        return

    def GuildMemberChangeGrade(self, request, response):
        if request.guild_member_kick.member_uid == self.userid:
            response.result = Response.NO_AUTHORITY
            return

        redis_profile = self.cache_clone.get_user_profile(self.userid)
        if not redis_profile:
            response.result = Response.USER_INVALID
            return

        guild_grade = int(redis_profile[GAMECOMMON.R_USER_GUILD_GRADE])
        if guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        if guild_grade != Define.GUILD_GRADE_MASTER:
            response.result = Response.NO_AUTHORITY
            return

        guild_uid = int(redis_profile[GAMECOMMON.R_USER_GUILD_UID])
        db_member = self.w_db['guildmember'].get_guild_member(guild_uid, request.guild_member_change_grade.member_uid)
        if not db_member:
            response.result = Response.USER_INVALID
            return

        self.w_db['guildmember'].add_guild_member(
            guild_uid,
            request.guild_member_change_grade.member_uid,
            request.guild_member_change_grade.change_grade
        )

        self.cache.set_user_info(
            request.guild_member_change_grade.member_uid,
            GAMECOMMON.R_USER_GUILD_GRADE,
            request.guild_member_change_grade.change_grade
        )
        
        if request.guild_member_change_grade.change_grade == Define.GUILD_GRADE_SECOND_MASTER:
            self.w_db['guildmember'].update_grade_promote_time(guild_uid, request.guild_member_change_grade.member_uid, self.begin)

        if request.guild_member_change_grade.change_grade == Define.GUILD_GRADE_MASTER:
            self.guild.update_guild_info(guild_uid, GAMECOMMON.GUILD_MASTER_UID, request.guild_member_change_grade.member_uid)
            self.w_db['guild'].change_master(guild_uid, request.guild_member_change_grade.member_uid)
            self.w_db['guildmember'].add_guild_member(guild_uid, self.userid, Define.GUILD_GRADE_SECOND_MASTER)
            self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_GUILD_GRADE, Define.GUILD_GRADE_SECOND_MASTER)
            
        response.result = Response.SUCCESS
        return

    def GuildJoinCondition(self, request, response):
        redis_profile = self.cache_clone.get_user_profile(self.userid)
        if not redis_profile:
            response.result = Response.USER_INVALID
            return

        guild_grade = int(redis_profile[GAMECOMMON.R_USER_GUILD_GRADE])
        if guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        if guild_grade != Define.GUILD_GRADE_MASTER:
            response.result = Response.NO_AUTHORITY
            return

        guild_uid = int(redis_profile[GAMECOMMON.R_USER_GUILD_UID])
        guild_redis = {}
        guild_redis[GAMECOMMON.GUILD_JOIN_TYPE] = request.guild_join_condition.join_type
        guild_redis[GAMECOMMON.GUILD_JOIN_LEVEL] = request.guild_join_condition.JoinLevel
        self.guild.update_guild_info_dict(guild_uid, guild_redis)

        self.w_db['guildinfo'].join_condition_change(
            guild_uid,
            request.guild_join_condition.join_type,
            request.guild_join_condition.JoinLevel
        )

        response.result = Response.SUCCESS
        return

    def GuildMSGModify(self, request, response):
        redis_profile = self.cache_clone.get_user_profile(self.userid)
        if not redis_profile:
            response.result = Response.USER_INVALID
            return

        guild_uid = int(redis_profile[GAMECOMMON.R_USER_GUILD_UID])
        if 0 >= guild_uid:
            response.result = Response.NO_AUTHORITY
            return

        guild_grade = int(redis_profile[GAMECOMMON.R_USER_GUILD_GRADE])
        if guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        if guild_grade != Define.GUILD_GRADE_MASTER:
            response.result = Response.NO_AUTHORITY
            return

        self.w_db['guildinfo'].update_guild_info(guild_uid, request.guild_msg_modify.msg)
        self.guild.update_guild_info(guild_uid, GAMECOMMON.GUILD_MESSAGE, request.guild_msg_modify.msg)

        response.result = Response.SUCCESS
        return

    def GuildInfoModify(self, request, response):
        redis_profile = self.cache_clone.get_user_profile(self.userid)
        if not redis_profile:
            response.result = Response.USER_INVALID
            return

        guild_uid = int(redis_profile[GAMECOMMON.R_USER_GUILD_UID])
        if 0 >= guild_uid:
            response.result = Response.NO_AUTHORITY
            return

        guild_grade = int(redis_profile[GAMECOMMON.R_USER_GUILD_GRADE])
        if guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        if guild_grade != Define.GUILD_GRADE_MASTER:
            response.result = Response.NO_AUTHORITY
            return

        msg = request.guild_info_modify.guild_info.guild_msg
        bg = request.guild_info_modify.guild_info.guild_bg
        emblem = request.guild_info_modify.guild_info.guild_emblem
        join_type = request.guild_info_modify.guild_info.join_type
        join_level = request.guild_info_modify.guild_info.join_level

        self.w_db['guild'].modify_guild(guild_uid, bg, emblem)
        self.w_db['guildinfo'].update_guild_info(guild_uid, msg, join_type, join_level)
        self.guild.update_guild_info_dict(
            guild_uid,
            {
                GAMECOMMON.GUILD_MESSAGE: msg,
                GAMECOMMON.GUILD_BG: bg,
                GAMECOMMON.GUILD_EMBLEM: emblem,
                GAMECOMMON.GUILD_JOIN_TYPE: join_type,
                GAMECOMMON.GUILD_JOIN_LEVEL: join_level
            }
        )
        response.result = Response.SUCCESS
        return

    def GetGuildInfo(self, request, response):
        user_redis = self.cache_clone.get_user_profile(self.userid)
        if not user_redis:
            response.result = Response.USER_INVALID
            return

        guild_uid = getGuildInfoType(self, request.get_guild_info)
        if not guild_uid:
            response.result = Response.GUILD_NOT_FOUND
            return

        guild_redis = self.guild_clone.get_guild_info(guild_uid)
        if not guild_redis:
            response.result = Response.GUILD_NOT_FOUND
            return
 
        # 운영툴에서 셋팅한 길드승부 기간 정보
        db_guildcontestinfo = self.w_db['guildcontestinfo'].get_guild_contest_info()
        if not db_guildcontestinfo:
            response.result = Response.GUILD_CONTEST_INFO_DO_NOT_EXIST
            return

        now_time = datetime.now()
        contest_start_time = db_guildcontestinfo.start_time
        contest_end_time = db_guildcontestinfo.end_time + timedelta(days=1) # 종료시간 8일로 셋팅시 00시 이므로 1일 추가
        diff = now_time - contest_start_time # 0,1,2,3

        # 길드 승부 활성화 체크하기 (0일차, 1일차 2일차 true, 3일차 false, 실제 전투에 참여 했는지 여부와 상관 없이) 
        # 운영툴에서 걸어놓은 길드 승부 기간이 아니면 false
        guild_contest_flag = True
        if (now_time < contest_start_time) or (now_time > contest_end_time):
             guild_contest_flag = False
        if diff.days == 3:
            guild_contest_flag = False


        member_cnt = self.w_db['guildmember'].guild_member_count(guild_uid)

        response.get_guild_info.guild_info.guild_uid = guild_uid
        response.get_guild_info.guild_info.guild_name = guild_redis[GAMECOMMON.GUILD_NAME]
        response.get_guild_info.guild_info.guild_msg = guild_redis[GAMECOMMON.GUILD_MESSAGE]
        response.get_guild_info.guild_info.my_grade = int(user_redis[GAMECOMMON.R_USER_GUILD_GRADE])
        response.get_guild_info.guild_info.guild_bg = int(guild_redis[GAMECOMMON.GUILD_BG])
        response.get_guild_info.guild_info.guild_emblem = int(guild_redis[GAMECOMMON.GUILD_EMBLEM])
        response.get_guild_info.guild_info.join_type = int(guild_redis[GAMECOMMON.GUILD_JOIN_TYPE])
        response.get_guild_info.guild_info.join_level = int(guild_redis[GAMECOMMON.GUILD_JOIN_LEVEL])
        response.get_guild_info.guild_info.member_cnt = member_cnt
        response.get_guild_info.guild_info.master_name = ""
        master_redis = self.cache_clone.get_user_data(guild_redis[GAMECOMMON.GUILD_MASTER_UID], GAMECOMMON.R_USER_NICK)
        if master_redis:
            response.get_guild_info.guild_info.master_name = master_redis
        response.get_guild_info.guild_info.guild_point = int(guild_redis[GAMECOMMON.GUILD_POINT])
        response.get_guild_info.guild_info.guild_contest_flag = int(guild_contest_flag) 
        response.result = Response.SUCCESS
        return

    def GuildMemberList(self, request, response):
        db_member_list = self.w_db['guildmember'].guild_member_all(request.guild_member_list.guild_uid)
        if not db_member_list:
            response.result = Response.GUILD_NOT_FOUND
            return

        for member in db_member_list:

            if member.guild_grade == Define.GUILD_GRADE_QUIT or member.guild_grade == Define.GUILD_GRADE_KICK:
                continue

            member_info = response.guild_member_list.member_info.add()
            member_info.member_uid = member.auid
            member_info.member_name = ""
            member_info.member_grade = member.guild_grade
            member_redis = self.cache_clone.get_user_profile(member.auid)
            
            if member_redis:
                member_info.member_name = member_redis[GAMECOMMON.R_USER_NICK]
                member_info.guild_point = int(member_redis[GAMECOMMON.R_USER_GUILD_POINT])
                member_info.level = int(member_redis[GAMECOMMON.R_USER_LEVEL])
                member_info.avatar_id = int(member_redis[GAMECOMMON.R_USER_AVATAR_ID])

            damage_list = convert_string_to_array(member.raid_record)
            for damageInfo in damage_list:
                attack_time = time_diff_in_seconds(damageInfo[0])
                record = member_info.damage_record.add()
                record.attacktime = attack_time
                record.damage = int(damageInfo[1])

            contest_damage_list = convert_string_to_array(member.contest_damage_record)
            for damageInfo in contest_damage_list:
                attack_time = time_diff_in_seconds(damageInfo[0])
                record = member_info.contest_damage_record.add()
                record.attacktime = attack_time
                record.damage = int(damageInfo[1])

        response.result = Response.SUCCESS
        return

    def GuildRecommendList(self, response):
        response.guild_recommend_list.CopyFrom(Response.GuildRecommendList())
        guild_uids = getGuildRecommendList(self)
        for uid in guild_uids:
            guild_redis = self.guild_clone.get_guild_info(uid)
            if not guild_redis:
                continue

            guild_info = response.guild_recommend_list.guild_info.add()
            guild_info.guild_uid = uid
            guild_info.guild_name = guild_redis[GAMECOMMON.GUILD_NAME]
            guild_info.guild_msg = guild_redis[GAMECOMMON.GUILD_MESSAGE]
            guild_info.guild_bg = int(guild_redis[GAMECOMMON.GUILD_BG])
            guild_info.guild_emblem = int(guild_redis[GAMECOMMON.GUILD_EMBLEM])
            guild_info.join_type = int(guild_redis[GAMECOMMON.GUILD_JOIN_TYPE])
            guild_info.join_level = int(guild_redis[GAMECOMMON.GUILD_JOIN_LEVEL])
            member_cnt = self.w_db['guildmember'].guild_member_count(uid)
            guild_info.member_cnt = member_cnt
            guild_info.master_name = ""
            master_redis = self.cache_clone.get_user_data(
                guild_redis[GAMECOMMON.GUILD_MASTER_UID],
                GAMECOMMON.R_USER_NICK
            )
            if master_redis:
                guild_info.master_name = master_redis
            guild_info.guild_point = int(guild_redis[GAMECOMMON.GUILD_POINT])

        response.result = Response.SUCCESS
        return

    def GuildSearch(self, request, response):
        response.guild_search.CopyFrom(Response.GuildSearch())
        guild_uids = getGuildSearchList(self, request.guild_search.search_key)
        for uid in guild_uids:
            guild_redis = self.guild_clone.get_guild_info(uid)
            if not guild_redis:
                continue

            guild_info = response.guild_search.guild_info.add()
            guild_info.guild_uid = uid
            guild_info.guild_name = guild_redis[GAMECOMMON.GUILD_NAME]
            guild_info.guild_msg = guild_redis[GAMECOMMON.GUILD_MESSAGE]
            guild_info.guild_bg = int(guild_redis[GAMECOMMON.GUILD_BG])
            guild_info.guild_emblem = int(guild_redis[GAMECOMMON.GUILD_EMBLEM])
            guild_info.join_type = int(guild_redis[GAMECOMMON.GUILD_JOIN_TYPE])
            guild_info.join_level = int(guild_redis[GAMECOMMON.GUILD_JOIN_LEVEL])
            member_cnt = self.w_db['guildmember'].guild_member_count(uid)
            guild_info.member_cnt = member_cnt
            guild_info.master_name = ""
            master_redis = self.cache_clone.get_user_data(
                guild_redis[GAMECOMMON.GUILD_MASTER_UID],
                GAMECOMMON.R_USER_NICK
            )
            if master_redis:
                guild_info.master_name = master_redis
            guild_info.guild_point = int(guild_redis[GAMECOMMON.GUILD_POINT])

        response.result = Response.SUCCESS
        return