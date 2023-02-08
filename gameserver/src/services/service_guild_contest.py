# -*- coding: utf-8 -*-
from datetime import date

from google.protobuf.json_format import *

from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *
from src.services.service_common import *
from src.services.service_guild import *


class ServiceGuildContest(object):
    def _getContestTicket(self, profile, ticket_max, increase_ticket):
        add_ticket = 0
        ticket_time = profile.guild_contest_ticket_time
        constest_charge_time = 14400 # TODO: 길드 승부 티켓 충전시간이 있는지 기획 및 로직 제검토. 아마 없는것으로 암.
        if profile.guild_contest_ticket < ticket_max:
            if profile.guild_contest_ticket_time:
                interval = self.begin - profile.guild_contest_ticket_time
                add_ticket = int(interval.seconds / constest_charge_time)
                if add_ticket > 0:
                    add_time = timedelta(seconds = add_ticket * constest_charge_time)
                    ticket_time = profile.guild_contest_ticket_time + add_time
            else:
                ticket_time = self.begin
        
        total_ticket= int(profile.guild_contest_ticket + add_ticket + increase_ticket)
        if total_ticket >= ticket_max:
            ticket_time = None

        return (total_ticket, ticket_time)

    def _findListTable(_lv, _listTable):
        return [element for element in _listTable if element['monster_level'] == _lv]


    # TODO: 코드 최적화 및 정리 필요
    def GuildContestInfo(self, response):
        db_profile = self.w_db['profile'].select_column(self.userid, "guild_uid, guild_grade")

        # 길드승부 도중 탈퇴된 길드원 에러 처리
        if db_profile.guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        # 운영툴에서 셋팅한 길드승부 기간 정보
        db_guildcontestinfo = self.w_db['guildcontestinfo'].get_guild_contest_info()
        if not db_guildcontestinfo:
            response.result = Response.GUILD_CONTEST_INFO_DO_NOT_EXIST
            return

        # 유저의 길드 기본정보
        db_guild = self.w_db['guild'].select_guild(db_profile.guild_uid)
        if not db_guild:
            response.result = Response.GUILD_DO_NOT_EXIST
            return
        
        now_time = datetime.now()
        guild_create_time = db_guild.guild_create
        contest_start_time = db_guildcontestinfo.start_time
        contest_end_time = db_guildcontestinfo.end_time + timedelta(days=1) # 종료시간 8일로 셋팅시 00시 이므로 1일 추가

        # 운영툴에서 셋팅한 길드승부 기간중에 생성된 길드인지 체크.
        if (guild_create_time > contest_start_time) and (guild_create_time < contest_end_time):
            response.result = Response.INVAILD_GUILD_CREATE_DAY
            return

        # 유효하지 않은 값 범위. - 운영툴에서 셋팅한 길드승부 기간이 아니다. 
        # (기획팀 논의 완료. 다른 컨텐츠를 하는 기간 혹은 아무것도 안함.)
        # issue2022 : 요청으로 3일차 이후에도 길드 승부 결과를 볼 수 있도록 하기 위해 주석처리
        # if (now_time < contest_start_time) or (now_time > contest_end_time):
        #     response.result = Response.NOT_PERIOD_GUILD_CONTEST
        #     return

        diff = now_time - contest_start_time # 0,1,2,3

        # 0일차 : 상대방 길드를 찾아 메치메이킹을 하는 기간.
        # 클라는 이 기간중 전투에는 못 들어가고 나옴. (기획 시퀀스 화면 1)
        if diff.days == 0:
            response.guild_contest_info.CopyFrom(Response.GuildContestInfo())
            response.result = Response.SUCCESS
            return

        # 1일차 ~ 2일차 : 길드승부 진행중. 나의 길드와 매칭된 상대방 길드정보를 준다.
        # 클라는 이때 전투 화면에 진입 할 수 있다. (GuildContestStart 패킷, GuildContestEnd 패킷)
        
        # 3일차 : 클라 정보 표기 요청으로 내길드, 상대길드 표기하도록 패킷 리턴 - 전투진입 불가

        # 길드 승부 정보
        db_guildinfo = self.w_db['guildinfo'].find_guild(db_profile.guild_uid)
        if not db_guildinfo:
            response.result = Response.GUILD_DO_NOT_EXIST
            return

        # 예외처리(임시) - 매칭기간중에 상대방 길드를 찾지 못 할 수도 있다. 
        # 길드 갯수가 홀수개, 혹은 기간중에 맞는 점수의 매칭상대를 찾지 못할 경우 등. 이 부분은 기획과 추가 논의 필요.
        enemy_guild_uid = db_guildinfo.contest_enemy_guild_guid
        if enemy_guild_uid == None:
            response.result = Response.NOT_FOUND_MATCH_GUILD_CONTEST
            return

        player_guild_redis = self.guild_clone.get_guild_info(db_profile.guild_uid)
        enemy_guild_redis = self.guild_clone.get_guild_info(enemy_guild_uid)
        user_redis = self.cache_clone.get_user_profile(self.userid)

        db_guildmember = self.w_db['guildmember'].get_guild_member(db_profile.guild_uid, self.userid)
        if not db_guildmember:
            response.result = Response.GUILD_NOT_FOUND
            return

        guild_contest_flag = 0
        if db_guildmember.contest_reward_time != None:
             guild_contest_flag = 1

        member_cnt = self.w_db['guildmember'].guild_member_count(db_profile.guild_uid)
        
        # 내 길드
        response.guild_contest_info.playerGuild.info.guild_uid = db_profile.guild_uid
        response.guild_contest_info.playerGuild.info.guild_name = player_guild_redis[GAMECOMMON.GUILD_NAME]
        response.guild_contest_info.playerGuild.info.guild_msg = player_guild_redis[GAMECOMMON.GUILD_MESSAGE]
        response.guild_contest_info.playerGuild.info.my_grade = int(user_redis[GAMECOMMON.R_USER_GUILD_GRADE])
        response.guild_contest_info.playerGuild.info.guild_bg = int(player_guild_redis[GAMECOMMON.GUILD_BG])
        response.guild_contest_info.playerGuild.info.guild_emblem = int(player_guild_redis[GAMECOMMON.GUILD_EMBLEM])
        response.guild_contest_info.playerGuild.info.join_type = int(player_guild_redis[GAMECOMMON.GUILD_JOIN_TYPE])
        response.guild_contest_info.playerGuild.info.join_level = int(player_guild_redis[GAMECOMMON.GUILD_JOIN_LEVEL])
        response.guild_contest_info.playerGuild.info.member_cnt = member_cnt
        response.guild_contest_info.playerGuild.info.guild_point = int(player_guild_redis[GAMECOMMON.GUILD_POINT])
        response.guild_contest_info.playerGuild.info.guild_contest_flag = int(guild_contest_flag) 
        response.guild_contest_info.playerGuild.info.master_name = ""
        master_name = self.cache_clone.get_user_data(player_guild_redis[GAMECOMMON.GUILD_MASTER_UID], GAMECOMMON.R_USER_NICK)
        if master_name:
            response.guild_contest_info.playerGuild.info.master_name = master_name

        # 적 길드
        enemy_member_cnt = self.w_db['guildmember'].guild_member_count(enemy_guild_uid)
        
        response.guild_contest_info.enemyGuild.info.guild_uid = enemy_guild_uid
        response.guild_contest_info.enemyGuild.info.guild_name = enemy_guild_redis[GAMECOMMON.GUILD_NAME]
        response.guild_contest_info.enemyGuild.info.guild_msg = enemy_guild_redis[GAMECOMMON.GUILD_MESSAGE]
        response.guild_contest_info.enemyGuild.info.my_grade = int(Define.GUILD_GRADE_MEMBER) # TODO: 상대방 길드 uid는 알지만 상대방 userid는 모름. 일반길드원 처리
        response.guild_contest_info.enemyGuild.info.guild_bg = int(enemy_guild_redis[GAMECOMMON.GUILD_BG])
        response.guild_contest_info.enemyGuild.info.guild_emblem = int(enemy_guild_redis[GAMECOMMON.GUILD_EMBLEM])
        response.guild_contest_info.enemyGuild.info.join_type = int(enemy_guild_redis[GAMECOMMON.GUILD_JOIN_TYPE])
        response.guild_contest_info.enemyGuild.info.join_level = int(enemy_guild_redis[GAMECOMMON.GUILD_JOIN_LEVEL])
        response.guild_contest_info.enemyGuild.info.member_cnt = enemy_member_cnt
        response.guild_contest_info.enemyGuild.info.guild_point = int(enemy_guild_redis[GAMECOMMON.GUILD_POINT])
        response.guild_contest_info.enemyGuild.info.guild_contest_flag = int(0) # TODO: 상대방 길드 uid는 알지만 상대방 userid는 모름. 0 처리
        response.guild_contest_info.enemyGuild.info.master_name = ""
        master_name = self.cache_clone.get_user_data(enemy_guild_redis[GAMECOMMON.GUILD_MASTER_UID], GAMECOMMON.R_USER_NICK)
        if master_name:
            response.guild_contest_info.enemyGuild.info.master_name = master_name

        # 내 길드 멤버 정보
        player_members = self.w_db['guildmember'].guild_member_all(db_profile.guild_uid)
        for member in player_members:
            member_info = response.guild_contest_info.playerGuild.members.add()
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

        # 적 길드 멤버 정보
        enemy_members = self.w_db['guildmember'].guild_member_all(enemy_guild_uid)
        for member in enemy_members:
            member_info = response.guild_contest_info.enemyGuild.members.add()
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

        response.guild_contest_info.id = 1
        response.guild_contest_info.days = diff.days
        response.guild_contest_info.cur_hp = db_guildinfo.contest_monster_hp
        response.guild_contest_info.boss_id = db_guildinfo.contest_monster
        response.guild_contest_info.boss_level = db_guildinfo.contest_monster_level
        response.guild_contest_info.remain_time = int(date.today().strftime('%Y%m%d'))
        response.result = Response.SUCCESS
        return

    def GuildContestStart(self, response):
        db_profile = self.w_db['profile'].select_column(self.userid, "guild_uid, guild_contest_ticket, guild_contest_ticket_time, guild_grade")
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        if db_profile.guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        contest_ticket_max = int(self.table.const_info.get(GAMECOMMON.CONTEST_TICKET_MAX).value)
        contest_charge_time = 14400 # TODO 기획 문의. 어떤 시간인가

        ticket, ticket_time = ServiceGuildContest._getContestTicket(self, db_profile, contest_ticket_max, 0)
        update_ticket = ticket - 1
        if 0 > update_ticket:
            response.result = Response.LACK_GUILD_CONTEST_TICKET
            return

        if not ticket_time:
            ticket_time = self.begin

        db_update = []
        value_list = []

        db_update.append('last_mode')
        value_list.append(GAMECOMMON.PLAY_MODE_GUILD_CONTEST)

        db_update.append('guild_contest_ticket')
        value_list.append(update_ticket)

        str_column = "guild_contest_ticket_time=NULL"
        response.guild_contest_start.contest_ticket_time = 0
        if ticket_time != None:
            str_column = "guild_contest_ticket_time='%s'" % (ticket_time)
            response.guild_contest_start.contest_ticket_time = self.next_charge_second(ticket_time, contest_charge_time)

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list, str_column)
        self.w_db['guildmember'].guild_contest_start(db_profile.guild_uid, self.userid, self.begin)

        response.guild_contest_start.contest_ticket = update_ticket
        response.result = Response.SUCCESS
        return

    def GuildContestEnd(self, request, response):
        db_profile = self.w_db['profile'].select_column(self.userid, "guild_uid, last_mode, guild_grade")
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        if db_profile.last_mode != GAMECOMMON.PLAY_MODE_GUILD_CONTEST:
            response.result = Response.LAST_PLAY_MODE_WRONG
            return

        if db_profile.guild_grade == Define.GUILD_GRADE_KICK:
            response.result = Response.GUILD_CHANGE_KICKED
            return

        db_guildinfo = self.w_db['guildinfo'].find_guild(db_profile.guild_uid)
        if not db_guildinfo:
            response.result = Response.GUILD_DO_NOT_EXIST
            return

        db_guildmember = self.w_db['guildmember'].get_guild_member(db_profile.guild_uid, self.userid)
        if not db_guildmember:
            response.result = Response.NOT_IN_GUILD
            return
        
        damage_record = convert_string_to_array(db_guildmember.contest_damage_record)
        damage_record.append([str(self.begin), request.guild_contest_end.damage])

        self.w_db['guildmember'].update_guild_contest_damage_record(db_profile.guild_uid, self.userid, str(damage_record))
        self.w_db['guildcontestdamage'].add_guild_contest_damage(db_profile.guild_uid, self.userid, request.guild_contest_end.damage)
        boss_hp = db_guildinfo.contest_monster_hp
        cur_hp = int(boss_hp) - int(request.guild_contest_end.damage)
        self.w_db['guildinfo'].update_contest_monster_hp(db_profile.guild_uid, cur_hp)

        response.guild_contest_end.boss_hp = cur_hp
        response.result = Response.SUCCESS
        return

    def GuildContestReward(self, response):
        # 조건에 맞을 경우 - 운영툴에서 셋팅한 길드 승부 기간이 3일차 이고 길드승부 참여 정보가 있는 유저.
        # 이때 기간중 로그인한 유저가 있으면 보상을 지급한다.
        
        # 유저의 길드승부 참여 정보가 있는지 체크
        db_profile = self.w_db['profile'].select_column(self.userid, "guild_uid, guild_grade")
        if not db_profile:
            response.result = Response.SUCCESS
            return

        # 정산 처리할때 탈퇴된 길드원은 보상 지급 없음
        if (db_profile.guild_grade == Define.GUILD_GRADE_QUIT) or (db_profile.guild_grade == Define.GUILD_GRADE_KICK):
            response.result = Response.SUCCESS
            return

        db_guildmember = self.w_db['guildmember'].get_guild_member(db_profile.guild_uid, self.userid)
        if not db_guildmember:
            response.result = Response.SUCCESS
            return

        if db_guildmember.contest_start_time == None:
            response.result = Response.SUCCESS
            return

         # 중복 지급 방지
        if db_guildmember.contest_reward_time != None:
            response.result = Response.SUCCESS
            return

        db_guildinfo = self.w_db['guildinfo'].find_guild(db_profile.guild_uid)
        if not db_guildinfo:
            response.result = Response.SUCCESS
            return

        player_guild_uid = db_profile.guild_uid
        enemy_guild_uid = db_guildinfo.contest_enemy_guild_guid
        player_constest_damage_sum = 0
        enemy_constest_damage_sum = 0
        
        # 내 길드 맴버 정보
        player_members = self.w_db['guildmember'].guild_member_all(player_guild_uid)
        for member in player_members:
            contest_damage_list = convert_string_to_array(member.contest_damage_record)
            for damageInfo in contest_damage_list:
                player_constest_damage_sum = player_constest_damage_sum + damageInfo[1]

        # 적 길드 멤버 정보
        enemy_members = self.w_db['guildmember'].guild_member_all(enemy_guild_uid)
        for member in enemy_members:
            contest_damage_list = convert_string_to_array(member.contest_damage_record)
            for damageInfo in contest_damage_list:
                enemy_constest_damage_sum = enemy_constest_damage_sum + damageInfo[1]

        # 승리 조건 체크 - 내 점수가 낮으면 패 이므로 우편으로 지급 안함.
        if (player_constest_damage_sum < enemy_constest_damage_sum):
            response.result = Response.SUCCESS
            return

        # 운영툴에서 셋팅한 길드승부 기간 정보
        db_guildcontestinfo = self.w_db['guildcontestinfo'].get_guild_contest_info()
        if not db_guildcontestinfo:
            response.result = Response.SUCCESS
            return

        now_time = datetime.now()
        contest_start_time = db_guildcontestinfo.start_time
        contest_end_time = db_guildcontestinfo.end_time + timedelta(days=1)

        # 운영툴에서 셋팅한 길드승부 기간이 아니다. TODO: (티켓 충전 시켜놓음 3/3)
        if (now_time < contest_start_time) or (now_time > contest_end_time):
            response.result = Response.SUCCESS
            return

        diff = now_time - contest_start_time

        # 0일차 : 어차피 모든 유저는 전투 진입을 하지 못하니 이때 접속한 유저는 티켓을 3/3으로 충전
        if diff.days == 0:
            response.result = Response.SUCCESS
            return

        # 1일차 : 유저가 각자 티켓을 소모함. 1일차는 아무것도 충전 안함.
        if diff.days == 1:
            response.result = Response.SUCCESS
            return

        # 3일차 : 정리 및 정산기간 인지 조건 체크 
        if diff.days != 3:
            response.result = Response.SUCCESS
            return

        # TODO: 임시 로직 승리한경우 길드포인트 +10 패배한 경우 길드포인트 -10 일단 200점 기준으로 함.
        # self.w_db['guildmember'].update_guild_point(player_guild_uid, 200)
        # self.w_db['guildmember'].update_guild_point(enemy_guild_uid, 200)

        # 우편 메시지 임시값.
        title = 'Guild Contest Reward Title',
        post = 'Guild Contest Reward Msg',

        # TODO: 임시로직 및 db. war_point관련 변경 사항이 없음. 워포인트 200~250 기준으로 매칭을 잡고 보상처리
        table = self.table.contest
        row = ServiceGuildContest._findListTable(
            db_guildinfo.contest_monster_level,
            table
        )
        
        reward_id = row[0].reward
        item_dict = ServiceCommon.get_reward_list(self, reward_id)
        items = str(list(map(lambda kv: [kv[0], kv[1].count], item_dict.items())))
        remove_time = datetime.now() + timedelta(days=14)
        self.w_db['post'].send_post(
            auid=self.userid,
            post_type=1, 
            title_msg=title,
            post_msg=post,
            post_item=items,
            remove_time=remove_time,
            keep_day=14
        )

        # 우편을 보냈으면 보상을 받은 유저로 처리
        self.w_db['guildmember'].update_contest_reward_time(player_guild_uid, self.userid, now_time)

        response.result = Response.SUCCESS
        return