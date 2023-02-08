# -*- coding: utf-8 -*-
import re
import time

from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


def calCountAndTime(self, count, time, charge_time, max):
    result_time = time
    result_count = count
    if count > max:
        result_time = None
        return (result_count, result_time)
    
    if not time:
        result_time = self.begin
        return (result_count, result_time)

    interval = self.begin - time
    add_count = int(interval.seconds / charge_time)
    if add_count > 0:
        add_time = timedelta(seconds = add_count * charge_time)
        result_time = time + add_time
        result_count += add_count
    if result_count > max:
        result_count = max
        result_time = None

    return (result_count, result_time)


class ServiceUser(object):
    def __init__(self):
        pass

    # TODO: 리펙 2차 클래스 내부에서만 쓰이는 메서드에 대한 네이밍 구분 및 구조, 설계 변화 필요    
    # 레핑 메서드 인데 session변수가 context.py에서 쓰임 확인 필요
    def generate_session_id(self, userid, nickname, serial):
        return self.session.generate_session_id(userid, nickname, serial)

    def LoginUser(self, request, response):
        account_db = self.w_db['account'].find_web_userid(request.login_user.user_token)
        if not account_db:
            response.result = Response.USER_NOT_FOUND
            return

        self.userid = account_db.account_uid
        response.login_user.nickname = account_db.nick_name
        response.login_user.block_time = 0
        response.login_user.session_id = ServiceUser.generate_session_id(
            self,
            account_db.account_uid,
            account_db.nick_name,
            request.serial
        )

        redis_data = {}
        redis_data[GAMECOMMON.R_USER_LAST_LOGIN] = str(self.begin)

        self.w_db['account'].update_last_login(self.userid, self.begin)
        self.cache.set_user_info_dict(self.userid, redis_data)
        response.login_user.serverTime = int(time.time())
        response.result = Response.SUCCESS
        return


    def RegisterUser(self, request, response):
        pattern = re.compile(r'\s+')
        sentence = re.sub(pattern, '', request.register_user.nickname)

        nick_name_min = int(self.table.const_info.get(GAMECOMMON.MIN_LENGTH_NICK_NAME).value)
        nick_name_max = int(self.table.const_info.get(GAMECOMMON.MAX_LENGTH_NICK_NAME).value)

        if nick_name_min > len(sentence.encode('euc-kr')):
            response.result = response.INVALID_NICKNAME
            return
        
        if nick_name_max < len(sentence.encode('euc-kr')):
            response.result = response.INVALID_NICKNAME
            return

        check_token = self.w_db['account'].find_web_userid(request.register_user.user_token)
        if check_token:
            response.result = Response.EXIST_WEB_USER_TOKEN
            return

        start_hero = set()
        try:
            self.userid = self.w_db['account'].insert_account(
                request.register_user.account_type,
                request.register_user.user_token,
                sentence,
                request.register_user.device_info,
                self.begin,
                request.register_user.email
            )

            withdraw_time = get_pass_time(-1, 0, 0)
            start_hero = set(map(lambda item: item.value, filter(lambda item: item.type == Define.INVEN_TYPE_HERO, self.table.start_hero)))
            stamina = int(self.table.const_info.get(GAMECOMMON.STAMINA_MAX_BASIC).value)
            raid_ticket_max = int(self.table.const_info.get(GAMECOMMON.RAID_TICKET_MAX).value)
            arena_ticket_max = int(self.table.const_info.get(GAMECOMMON.ARENA_TICKET_MAX).value)
            darknest_ticket_max = int(self.table.const_info.get(GAMECOMMON.DARKNEST_TICKET_MAX).value)
            contest_ticket_max = int(self.table.const_info.get(GAMECOMMON.CONTEST_TICKET_MAX).value)
            default_hero_max = int(self.table.const_info.get(GAMECOMMON.DEFAULT_HERO_MAX).value)
            default_equip_normal_max = int(self.table.const_info.get(GAMECOMMON.DEFAULT_EQUIP_NORMAL_MAX).value)
            default_equip_pvp_max = int(self.table.const_info.get(GAMECOMMON.DEFAULT_EQUIP_PVP_MAX).value)

            self.w_db['profile'].insert_profile(
                auid = self.userid,
                equip_normal_max = default_equip_normal_max,
                equip_pvp_max = default_equip_pvp_max,
                hero_max = default_hero_max,
                stamina = stamina,
                guild_withdraw_time = withdraw_time,
                raid_ticket = raid_ticket_max,
                arena_ticket = arena_ticket_max,
                darknest_ticket = darknest_ticket_max,
                contest_ticket = contest_ticket_max,
                had_hero_set = convert_set_to_string(start_hero)
            )


            self.w_db['territory'].insert_territory(self.userid, Define.BUILDING_TYPE_CASTLE, level=1, start_time=self.begin, build_slot=1)
            self.w_db['territory'].insert_territory(self.userid, Define.BUILDING_TYPE_ALTAR, level=1, start_time=self.begin, build_slot=2)
            reward_date = datetime(withdraw_time.year, withdraw_time.month, withdraw_time.day)
            self.w_db['attendance'].insert_attendance_info(self.userid, reward_date)

        except Exception as e:
            self.logger.error("insert account error : {}".format(e))
            response.result = Response.INVALID_PROFILE
            return

        teamInfo = {}
        teamInfo['formation'] = 2 # 왜 고정값 2 인가?
        hero_slot_idx = 0
        for item in self.table.start_hero:
            if item.type == Define.INVEN_TYPE_HERO:
                self.w_db['heroinven'].insert_hero(self.userid, item.value)
                hero_slot_idx += 1
            elif item.type == Define.INVEN_TYPE_EQUIP:
                self.w_db['equipinven'].insert_equip(self.userid, item.value, False)
            elif item.type == Define.INVEN_TYPE_ETC:
                if item.value == GAMECOMMON.ITEM_GOLD_ID:
                    self.w_db['profile'].increase_money(self.userid, item.count)
                elif item.value == GAMECOMMON.ITEM_RUBY_ID:
                    self.w_db['profile'].increase_cash(self.userid, item.count)
                else:
                    self.w_db['etcinven'].add_item(self.userid, item.value, item.count)

        self.w_db['regioninfo'].insert_region_info(self.userid)

        for idx in range(1, GAMECOMMON.RESOURCE_REFRESH_COUNT):
            self.w_db['resourcecollect'].insert_data(self.userid, idx, self.begin)

        for idx in range(0, GAMECOMMON.RESOURCE_REFRESH_COUNT):
            resource, level, dist = self.generate_resource()
            self.w_db['resourcedispatch'].insert_data(
                self.userid,
                idx + GAMECOMMON.RESOURCE_REFRESH_COUNT,
                resource,
                level, 
                dist
            )

        # TODO: 변수 선언 이게 최적인가?
        territory_dict = {}
        territory_dict[Define.BUILDING_TYPE_CASTLE] = 1
        territory_dict[Define.BUILDING_TYPE_ALTAR] = 1
        territory_dict[Define.BUILDING_TYPE_FOOD_STORAGE] = self.table.const_info.get(GAMECOMMON.BASE_FOOD_STORAGE).value
        territory_dict[Define.BUILDING_TYPE_IRON_STORAGE] = self.table.const_info.get(GAMECOMMON.BASE_IRON_STORAGE).value
        territory_dict[Define.BUILDING_TYPE_STONE_STORAGE] = self.table.const_info.get(GAMECOMMON.BASE_STONE_STORAGE).value
        territory_dict[Define.BUILDING_TYPE_WOOD_STORAGE] = self.table.const_info.get(GAMECOMMON.BASE_WOOD_STORAGE).value
        territory_dict[Define.BUILDING_TYPE_TRADE_SHIP] = {}
        territory_dict[Define.BUILDING_TYPE_WORKSHOP] = {}
        territory_dict[Define.BUILDING_TYPE_LABORATORY] = {}

        try:
            self.cache.set_user_profile(
                user_id=self.userid,
                nickname=sentence,
                last_login=str(self.begin),
                team_info=str(teamInfo),
                level=1,
                exp=0,
                territory_dict=str(territory_dict),
                start_hero=convert_set_to_string(start_hero)
            )
        except Exception as e:
            response.result = Response.FAILURE
            return

        check_idx = int(24 - self.begin.hour)
        if 2 < check_idx:
            check_idx = 0

        check_list = [0, 0, 0]
        check_list[check_idx] = 1
        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_REFRESH_RESOURCE, str(check_list))

        # darknest insert
        darknest_id = 1 # 초기값이므로 1
        darknest_dict = {}
        darknest_dict[darknest_id] = 1
        self.w_db['darknest'].insert_darknest_info(self.userid, darknest_id, self.begin, str(darknest_dict))

        response.result = Response.SUCCESS
        return

    def GetProfile(self, response):
        account_db = self.w_db['account'].find_user_id(self.userid)
        if not account_db:
            response.result = Response.INVALID_USER
            return

        db_info = self.w_db['profile'].find_profile(self.userid)
        if not db_info:
            response.result = Response.INVALID_PROFILE
            return

        db_update = []
        value_list = []
        str_column = None
        response.get_profile.auid = self.userid
        response.get_profile.last_login_time = time_diff_in_seconds(account_db.last_login)
        response.get_profile.arena_match_refresh_time = time_diff_in_seconds(db_info.arena_match_refresh_time)
        response.get_profile.avatar_id = db_info.avatar_id
        response.get_profile.level = db_info.level
        response.get_profile.exp = db_info.exp
        response.get_profile.hero_inven_max = db_info.hero_inven_max
        response.get_profile.equp_inven_normal_max = db_info.equip_normal_inven_max
        response.get_profile.equp_inven_pvp_max = db_info.equip_pvp_inven_max
        response.get_profile.cash = db_info.cash
        response.get_profile.money = db_info.money
        response.get_profile.stamina_max = db_info.stamina_max
        response.get_profile.stamina_time = 0
        
        # 아레나 관련 리펙토링
        # TODO: 코드 리펙토링
        db_arena_normal = self.w_db['arenanormal'].get_arena_info(self.userid)
        arean_rank = 0
        const_reward_time = int(self.table.const_info.get(GAMECOMMON.ARENA_NORMAL_REWARD_TERM).value)
        arena_reward_time = 0
        if not db_arena_normal:
            arean_rank = self.arena_clone.get_arena_normal_total() + 1
            self.arena.set_arena_normal_rank(self.userid, arean_rank) # TODO: redis에 2중 관리 필요한가?
            refresh_time = get_pass_time(0, 0, -7200) # TODO: 갱신 시간에 관하여 다시 로직 검토
            self.w_db['arenanormal'].insert_arena_info(self.userid, arean_rank, refresh_time, datetime.now())
            arena_reward_time = const_reward_time
        else:
            arean_rank = db_arena_normal.rank
            reward_time = time_diff_in_seconds(db_arena_normal.reward_time)
            if (const_reward_time > reward_time):
                arena_reward_time = const_reward_time - reward_time
        
        response.get_profile.reward_time_arena_normal = arena_reward_time
        response.get_profile.rank_arena_normal = arean_rank
        
        season_end = datetime(self.begin.year, self.begin.month+1, 1, 0, 0, 1)
        if self.begin.month == 12:
            season_end = datetime(self.begin.year+1, 1, 1, 0, 0, 1)
        
        response.get_profile.season_time_arena_normal = time_diff_in_seconds(season_end)
        
        stamina_charge_time = int(self.table.const_info.get(GAMECOMMON.STAMINA_TIME).value)
        # stamina start
        stamina, stamina_time = calCountAndTime(
            self,
            db_info.stamina_cur,
            db_info.stamina_time,
            stamina_charge_time,
            db_info.stamina_max,
        )
        db_update.append('stamina_cur')
        value_list.append(stamina)
        response.get_profile.stamina = stamina
        response.get_profile.stamina_time = self.next_charge_second(stamina_time, stamina_charge_time) if stamina_time else 0
        str_column = "stamina_time=NULL"
        if stamina_time != None:
            str_column = "stamina_time='%s'" % (stamina_time)
        # stamina end
        
        # raid_ticket start
        raid_ticket_max = int(self.table.const_info.get(GAMECOMMON.RAID_TICKET_MAX).value)
        raid_charge_time = int(self.table.const_info.get(GAMECOMMON.RAID_CHARGE_TIME).value)
        raid_ticket, raid_ticket_time = calCountAndTime(
            self,
            db_info.guild_raid_ticket, 
            db_info.guild_raid_ticket_time,
            raid_charge_time,
            raid_ticket_max,
        )
        db_update.append('guild_raid_ticket')
        value_list.append(raid_ticket)
        response.get_profile.guild_raid_ticket = raid_ticket
        response.get_profile.guild_raid_ticket_time = self.next_charge_second(raid_ticket_time, raid_charge_time) if raid_ticket_time else 0
        
        if raid_ticket_time != None:
            str_column += ",guild_raid_ticket_time='%s'" % (raid_ticket_time)
        else:
            str_column += ",guild_raid_ticket_time=NULL"
        # raid_ticket end
        
        # contest_ticket start
        contest_ticket_max = int(self.table.const_info.get(GAMECOMMON.CONTEST_TICKET_MAX).value)
        contest_charge_time = 14400 # TODO 기획 문의. 어떤 시간인가
        contest_ticket, contest_ticket_time = calCountAndTime(
            self,
            db_info.guild_contest_ticket, 
            db_info.guild_contest_ticket_time,
            contest_charge_time,
            contest_ticket_max,
        )
        db_update.append('guild_contest_ticket')
        value_list.append(contest_ticket)
        response.get_profile.guild_contest_ticket = contest_ticket
        response.get_profile.guild_contest_ticket_time = self.next_charge_second(contest_ticket_time, contest_charge_time) if contest_ticket_time else 0
        
        if contest_ticket_time != None:
            str_column += ",guild_contest_ticket_time='%s'" % (contest_ticket_time)
        else:
            str_column += ",guild_contest_ticket_time=NULL"

        # contest_ticket end
        
        # arena_ticket start
        arena_ticket_max = int(self.table.const_info.get(GAMECOMMON.ARENA_TICKET_MAX).value)
        arena_charge_time = int(self.table.const_info.get(GAMECOMMON.ARENA_CHARGE_TIME).value)
        arena_ticket, arena_ticket_time = calCountAndTime(
            self,
            db_info.arena_ticket, 
            db_info.arena_ticket_time,
            arena_charge_time, 
            arena_ticket_max
        )
        db_update.append('arena_ticket')
        value_list.append(arena_ticket)
        response.get_profile.arena_ticket = arena_ticket
        response.get_profile.arena_ticket_time = self.next_charge_second(arena_ticket_time, arena_charge_time) if arena_ticket_time else 0
        
        if arena_ticket_time != None:
            str_column += ",arena_ticket_time='%s'" % (arena_ticket_time)
        else:
            str_column += ",arena_ticket_time=NULL"

        # arena_ticket end
        
        # darknest_ticket start
        darknest_ticket_max = int(self.table.const_info.get(GAMECOMMON.DARKNEST_TICKET_MAX).value)
        darknest_charge_time = int(self.table.const_info.get(GAMECOMMON.DARKNEST_CHARGE_TIME).value)
        darknest_ticket, darknest_ticket_time = calCountAndTime(
            self,
            db_info.darknest_ticket, 
            db_info.darknest_ticket_time,
            darknest_charge_time, 
            darknest_ticket_max
        )
        db_update.append('darknest_ticket')
        value_list.append(darknest_ticket)
        response.get_profile.darknest_ticket = darknest_ticket
        response.get_profile.darknest_ticket_time = self.next_charge_second(darknest_ticket_time, darknest_charge_time) if darknest_ticket_time else 0
        
        if darknest_ticket_time != None: 
            str_column += ",darknest_ticket_time='%s'" % (darknest_ticket_time)
        else:
            str_column += ",darknest_ticket_time=NULL"
        # darknest_ticket end
        
        if 0 != db_info.guild_uid:
            guild_redis = self.guild_clone.get_guild_info(db_info.guild_uid)
            if guild_redis:
                response.get_profile.guildinfo.guild_uid = db_info.guild_uid
                response.get_profile.guildinfo.guild_name = guild_redis[GAMECOMMON.GUILD_NAME]
                response.get_profile.guildinfo.my_grade = db_info.guild_grade
                response.get_profile.guildinfo.guild_bg = int(guild_redis[GAMECOMMON.GUILD_BG])
                response.get_profile.guildinfo.guild_emblem = int(guild_redis[GAMECOMMON.GUILD_EMBLEM])
                response.get_profile.guildinfo.guild_point = int(guild_redis[GAMECOMMON.GUILD_POINT])
                master_redis = self.cache_clone.get_user_data(guild_redis[GAMECOMMON.GUILD_MASTER_UID],GAMECOMMON.R_USER_NICK)
                if master_redis:
                    response.get_profile.guildinfo.master_name = master_redis

        self.w_db['profile'].update_user_column(self.userid, db_update, value_list, str_column)

        db_info = self.w_db['regioninfo'].select_region_info(self.userid)
        if not db_info:
            response.result = Response.DB_NOT_EXIST
            return

        response.get_profile.regionInfo.region_num = db_info.region_num
        response.get_profile.regionInfo.region_difficulty = db_info.region_difficulty
        response.get_profile.regionInfo.region_step = db_info.region_step
        response.result = Response.SUCCESS
        return


    def GetUserProfile(self, request, response):
        user_uid = request.get_user_profile.user_uid
        user_redis = self.cache_clone.get_user_profile(user_uid)
        if not user_redis:
            response.result = Response.USER_INVALID
            return

        stamina = int(self.table.const_info.get(GAMECOMMON.STAMINA_MAX_BASIC).value)

        response.get_user_profile.user_info.stamina = stamina
        response.get_user_profile.user_info.stamina_max = stamina
        response.get_user_profile.user_info.nickname = user_redis[GAMECOMMON.R_USER_NICK]
        response.get_user_profile.user_info.avatar_id = int(user_redis[GAMECOMMON.R_USER_AVATAR_ID])
        response.get_user_profile.user_info.level = int(user_redis[GAMECOMMON.R_USER_LEVEL])
        response.get_user_profile.user_info.exp = int(user_redis[GAMECOMMON.R_USER_EXP])
        
        level_set = convert_string_to_set(user_redis[GAMECOMMON.R_USER_LEVEL_SET])
        response.get_user_profile.user_info.rewarded_level_list.extend(list(level_set))
        response.get_user_profile.user_info.arenaRank = self.arena_clone.get_arena_normal_rank(user_uid)
        
        # TODO: redis team info 삭제 예정 - 여기가 가장 중요
        team_info = user_redis[GAMECOMMON.R_USER_TEAM_INFO]
        self.convert_team_data_redis_to_protobuf(response.get_user_profile.user_info.team_info, team_info)

        response.get_user_profile.user_info.guildinfo.guild_uid = 0
        response.get_user_profile.user_info.guildinfo.guild_name = ''
        response.get_user_profile.user_info.guildinfo.guild_bg = 0
        response.get_user_profile.user_info.guildinfo.guild_emblem = 0
        response.get_user_profile.user_info.guildinfo.master_name = ''
        response.get_user_profile.user_info.guildinfo.guild_point = 0
        response.get_user_profile.user_info.last_login_time = time_diff_in_seconds(parser.parse(user_redis[GAMECOMMON.R_USER_LAST_LOGIN]))
        
        if 0 != int(user_redis[GAMECOMMON.R_USER_GUILD_UID]):
            guild_redis = self.guild_clone.get_guild_info(user_redis[GAMECOMMON.R_USER_GUILD_UID])
            if guild_redis:
                response.get_user_profile.user_info.guildinfo.guild_uid = int(user_redis[GAMECOMMON.R_USER_GUILD_UID])
                response.get_user_profile.user_info.guildinfo.guild_name = guild_redis[GAMECOMMON.GUILD_NAME]
                response.get_user_profile.user_info.guildinfo.guild_bg = int(guild_redis[GAMECOMMON.GUILD_BG])
                response.get_user_profile.user_info.guildinfo.guild_emblem = int(guild_redis[GAMECOMMON.GUILD_EMBLEM])
                master_redis = self.cache_clone.get_user_data(guild_redis[GAMECOMMON.GUILD_MASTER_UID], GAMECOMMON.R_USER_NICK)
                if master_redis:
                    response.get_user_profile.user_info.guildinfo.master_name = master_redis
                response.get_user_profile.user_info.guildinfo.guild_point = int(guild_redis[GAMECOMMON.GUILD_POINT])

        response.result = Response.SUCCESS
        return


    def ChangeNickName(self, request, response):
        db_info = self.w_db['profile'].select_column(self.userid, "cash")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        consume_cash = int(self.table.const_info.get(GAMECOMMON.CASH_CONSUME_NICK_NAME_CHANGE).value)

        update_cash = db_info.cash - consume_cash
        if 0 > update_cash:
            response.result = Response.CASH_LACK
            return

        pattern = re.compile(r'\s+')
        sentence = re.sub(pattern, '', request.nick_name_change.change_nick)

        nick_name_min = int(self.table.const_info.get(GAMECOMMON.MIN_LENGTH_NICK_NAME).value)
        nick_name_max = int(self.table.const_info.get(GAMECOMMON.MAX_LENGTH_NICK_NAME).value)

        if nick_name_min > len(sentence.encode('euc-kr')):
            response.result = response.INVALID_NICKNAME
            return
        
        if nick_name_max < len(sentence.encode('euc-kr')):
            response.result = response.INVALID_NICKNAME
            return

        try:
            self.w_db['account'].change_user_nickname(self.userid, sentence)
        except:
            response.result = response.EXIST_NICKNAME
            return

        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_NICK, sentence)

        self.w_db['profile'].update_cash(self.userid, update_cash)

        consume_cash = int(self.table.const_info.get(GAMECOMMON.CASH_CONSUME_NICK_NAME_CHANGE).value)
        response.nick_name_change.use_cash = consume_cash
        response.nick_name_change.change_nick = sentence
        response.result = Response.SUCCESS
        return


    def ChangeAvatar(self, request, response):
        self.w_db['profile'].update_avatar_id(self.userid, request.avatar_change.change_avatar)
        self.cache.set_user_info(self.userid, GAMECOMMON.R_USER_AVATAR_ID, request.avatar_change.change_avatar)
        response.result = Response.SUCCESS
        return


    def UseCash(self, request, response):
        db_profile = self.w_db['profile'].select_column(self.userid, "cash")
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        update_cash = db_profile.cash - request.use_cash.use_cash
        if 0 > update_cash:
            response.result = Response.CASH_LACK
            return

        self.w_db['profile'].update_cash(self.userid, update_cash)

        response.result = Response.SUCCESS
        return

    def ChargeAmount(self, request, response):
        db_profile = self.w_db['profile'].select_column(
            self.userid,
            "stamina_cur, guild_raid_ticket, arena_ticket, darknest_ticket, cash"
        )

        if not db_profile:
            response.result = Response.USER_INVALID
            return

        raid_ticket_max = int(self.table.const_info.get(GAMECOMMON.RAID_TICKET_MAX).value)
        arena_ticket_max = int(self.table.const_info.get(GAMECOMMON.ARENA_TICKET_MAX).value)
        darknest_ticket_max = int(self.table.const_info.get(GAMECOMMON.DARKNEST_TICKET_MAX).value)
        stamina_charge_cash = int(self.table.const_info.get(GAMECOMMON.STAMINA_CHARGE_CASH).value)
        stamina_charge_count = int(self.table.const_info.get(GAMECOMMON.STAMINA_CHARGE_COUNT).value)
        darknest_ticket_charge_cash = int(self.table.const_info.get(GAMECOMMON.DARKNEST_TICKET_CHARGE_CASH).value)
        arena_ticket_charge_cash = int(self.table.const_info.get(GAMECOMMON.ARENA_TICKET_CHARGE_CASH).value)
        raid_ticket_charge_cash = int(self.table.const_info.get(GAMECOMMON.RAID_TICKET_CHARGE_CASH).value)
        arena_refresh_cost = int(self.table.const_info.get(GAMECOMMON.ARENA_REFRESH_COST).value)

        # TODO: 로직 개선 - 지저분한 if else 코드 구조를 모듈화.
        charge_type = request.charge_amount.charge_type
        response.charge_amount.charge_type = request.charge_amount.charge_type
        use_cash = stamina_charge_cash
        if charge_type == Define.CHARGE_TYPE_STAMINA:
            update_value = db_profile.stamina_cur + stamina_charge_count
            update_cash = db_profile.cash - stamina_charge_cash
            if 0 > update_cash:
                response.result = Response.CASH_LACK
                return
            use_cash = stamina_charge_cash
        elif charge_type == Define.CHARGE_TYPE_ARENA_MATCH_REFRESH:
            update_value = 0
            update_cash = db_profile.cash - arena_refresh_cost
            if 0 > update_cash:
                response.result = Response.CASH_LACK
                return
            use_cash = arena_refresh_cost
        else:
            if charge_type == Define.CHARGE_TYPE_GUILD_RAID_TICKET:
                update_value = db_profile.guild_raid_ticket + raid_ticket_max
                use_cash = raid_ticket_charge_cash
            elif charge_type == Define.CHARGE_TYPE_ARENA_TICKET:
                update_value = db_profile.arena_ticket + arena_ticket_max
                use_cash = arena_ticket_charge_cash
            elif charge_type == Define.CHARGE_TYPE_DARKNEST_TICKET:
                update_value = db_profile.darknest_ticket + darknest_ticket_max
                use_cash = darknest_ticket_charge_cash
            else:
                response.result = Response.INVALID_VALUE
                return
            update_cash = db_profile.cash - use_cash
            if 0 > update_cash:
                response.result = Response.CASH_LACK
                return

        self.w_db['profile'].charge_amount_value(self.userid, request.charge_amount.charge_type, update_value, update_cash)
        response.charge_amount.use_cash = use_cash
        response.charge_amount.result_value = update_value

        response.result = Response.SUCCESS
        return

    def UserLevelReward(self, request, response):
        response.user_level_reward.CopyFrom(Response.UserLevelReward())

        db_profile = self.w_db['profile'].select_column(self.userid, "level, exp, stamina_max, stamina_cur, stamina_time, level_set")
        if not db_profile:
            response.result = Response.INVALID_PROFILE
            return

        db_level = db_profile.level
        db_exp = db_profile.exp
        db_stamina_cur = db_profile.stamina_cur
        db_level_set = db_profile.level_set

        level_set_str = db_level_set
        level_set = convert_string_to_set(level_set_str)

        request_level = request.user_level_reward.level

        exists = level_set and request_level in level_set
        if exists:
            response.result = Response.INVALID_USER_LEVEL_CONDITION
            return

        user_level_reward_data = self.table.user_level_exp.get(request_level, None)
        if not user_level_reward_data:
            response.result = Response.INVALID_GAMEDATA
            return


        max_stamina = user_level_reward_data.max_stamina
        reward_set_id = user_level_reward_data.reward_set_id

        level_set.add(request_level)
        level_set_str = convert_set_to_string(level_set)

        self.w_db['profile'].increase_stamina_max(self.userid, stamina_max=max_stamina)
        self.w_db['profile'].update_level_set(self.userid, level_set_str)

        item_dict = self.get_reward_list(reward_set_id)
        self.reward_packet_process(
            item_dict,
            response.user_level_reward.reward_item
        )

        response.user_level_reward.user_info.level = db_level
        response.user_level_reward.user_info.exp = db_exp
        response.user_level_reward.user_info.stamina = max_stamina + db_stamina_cur
        response.user_level_reward.user_info.stamina_max = max_stamina
        response.user_level_reward.user_info.rewarded_level_list.extend(list(level_set))
        response.result = Response.SUCCESS
        return