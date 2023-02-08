# -*- coding: utf-8 -*-
from random import randint

from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


class ServiceArenaNormal(object):
    def __init__(self):
        pass

    def __refresh_arena_match(self, my_rank):
        target_list = []
        for i in range(3):
            target_rank = ServiceArenaNormal.__get_arena_normal_target(self, my_rank, i + 1)
            if target_rank == my_rank:
                target_rank - 1

            if 0 < target_rank:
                target_list.append(target_rank)

        return target_list

    def __get_arena_normal_target(self, rank, number):
        min_rank = 0
        max_rank = 0

        if number == 1:
            min_rank = rank - 1
            max_rank = int(rank * 0.8)
        elif number == 2:
            min_rank = int(rank * 0.8) - 1
            max_rank = int(rank * 0.6)
        else:
            min_rank = int(rank * 0.6) - 1
            max_rank = int(rank * 0.4)

        if 0 >= min_rank:
            return -1
        return randint(max_rank, min_rank)

    def __arena_normal_rank_reward(self, rank):
        for reward in self.table.arena_normal_reward:
            if reward.rank_min <= rank and reward.rank_max >= rank:
                return reward.reward_id

        return self.table.arena_normal_reward[len(self.table.arena_normal_reward)-1].reward_id

    def __get_arena_ticket(self, userinfo, ticket_max, increase_ticket):
        add_ticket = 0
        ticket_time = None
        arena_charge_time = int(self.table.const_info.get(GAMECOMMON.ARENA_CHARGE_TIME).value)

        if userinfo.arena_ticket < ticket_max:
            if userinfo.arena_ticket_time:
                interval = self.begin - userinfo.arena_ticket_time if userinfo.arena_ticket_time else timedelta(seconds=ticket_max * arena_charge_time)
                add_ticket = interval.seconds / arena_charge_time
                if (userinfo.arena_ticket + add_ticket) < ticket_max:
                    if (userinfo.arena_ticket + add_ticket + increase_ticket) < ticket_max:
                        add_time = timedelta(seconds=interval.seconds / arena_charge_time * arena_charge_time)
                        ticket_time = userinfo.arena_ticket_time + add_time
                else:
                    add_ticket = ticket_max - userinfo.arena_ticket
                    if add_ticket < 0:
                        add_ticket = 0
            else:
                ticket_time = self.begin

        total_ticket= int(userinfo.arena_ticket + add_ticket + increase_ticket)
        return (total_ticket, ticket_time)



    def __res_packet_deck(self, _response):
        db_deck = self.w_db['deck'].get_deck_info(self.userid)
        if not db_deck:
            return
        
        hero_uids = []
        for i in range(1, 6):
            huid = "huid" + str(i)
            hero_uid = db_deck[huid]
            hero_uids.append(hero_uid)

        db_hero_list = self.w_db['heroinven'].find_item_list(self.userid, hero_uids)
        deck = _response.deck
        deck.formation = db_deck.formation
        for db_hero in db_hero_list:
            hero = deck.hero_list.add()
            hero.hero_uid = db_hero.uid
            hero.hero_id = db_hero.item_id
            hero.passive_1 = db_hero.passive_skill_id1
            hero.passive_2 = db_hero.passive_skill_id2

            if db_hero.potential_stat_list != None:
                db_potential_list = str(db_hero.potential_stat_list, 'utf-8').split(',')
                for db_potential in db_potential_list:
                    potential = hero.potential_stat_list.add()
                    data = str(db_potential).split(':')
                    potential.type = int(data[0])
                    potential.value = int(data[1])

            if (db_hero.equip_uid1 != None):
                db_equip1 = self.w_db['equipinven'].find_item(self.userid, db_hero.equip_uid1)
                if (db_equip1 != None):
                    hero.equip1.equip_uid = db_hero.equip_uid1
                    hero.equip1.equip_id = db_equip1.item_id
                    hero.equip1.equip_exp = db_equip1.exp

            if (db_hero.equip_uid2 != None):
                db_equip2 = self.w_db['equipinven'].find_item(self.userid, db_hero.equip_uid2)
                if (db_equip2 != None):
                    hero.equip2.equip_uid = db_hero.equip_uid2
                    hero.equip2.equip_id = db_equip2.item_id
                    hero.equip2.equip_exp = db_equip2.exp

        return

    def __get_target_match_info(self, _target_uid, _response):
        # 대상 유저 정보
        db_account = self.w_db['account'].find_user_id(_target_uid)
        db_arena_normal = self.w_db['arenanormal'].get_arena_info(_target_uid)
        db_profile = self.w_db['profile'].find_profile(_target_uid)
        
        target_guild_uid = db_profile.guild_uid
        db_guild = self.w_db['guild'].select_guild(target_guild_uid)

        user = _response
        user.rank = db_arena_normal.rank
        user.name = db_account.nick_name
        user.level = db_profile.level
        user.avatar_id = db_profile.avatar_id
        user.uid = _target_uid

        # 대상 유저의 덱 정보
        ServiceArenaNormal.__res_packet_deck(self, _response)

        # 대상 유저의 길드 정보 (필요한것 있으면 추가)
        guild = _response.guildinfo
        guild.guild_uid = db_guild.guild_uid
        guild.guild_name = db_guild.guild_name
        return _response

    def __update_deck(self, formation, hero_list):
        # update deck
        for hero in hero_list:
            self.w_db['deck'].update_deck_info(
                self.userid,
                formation,
                hero.slot_idx,
                hero.hero_uid
            )

        # hero equip update
        for hero in hero_list:
            if hero.equip_uid_1 != None:
                self.w_db['heroinven'].update_hero_equip_uid1(self.userid, hero.hero_uid, hero.equip_uid_1)
            if hero.equip_uid_2 != None:
                self.w_db['heroinven'].update_hero_equip_uid2(self.userid, hero.hero_uid, hero.equip_uid_2)
        
        return


    def get_info(self, response):
        target_list = []
        arean_rank = 0
        db_arena_normal = self.w_db['arenanormal'].get_arena_info(self.userid)
        const_reward_time = int(self.table.const_info.get(GAMECOMMON.ARENA_NORMAL_REWARD_TERM).value)

        if not db_arena_normal: # 최초 매칭 리스트 초기화
            arean_rank = self.arena_clone.get_arena_normal_total() + 1
            self.arena.set_arena_normal_rank(self.userid, arean_rank)
            refresh_time = get_pass_time(0, 0, -7200)
            self.w_db['arenanormal'].insert_arena_info(self.userid, arean_rank, refresh_time, datetime.now())
            response.get_arena_info.reward_time = const_reward_time

            target_list = ServiceArenaNormal.__refresh_arena_match(self, arean_rank)
            target_list_str = str(target_list)
            self.w_db['arenanormal'].set_arena_target(self.userid, target_list_str)
 
        elif db_arena_normal: # 기존 매칭 리스트 순위 검증
            arean_rank = db_arena_normal.rank

            reward_time = time_diff_in_seconds(db_arena_normal.reward_time)
            response.get_arena_info.reward_time = 0
            if const_reward_time > reward_time:
                response.get_arena_info.reward_time = const_reward_time - reward_time

            target_list_str = db_arena_normal.target_list
            target_list = convert_string_to_set(target_list_str)

            for target_rank in target_list:
                if arean_rank <= target_rank:
                    refresh_target_list = ServiceArenaNormal.__refresh_arena_match(self, arean_rank)
                    refresh_target_list_str = str(refresh_target_list)
                    self.w_db['arenanormal'].set_arena_target(self.userid, refresh_target_list_str)
                    target_list = refresh_target_list
                    break
        else:
            pass

        for rank in target_list:
            target_user = self.arena_clone.get_arena_normal_userid(rank)
            if not target_user:
                self.logger.error("db not exist target_user")
                continue
            redis_data = self.cache_clone.get_user_profile(target_user[0])
            if not redis_data:
                self.logger.error("cache not exist target_user")
                continue

            matchInfo = response.get_arena_info.normal_match_users.add()
            matchInfo.rank = rank
            matchInfo.name = redis_data[GAMECOMMON.R_USER_NICK]
            matchInfo.level = int(redis_data[GAMECOMMON.R_USER_LEVEL])
            matchInfo.avatar_id = int(redis_data[GAMECOMMON.R_USER_AVATAR_ID])
            matchInfo.uid = int(target_user[0])

            # TODO: redis team info 삭제 예정
            team_info = redis_data[GAMECOMMON.R_USER_TEAM_INFO]
            self.convert_team_data_redis_to_protobuf(matchInfo.team_info, team_info)

            if 0 != int(redis_data[GAMECOMMON.R_USER_GUILD_UID]):
                guild_redis = self.guild_clone.get_guild_info(redis_data[GAMECOMMON.R_USER_GUILD_UID])
                if guild_redis:
                    matchInfo.guildinfo.guild_name = guild_redis[GAMECOMMON.GUILD_NAME]
                    matchInfo.guildinfo.guild_bg = int(guild_redis[GAMECOMMON.GUILD_BG])
                    matchInfo.guildinfo.guild_emblem = int(guild_redis[GAMECOMMON.GUILD_EMBLEM])

        season_end = datetime(self.begin.year, self.begin.month+1, 1, 0, 0, 1)
        if self.begin.month == 12:
            season_end = datetime(self.begin.year+1, 1, 1, 0, 0, 1)

        response.get_arena_info.season_time = time_diff_in_seconds(season_end)
        response.get_arena_info.rank = arean_rank

        user_redis = self.cache_clone.get_user_profile(self.userid)
        if not user_redis:
            response.result = Response.USER_INVALID
            return

        # TODO: redis team info 삭제 예정
        team_info = user_redis[GAMECOMMON.R_USER_TEAM_INFO]
        self.convert_team_data_redis_to_protobuf(response.get_arena_info.team_info, team_info)
        
        # 나의 팀 정보 최대 5개. 없으면 빈배열
        # 클라가 요구하는 패킷을 추가하고 거기에 일단 강제로 맞추어 넣어준다.
        # 개발중에 기존 계정의 redis 구조가 변경된 것에 대한 대응은 redis 포멧 변경 혹은 redis 초기화로 대응한다.
        team_info_dict = convert_string_to_dict(team_info)
        for k, v in team_info_dict.items():
            if k == 'formation':
                continue
            
            resinfo = response.get_arena_info.team_hero.add()
            if not v['hero_uid']:
                continue
            
            resinfo.hero_uid = v['hero_uid']
            resinfo.equip1_uid = v['equip1']['equip_uid']
            resinfo.equip2_uid = v['equip2']['equip_uid']

        response.result = Response.SUCCESS
        return

    def get_match(self, response):
        db_arena_normal = self.w_db['arenanormal'].get_arena_info(self.userid)
        if not db_arena_normal:
            response.result = Response.USER_INVALID
            return

        target_list = ServiceArenaNormal.__refresh_arena_match(self, db_arena_normal.rank) 

        if db_arena_normal.target_list:
            # target_list = db_arena_normal.target_list
            # arr = self.convert_string_to_array(db_arena_normal.target_list)
            # target_list = arr
            pass
        else:
            self.logger.error("db_arena_normal.target_list is None")
            pass

        for rank in target_list:
            target_user = self.arena_clone.get_arena_normal_userid(rank)
            if not target_user:
                continue

            redis_data = self.cache_clone.get_user_profile(target_user[0])
            if not redis_data:
                continue

            matchInfo = response.get_arena_match_list.match_users.add()
            matchInfo.rank = rank
            matchInfo.name = redis_data[GAMECOMMON.R_USER_NICK]
            matchInfo.level = int(redis_data[GAMECOMMON.R_USER_LEVEL])
            matchInfo.avatar_id = int(redis_data[GAMECOMMON.R_USER_AVATAR_ID])
            matchInfo.uid = int(target_user[0])
            
            # TODO: redis team info 삭제 예정
            team_info = redis_data[GAMECOMMON.R_USER_TEAM_INFO]
            self.convert_team_data_redis_to_protobuf(matchInfo.team_info, team_info)

            if 0 != int(redis_data[GAMECOMMON.R_USER_GUILD_UID]):
                guild_redis = self.guild_clone.get_guild_info(redis_data[GAMECOMMON.R_USER_GUILD_UID])
                if guild_redis:
                    matchInfo.guildinfo.guild_name = guild_redis[GAMECOMMON.GUILD_NAME]
                    matchInfo.guildinfo.guild_bg = int(guild_redis[GAMECOMMON.GUILD_BG])
                    matchInfo.guildinfo.guild_emblem = int(guild_redis[GAMECOMMON.GUILD_EMBLEM])
        
        self.w_db['profile'].update_arena_match_refresh_time(self.userid, self.begin)
        response.result = Response.SUCCESS
        return

    def start_battle(self, request, response):
        db_info = self.w_db['profile'].select_column(self.userid, "arena_ticket, arena_ticket_time, level")
        if not db_info:
            response.result = Response.USER_INVALID
            return

        arena_ticket_max = int(self.table.const_info.get(GAMECOMMON.ARENA_TICKET_MAX).value)
        arena_charge_time = int(self.table.const_info.get(GAMECOMMON.ARENA_CHARGE_TIME).value)

        ticket, ticket_time = ServiceArenaNormal.__get_arena_ticket(self, db_info, arena_ticket_max, 0)
        update_ticket = ticket - 1
        if 0 > update_ticket:
            response.result = Response.ARENA_TICKET_LACK
            return

        if not ticket_time:
            ticket_time = self.begin

        db_update = []
        value_list = []

        db_update.append('last_mode')
        value_list.append(GAMECOMMON.PLAY_MODE_ARENA_NORMAL)

        db_update.append('arena_ticket')
        value_list.append(update_ticket)

        str_column = "arena_ticket_time=NULL"
        if ticket_time != None:
            str_column = "arena_ticket_time='%s'" % (ticket_time)
            response.start_arena_battle.arena_ticket_time = self.next_charge_second(ticket_time, arena_charge_time)
        
        self.w_db['profile'].select_column(self.userid, "arena_ticket, arena_ticket_time")
        self.w_db['profile'].update_user_column(self.userid, db_update, value_list, str_column)

        my_rank = self.arena_clone.get_arena_normal_rank(self.userid)
        if my_rank != request.start_arena_battle.my_rank:
            response.result = Response.INVALID_CACHE
            return

        db_arena_normal = self.w_db['arenanormal'].get_arena_info(self.userid)
        if not db_arena_normal:
            response.result = Response.DB_NOT_EXIST
            return

        find_target = self.arena_clone.get_arena_normal_userid(request.start_arena_battle.target_rank)
        if len(find_target) < 0:
            response.result = Response.INVALID_CACHE
            return

        target_auid = int(find_target[0])
        if target_auid != request.start_arena_battle.target_uid:
            response.result = Response.INVALID_CACHE
            return

        target_redis = self.cache_clone.get_user_profile(target_auid)
        if not target_redis:
            response.result = Response.INVALID_CACHE
            return

        # 나와 상대방의 타겟을 상호 기입
        self.w_db['arenanormal'].set_battle_target(auid=self.userid, target_uid=target_auid, battle_time=self.begin)
        self.w_db['arenanormal'].set_battle_target(auid=target_auid, target_uid=self.userid, battle_time=self.begin)

        response.start_arena_battle.match_user.rank = request.start_arena_battle.target_rank
        response.start_arena_battle.match_user.name = target_redis[GAMECOMMON.R_USER_NICK]
        response.start_arena_battle.match_user.level = int(target_redis[GAMECOMMON.R_USER_LEVEL])
        response.start_arena_battle.match_user.avatar_id = int(target_redis[GAMECOMMON.R_USER_AVATAR_ID])
        response.start_arena_battle.arena_ticket = update_ticket
        response.result = Response.SUCCESS
        return

    def end_battle(self, request, response):
        db_arena_normal = self.w_db['arenanormal'].get_arena_info(self.userid)
        if not db_arena_normal:
            response.result = Response.DB_NOT_EXIST
            return

        db_arena_target = self.w_db['arenanormal'].get_arena_info(db_arena_normal.battle_target_uid)
        if not db_arena_target:
            self.w_db['arenanormal'].clear_battle_target(self.userid)
            response.result = Response.DB_NOT_EXIST
            return

        my_battle_record = convert_string_to_array(db_arena_normal.battle_record)
        if 10 <= len(my_battle_record):
            del my_battle_record[0]

        target_battle_record = convert_string_to_array(db_arena_target.battle_record)
        if 10 <= len(target_battle_record):
            del target_battle_record[0]

        arena_reward = 0
        before_rank = db_arena_normal.rank
        target_list = []

        if request.end_arena_battle.win_flag:
            arena_reward = 100
            if db_arena_target.rank < db_arena_normal.rank:
                my_battle_record.append([1, 1, db_arena_target.auid, db_arena_normal.rank, db_arena_target.rank])
                target_battle_record.append([0, 0, db_arena_normal.auid, db_arena_target.rank, db_arena_normal.rank])

                self.w_db['arenanormal'].arena_battle_end_change_rank(self.userid, db_arena_target.rank, str(my_battle_record))
                self.w_db['arenanormal'].arena_battle_end_change_rank(db_arena_target.auid, db_arena_normal.rank, str(target_battle_record))

                self.arena.set_arena_normal_rank(self.userid, db_arena_target.rank)
                self.arena.set_arena_normal_rank(db_arena_target.auid, db_arena_normal.rank)

                response.end_arena_battle.change_rank = db_arena_target.rank
                target_list = ServiceArenaNormal.__refresh_arena_match(self, db_arena_target.rank)
            else:
                response.end_arena_battle.change_rank = db_arena_normal.rank
                target_list = ServiceArenaNormal.__refresh_arena_match(self, db_arena_normal.rank)

        else:
            arena_reward = 10

            my_battle_record.append([1, 0, db_arena_target.auid, db_arena_normal.rank, db_arena_target.rank])
            target_battle_record.append([0, 1, db_arena_normal.auid, db_arena_target.rank, db_arena_normal.rank])

            self.w_db['arenanormal'].arena_battle_end(self.userid, str(my_battle_record))
            self.w_db['arenanormal'].arena_battle_end(db_arena_target.auid, str(target_battle_record))

            response.end_arena_battle.change_rank = db_arena_normal.rank
            target_list = ServiceArenaNormal.__refresh_arena_match(self, db_arena_normal.rank)

        self.w_db['etcinven'].add_item(self.userid, GAMECOMMON.ITEM_ARENA_COIN, arena_reward)

        if target_list:
            self.w_db['arenanormal'].set_arena_target(self.userid, str(target_list))
            pass

        # #issue1907 잘못된 구현 시간 외 자연 회복 말고 아레나 티켓을 주는 것은 상대방 랭크의 변화 유무이지 나의 랭크는 무관계
        # after_rank = response.end_arena_battle.change_rank
        # if after_rank < before_rank:
        #     db_info = self.w_db['profile'].select_column(self.userid, "arena_ticket, arena_ticket_time")
        #     if db_info:
        #         self.w_db['profile'].update_user_column(self.userid, ['arena_ticket'], [db_info.arena_ticket + 1])

        response.end_arena_battle.battle_type = Define.ARENA_TYPE_NORMAL
        response.end_arena_battle.reward_item.count = arena_reward
        response.end_arena_battle.reward_item.item_id = GAMECOMMON.ITEM_ARENA_COIN
        response.result = Response.SUCCESS
        return

    def reward(self, response):
        db_arena_normal = self.w_db['arenanormal'].get_arena_info(self.userid)
        if not db_arena_normal:
            response.result = Response.USER_INVALID
            return

        const_reward_time = int(self.table.const_info.get(GAMECOMMON.ARENA_NORMAL_REWARD_TERM).value)
        if const_reward_time > time_diff_in_seconds(db_arena_normal.reward_time):
            response.result = Response.TIME_ERROR
            return

        reward_id = ServiceArenaNormal.__arena_normal_rank_reward(self, db_arena_normal.rank)
        item_dict = self.get_reward_list(reward_id)
        self.reward_packet_process(
            item_dict,
            response.arena_reward.reward_item
        )
        self.w_db['arenanormal'].update_arena_reward_time(self.userid, datetime.now())

        response.arena_reward.reward_time = const_reward_time
        response.result = Response.SUCCESS
        return


    def ranking(self, response):
        rank_users = self.arena_clone.arena_normal_rank_range(1, 10)
        for rank in rank_users:
            user_redis = self.cache_clone.get_user_profile(int(rank[0]))
            if not user_redis:
                continue

            rank_user = response.arena_ranking_list.total_rank.add()
            rank_user.uid = int(rank[0])
            rank_user.name = user_redis[GAMECOMMON.R_USER_NICK]
            rank_user.rank = int(rank[1])
            rank_user.avatar_id = int(user_redis[GAMECOMMON.R_USER_AVATAR_ID])

        my_rank = self.arena_clone.get_arena_normal_rank(self.userid)
        if my_rank < 5:
            min_rank = 1
        else:
            min_rank = my_rank - 5
            min_rank = max(1, min_rank)

        max_rank = my_rank + 5
        between_rank = self.arena_clone.arena_normal_rank_range(min_rank, max_rank)
        for rank in between_rank:
            user_redis = self.cache_clone.get_user_profile(int(rank[0]))
            if not user_redis:
                continue

            rank_user = response.arena_ranking_list.between_rank.add()
            rank_user.uid = int(rank[0])
            rank_user.name = user_redis[GAMECOMMON.R_USER_NICK]
            rank_user.rank = int(rank[1])
            rank_user.avatar_id = int(user_redis[GAMECOMMON.R_USER_AVATAR_ID])

        response.result = Response.SUCCESS
        return

    def battle_record(self, response):
        db_arena_normal = self.w_db['arenanormal'].get_arena_info(self.userid)
        if not db_arena_normal:
            response.result = Response.USER_INVALID
            return

        history = convert_string_to_array(db_arena_normal.battle_record)
        for info in history:
            battle_info = response.arena_record_list.history_list.add()
            battle_info.attacker = int(info[0])
            battle_info.win_flag = int(info[1])
            target_redis = self.cache_clone.get_user_data(info[2], GAMECOMMON.R_USER_NICK)
            battle_info.name = target_redis if target_redis else ""
            battle_info.my_rank = int(info[3])
            battle_info.target_rank = int(info[4])
            battle_info.targetUid = int(info[2])

        response.result = Response.SUCCESS
        return

    # 아레나 일반전 명예의 전당
    def ArenaHallofFame(self, request, response):
        redis_hall_of_fame = self.arena_clone.get_hall_of_fame_data(GAMECOMMON.ARENA_HALL_OF_FAME)
        if not redis_hall_of_fame:
            response.arena_hall_of_fame.season = 0
            response.result = Response.SUCCESS
            return

        last_season = int(redis_hall_of_fame[GAMECOMMON.ARENA_LAST_SEASON])
        response.arena_hall_of_fame.season = last_season - (request.arena_hall_of_fame.page-1)
        hall_of_fame_list = convert_string_to_dict(redis_hall_of_fame[GAMECOMMON.ARENA_HALL_OF_FAME_LIST])
        if len(hall_of_fame_list) < request.arena_hall_of_fame.page:
            response.arena_hall_of_fame.season = 0
            response.result = Response.SUCCESS
            return

        rank = 1

        for auid in hall_of_fame_list[request.arena_hall_of_fame.page - 1]:
            if 0 == auid:
                continue

            redis_data = self.cache_clone.get_user_profile(auid)
            if not redis_data:
                matchInfo = response.arena_hall_of_fame.users.add()
                matchInfo.rank = rank
                matchInfo.name = ''
                matchInfo.level = 0
                matchInfo.avatar_id = 0
                matchInfo.uid = 0

                rank += 1
                continue

            matchInfo = response.arena_hall_of_fame.users.add()
            matchInfo.rank = rank
            matchInfo.name = redis_data[GAMECOMMON.R_USER_NICK]
            matchInfo.level = int(redis_data[GAMECOMMON.R_USER_LEVEL])
            matchInfo.avatar_id = int(redis_data[GAMECOMMON.R_USER_AVATAR_ID])
            matchInfo.uid = int(auid)

            # TODO: redis team info 삭제 예정
            team_info = redis_data[GAMECOMMON.R_USER_TEAM_INFO]
            self.convert_team_data_redis_to_protobuf(matchInfo.team_info, team_info)

            if 0 != int(redis_data[GAMECOMMON.R_USER_GUILD_UID]):
                guild_redis = self.guild_clone.get_guild_info(redis_data[GAMECOMMON.R_USER_GUILD_UID])
                if guild_redis:
                    matchInfo.guildinfo.guild_name = guild_redis[GAMECOMMON.GUILD_NAME]
                    matchInfo.guildinfo.guild_bg = int(guild_redis[GAMECOMMON.GUILD_BG])
                    matchInfo.guildinfo.guild_emblem = int(guild_redis[GAMECOMMON.GUILD_EMBLEM])

            rank += 1

        response.result = Response.SUCCESS
        return

    def Get_Deck(self, response):
        ServiceArenaNormal.__res_packet_deck(self, response.get_deck_arena_normal)
        response.result = Response.SUCCESS
        return

    def Update_Deck(self, request, response):
        # TODO: deck db update
        req_formation = request.update_deck_arena_normal.formation
        req_hero_list = request.update_deck_arena_normal.hero_list

        db_deck = self.w_db['deck'].get_deck_info(self.userid)
        if not db_deck:
            self.w_db['deck'].insert_deck_info(self.userid, req_formation)
           
        ServiceArenaNormal.__update_deck(self, req_formation, req_hero_list)

        # 업데이트 후 덱 정보
        ServiceArenaNormal.__res_packet_deck(self, response.update_deck_arena_normal)
        
        response.result = Response.SUCCESS
        return

    def Get_Match(self, request, response):
        req_target_uid = request.get_match_arena_normal.target_uid

        ServiceArenaNormal.__get_target_match_info(self, req_target_uid, response.get_match_arena_normal.match_user_info)
        
        response.result = Response.SUCCESS
        return

    def Search_Match(self, response):
        match_target_uid_list = [1214, 1214, 1214] # 테스트 데이터 - 예를들어 대상 3명을 찾음.

        for target_uid in match_target_uid_list:
            match_user_info = response.search_match_arena_normal.match_user_list.add()
            ServiceArenaNormal.__get_target_match_info(self, target_uid, match_user_info)

        response.result = Response.SUCCESS
        return

    def Refresh_Match(self, response):
        match_target_uid_list = [1214, 1214, 1214] # 테스트 데이터 - 예를들어 대상 3명을 찾음.

        for target_uid in match_target_uid_list:
            match_user_info = response.refresh_match_arena_normal.match_user_list.add()
            ServiceArenaNormal.__get_target_match_info(self, target_uid, match_user_info)

        response.refresh_match_arena_normal.remain_time = 1223330 # 15분 이하의 unixtimestamp
        response.result = Response.SUCCESS
        return

    def Skip_Match(self, response):
        consume_cash = int(self.table.const_info.get(GAMECOMMON.ARENA_REFRESH_COST).value)
        self.w_db['profile'].decrease_cash(self.userid, consume_cash)
        db_profile = self.w_db['profile'].find_profile(self.userid)
        response.skip_match_arena_normal.remain_cash = db_profile.cash
        response.result = Response.SUCCESS
        return

    def Start_Battle(self, request, response):
        req_target_uid = request.start_battle_arena_normal.target_uid
        # TODO : 전투 씬 - 퍼즐판에 진입. 기존 로직 전부삭제 및 redis, rdb 고려하여 재구현.
        # 티켓 차감 로직만 일단 살리고 해당 부분도 리팩토링
        # 전투 시작 종료 로직에 타겟 유저를 다시 찾는 로직을 섞지 않는다 - 패킷으로 분리 해둠.
        # 오직 자원차감, 보상지급, 전투 종료시 랭크 변경만 함.
        db_profile = self.w_db['profile'].select_column(self.userid, "arena_ticket, arena_ticket_time, level")
        if not db_profile:
            response.result = Response.USER_INVALID
            return

        db_arena_normal = self.w_db['arenanormal'].get_arena_info(self.userid)
        if not db_arena_normal:
            response.result = Response.DB_NOT_EXIST
            return

        db_arena_target = self.w_db['arenanormal'].get_arena_info(req_target_uid)
        if not db_arena_target:
            response.result = Response.DB_NOT_EXIST
            return

        if db_arena_target.rank > db_arena_normal.rank:
            response.result = Response.FAILURE # TODO: 대상이 랭크값이 큼. 상대방이 나보다 랭크가 낮으므로 에러코드 추가 및 처리
            return

        arena_ticket_max = int(self.table.const_info.get(GAMECOMMON.ARENA_TICKET_MAX).value)
        arena_charge_time = int(self.table.const_info.get(GAMECOMMON.ARENA_CHARGE_TIME).value)

        # TODO: 코드 최적화 및 리팩토링 필요
        self.w_db['arenanormal'].set_battle_target(auid=self.userid, target_uid=req_target_uid, battle_time=self.begin)
        self.w_db['arenanormal'].set_battle_target(auid=req_target_uid, target_uid=self.userid, battle_time=self.begin)

        ticket, ticket_time = ServiceArenaNormal.__get_arena_ticket(self, db_profile, arena_ticket_max, 0)
        res_update_ticket = ticket - 1
        if 0 > res_update_ticket:
            response.result = Response.ARENA_TICKET_LACK
            return

        if not ticket_time:
            ticket_time = self.begin

        db_update = []
        value_list = []

        db_update.append('last_mode')
        value_list.append(GAMECOMMON.PLAY_MODE_ARENA_NORMAL)

        db_update.append('arena_ticket')
        value_list.append(res_update_ticket)

        str_column = "arena_ticket_time=NULL"
        if ticket_time != None:
            str_column = "arena_ticket_time='%s'" % (ticket_time)
            res_arena_ticket_time = self.next_charge_second(ticket_time, arena_charge_time)
        
        self.w_db['profile'].select_column(self.userid, "arena_ticket, arena_ticket_time")
        self.w_db['profile'].update_user_column(self.userid, db_update, value_list, str_column)

        response.start_battle_arena_normal.arena_ticket = res_update_ticket
        response.start_battle_arena_normal.arena_ticket_time = res_arena_ticket_time
        response.result = Response.SUCCESS
        return

    def End_Battle(self, request, response):
        req_win_flag = request.end_battle_arena_normal.win_flag
        # TODO : 전투 씬 - 퍼즐판에서 나옴. 기존 로직 전부삭제 및 redis, rdb 고려하여 재구현.
        # 보상 지급 및 보상 받은 정보만 패킷 리턴 해당 부분도 리팩토링
        # 전투 시작 종료 로직에 타겟 유저를 다시 찾는 로직을 섞지 않는다. - 패킷으로 분리 해둠.
        # 오직 자원차감, 보상지급, 전투 종료시 랭크 변경만 함.

        db_arena_normal = self.w_db['arenanormal'].get_arena_info(self.userid)
        if not db_arena_normal:
            response.result = Response.DB_NOT_EXIST
            return

        db_arena_target = self.w_db['arenanormal'].get_arena_info(db_arena_normal.battle_target_uid)
        if not db_arena_target:
            response.result = Response.DB_NOT_EXIST
            return

        my_battle_record = convert_string_to_array(db_arena_normal.battle_record)
        if 10 <= len(my_battle_record):
            del my_battle_record[0]

        target_battle_record = convert_string_to_array(db_arena_target.battle_record)
        if 10 <= len(target_battle_record):
            del target_battle_record[0]

        res_arena_reward = 0
        if req_win_flag:
            res_arena_reward = int(self.table.const_info.get(GAMECOMMON.ARENA_NORMAL_WIN_REWARD).value)
            
            # 전투 레코드 기록 (로직 파악 후 최적화)
            my_battle_record.append([1, 1, db_arena_target.auid, db_arena_normal.rank, db_arena_target.rank])
            target_battle_record.append([0, 0, db_arena_normal.auid, db_arena_target.rank, db_arena_normal.rank])

            # 나와 대상의 랭크를 바꿈, 전투 레코드 기록
            self.w_db['arenanormal'].arena_battle_end_change_rank(self.userid, db_arena_target.rank, str(my_battle_record))
            self.w_db['arenanormal'].arena_battle_end_change_rank(db_arena_target.auid, db_arena_normal.rank, str(target_battle_record))
        else:
            res_arena_reward = int(self.table.const_info.get(GAMECOMMON.ARENA_NORMAL_LOSE_REWARD).value)
            
            # 전투 레코드 기록 (로직 파악 후 최적화)
            my_battle_record.append([1, 0, db_arena_target.auid, db_arena_normal.rank, db_arena_target.rank])
            target_battle_record.append([0, 1, db_arena_normal.auid, db_arena_target.rank, db_arena_normal.rank])

            # 전투 레코드 기록, 랭크 교체 없음.
            self.w_db['arenanormal'].arena_battle_end(self.userid, str(my_battle_record))
            self.w_db['arenanormal'].arena_battle_end(db_arena_target.auid, str(target_battle_record))

        # 코인 보상 지급 (승,패)
        self.w_db['etcinven'].add_item(self.userid, GAMECOMMON.ITEM_ARENA_COIN, res_arena_reward)

        # 승패에 따라서 랭크가 바뀌거나 유지된 나의 아레나 일반 랭크 구함
        after_arena_normal = self.w_db['arenanormal'].get_arena_info(self.userid)

        response.end_battle_arena_normal.change_rank = after_arena_normal.rank
        response.end_battle_arena_normal.reward_item.item_id = GAMECOMMON.ITEM_ARENA_COIN
        response.end_battle_arena_normal.reward_item.count = res_arena_reward
        response.result = Response.SUCCESS
        return

    def Get_Ranking(self, response):
        # TODO: 로직 검토 및 재구현 (redis rdb 이원화 제거)
        rank_users = self.arena_clone.arena_normal_rank_range(1, 10)
        for rank in rank_users:
            user_redis = self.cache_clone.get_user_profile(int(rank[0]))
            if not user_redis:
                continue

            rank_user = response.arena_ranking_list.total_rank.add()
            rank_user.uid = int(rank[0])
            rank_user.name = user_redis[GAMECOMMON.R_USER_NICK]
            rank_user.rank = int(rank[1])
            rank_user.avatar_id = int(user_redis[GAMECOMMON.R_USER_AVATAR_ID])

        my_rank = self.arena_clone.get_arena_normal_rank(self.userid)
        if my_rank < 5:
            min_rank = 1
        else:
            min_rank = my_rank - 5
            min_rank = max(1, min_rank)

        max_rank = my_rank + 5
        between_rank = self.arena_clone.arena_normal_rank_range(min_rank, max_rank)
        for rank in between_rank:
            user_redis = self.cache_clone.get_user_profile(int(rank[0]))
            if not user_redis:
                continue

            rank_user = response.arena_ranking_list.between_rank.add()
            rank_user.uid = int(rank[0])
            rank_user.name = user_redis[GAMECOMMON.R_USER_NICK]
            rank_user.rank = int(rank[1])
            rank_user.avatar_id = int(user_redis[GAMECOMMON.R_USER_AVATAR_ID])

        response.result = Response.SUCCESS
        return

    def Get_Record(self, response):
        db_arena_normal = self.w_db['arenanormal'].get_arena_info(self.userid)
        if not db_arena_normal:
            response.result = Response.USER_INVALID
            return

        history = convert_string_to_array(db_arena_normal.battle_record)
        for info in history:
            battle_info = response.arena_record_list.history_list.add()
            battle_info.attacker = int(info[0])
            battle_info.win_flag = int(info[1])
            target_redis = self.cache_clone.get_user_data(info[2], GAMECOMMON.R_USER_NICK)
            battle_info.name = target_redis if target_redis else ""
            battle_info.my_rank = int(info[3])
            battle_info.target_rank = int(info[4])
            battle_info.targetUid = int(info[2])

        response.result = Response.SUCCESS
        return

    def Get_Reward(self, response):
        db_arena_normal = self.w_db['arenanormal'].get_arena_info(self.userid)
        if not db_arena_normal:
            response.result = Response.USER_INVALID
            return

        reward_time = int(self.table.const_info.get(GAMECOMMON.ARENA_NORMAL_REWARD_TERM).value)
        if reward_time > time_diff_in_seconds(db_arena_normal.reward_time):
            response.result = Response.TIME_ERROR
            return

        reward_id = ServiceArenaNormal.__arena_normal_rank_reward(self, db_arena_normal.rank)
        item_dict = self.get_reward_list(reward_id)
        self.reward_packet_process(
            item_dict,
            response.arena_reward.reward_item
        )
        self.w_db['arenanormal'].update_arena_reward_time(self.userid, datetime.now())

        response.arena_reward.reward_time = reward_time
        response.result = Response.SUCCESS
        return

    def Get_HOF(self, request, response):
        # TODO: 로직 구현 후 다시 작업 (redis rdb 이원화 제거)
        redis_hall_of_fame = self.arena_clone.get_hall_of_fame_data(GAMECOMMON.ARENA_HALL_OF_FAME)
        if not redis_hall_of_fame:
            response.arena_hall_of_fame.season = 0
            response.result = Response.SUCCESS
            return

        last_season = int(redis_hall_of_fame[GAMECOMMON.ARENA_LAST_SEASON])
        response.arena_hall_of_fame.season = last_season - (request.arena_hall_of_fame.page-1)
        hall_of_fame_list = convert_string_to_dict(redis_hall_of_fame[GAMECOMMON.ARENA_HALL_OF_FAME_LIST])
        if len(hall_of_fame_list) < request.arena_hall_of_fame.page:
            response.arena_hall_of_fame.season = 0
            response.result = Response.SUCCESS
            return

        rank = 1

        for auid in hall_of_fame_list[request.arena_hall_of_fame.page - 1]:
            if 0 == auid:
                continue

            redis_data = self.cache_clone.get_user_profile(auid)
            if not redis_data:
                normalMatch = response.arena_hall_of_fame.user_list.add()
                normalMatch.rank = rank
                normalMatch.name = ''
                normalMatch.level = 0
                normalMatch.avatar_id = 0
                normalMatch.uid = 0

                rank += 1
                continue

            normalMatch = response.arena_hall_of_fame.users.add()
            normalMatch.rank = rank
            normalMatch.name = redis_data[GAMECOMMON.R_USER_NICK]
            normalMatch.level = int(redis_data[GAMECOMMON.R_USER_LEVEL])
            normalMatch.avatar_id = int(redis_data[GAMECOMMON.R_USER_AVATAR_ID])
            normalMatch.uid = int(auid)
            
            # TODO: deck 구조체를 사용할 방법 고안 - Redis? Mysql? 
            # 명예의 전당 정보에 해당 타유저의 덱 정보가 필요하다면 추가

            # TODO: redis team info 삭제 예정
            # team_info = redis_data[GAMECOMMON.R_USER_TEAM_INFO]
            # self.convert_team_data_redis_to_protobuf(normalMatch.team_info, team_info)

            if 0 != int(redis_data[GAMECOMMON.R_USER_GUILD_UID]):
                guild_redis = self.guild_clone.get_guild_info(redis_data[GAMECOMMON.R_USER_GUILD_UID])
                if guild_redis:
                    normalMatch.guildinfo.guild_name = guild_redis[GAMECOMMON.GUILD_NAME]
                    normalMatch.guildinfo.guild_bg = int(guild_redis[GAMECOMMON.GUILD_BG])
                    normalMatch.guildinfo.guild_emblem = int(guild_redis[GAMECOMMON.GUILD_EMBLEM])

            rank += 1

        response.result = Response.SUCCESS
        return
