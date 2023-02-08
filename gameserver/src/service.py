# -*- coding: utf-8 -*-
import functools
import json
import pprint
import sys
import traceback
from datetime import datetime
from functools import wraps

from google.protobuf.json_format import MessageToDict

from src.common.util import *
from src.protocol.webapp_pb import Request, Response
from src.services.service_account import *
from src.services.service_arena import *
from src.services.service_arena_normal import *
from src.services.service_attend import *
from src.services.service_collection import *
from src.services.service_common import *
from src.services.service_darknest import *
from src.services.service_endless_tower import *
from src.services.service_equip import *
from src.services.service_event import *
from src.services.service_event_dungeon import *
from src.services.service_farming_tower import *
from src.services.service_gacha import *
from src.services.service_guild import *
from src.services.service_guild_contest import *
from src.services.service_guild_raid import *
from src.services.service_hero import *
from src.services.service_inventory import *
from src.services.service_make import *
from src.services.service_post import *
from src.services.service_region import *
from src.services.service_research import *
from src.services.service_resource import *
from src.services.service_shop import *
from src.services.service_territory import *
from src.services.service_trade import *
from src.services.service_user import *

INDENT = 4*' '
def stacktrace(func):
    @functools.wraps(func)
    def wrapped(*args, **kwds):
        callstack = '\n'.join([INDENT+line.strip() for line in traceback.format_stack()][:-1])
        return func(*args, **kwds)
    return wrapped


G_PROCS = {}
def register_process(command):
    def register(func):
        G_PROCS[command] = func
        return func
    return register


def check_field(func):
    @wraps(func)
    def check_field_func(self, request, response):
        if request.serial == -999 or request.session_id == -999:
            return func(self, request, response)
        if request.HasField(func.__name__):
            return func(self, request, response)
        else:
            self.logger.error("request.HasField(ip:%s, command:%s, func_name:%s)" % (self.peer, request.command, func.__name__))
            return True
    return check_field_func


def check_userid(func):
    @wraps(func)
    def check_userid_func(self, request, response):
        if request.serial == -999 or request.session_id == -999:
            return func(self, request, response)

        session_info = self.session_clone.get_session_info(request.session_id, self.session, request.serial)
        if not session_info:
            response.result = Response.SESSION_EXPIRED
            return

        self.userid = int(session_info[0])
        self.nickname = session_info[1]
        func(self, request, response)
        response.userid = self.userid
        response.nickname = self.nickname
    return check_userid_func


def check_event(func):
    @wraps(func)
    def check_field_func(self, request, response):
        func(self, request, response)
    return check_field_func


def check_exp(func):
    @wraps(func)
    def check_exp_wrapper(self, request, response):
        func(self, request, response)
    return check_exp_wrapper

class WebAppService(ServiceCommon):
    def __init__(self, context):
        ServiceCommon.__init__(self)
        ServiceUser.__init__(self) 
        ServiceHero.__init__(self, context)
        ServiceInventory.__init__(self)
        ServiceTrade.__init__(self)
        ServiceTerritory.__init__(self)
        ServiceArena.__init__(self)
        
        self.userid = None
        self.nickname = None
        self.begin = datetime.now()
        self.context = context
        self.table = context.table
        
        self.peer = None
        self.user_agent = None
        
        self.w_db = context.w_db
        # self.r_db = context.r_db

        self.session = context.session
        self.session_clone = context.session_clone

        self.cache = context.cache
        self.cache_clone = context.cache_clone

        self.guild = context.guild
        self.guild_clone = context.guild_clone

        # TODO : 서버 서비스 코드에서 현재 안씀
        # self.event_redis = context.event_redis
        # self.event_clone_redis = context.event_clone_redis

        self.arena = context.arena
        self.arena_clone = context.arena_clone

        self.arena_tournament = context.arena_tournament
        self.arena_tournament_clone = context.arena_tournament_clone

    def set_peer(self, peer):
        self.peer = peer

    def set_user_agent(self, user_agent):
        self.user_agent = user_agent

    def process_raw_request(self, raw_request):
        self.begin = datetime.now()
        request = Request()
        try:
            request.ParseFromString(raw_request)
        except Exception as e:
            self.logger.exception("process_raw_request. request.ParseFromString {}".format(e.message))
            return None

        raw_response = self.process_request(request).SerializeToString()
        return raw_response

    def process_request(self, request):
        response = Response()
        response.command = request.command
        response.serial = request.serial
        response.result = Response.FAILURE

        try:
            G_PROCS.get(request.command)(self, request, response)
        except Exception as e:
            self.logger.error("Package command Error : ", e)

        requestStr = json.dumps(MessageToDict(request))
        print(requestStr, file=sys.stderr)
        
        resonseStr = json.dumps(MessageToDict(response))
        print(resonseStr, file=sys.stderr)
        
        return response




    @register_process(Request.CHECK_VERSION)
    @check_field
    def check_version(self, request, response):
        ServiceAccount.CheckVerison(self, request, response)

    @register_process(Request.CHECK_UPDATE)
    @check_userid
    def check_update(self, request, response):
        ServiceAccount.CheckUpdate(self, response)
    
    @register_process(Request.PUSH_ALRAM_AGREE)
    @check_userid
    @check_field
    def push_alram_agree(self, request, response):
        ServiceAccount.PushAlramAgree(self, request, response)

    @register_process(Request.LOGIN_USER)
    @check_field
    def login_user(self, request, response):
        ServiceUser.LoginUser(self, request, response)

    @register_process(Request.REGISTER_USER)
    @check_field
    def register_user(self, request, response):
        ServiceUser.RegisterUser(self, request, response)

    @register_process(Request.GET_PROFILE) # 유저 모든정보
    @check_userid
    def get_profile(self, request, response): # 코어코드 : req가 없어도 일단 param 갯수를 맞춰야 함
        ServiceUser.GetProfile(self, response)

    @register_process(Request.GET_USER_PROFILE) # 유저 간단정보
    @check_userid
    @check_field
    def get_user_profile(self, request, response):
        ServiceUser.GetUserProfile(self, request, response)

    @register_process(Request.NICK_NAME_CHANGE)
    @check_userid
    @check_field
    def nick_name_change(self, request, response):
        ServiceUser.ChangeNickName(self, request, response)

    @register_process(Request.AVATAR_CHANGE)
    @check_userid
    @check_field
    def avatar_change(self, request, response):
        ServiceUser.ChangeAvatar(self, request, response)

    @register_process(Request.USE_CASH)
    @check_userid
    @check_field
    def use_cash(self, request, response): # 범용적으로 여기저기서 보석을 사용할때 사용됨 (지역다시하기 유료재화, 등)
        ServiceUser.UseCash(self, request, response)

    @register_process(Request.CHARGE_AMOUNT)
    @check_userid
    @check_field
    def charge_amount(self, request, response): # 보석을 사용하여 스테미너 충전, 티켓 충전, 등을 진행할때 사용한다.
        ServiceUser.ChargeAmount(self, request, response)

    @register_process(Request.USER_LEVEL_REWARD)
    @check_userid
    def user_level_reward(self, request, response):
        ServiceUser.UserLevelReward(self, request, response)

    @register_process(Request.ATTEND_INFO)
    @check_userid
    def attend_info(self, request, response):
        ServiceAttend.AttendInfo(self, response)

    @register_process(Request.ATTEND_REWARD)
    @check_userid
    def continue_attend_reward(self, request, response):
        ServiceAttend.ContinueAttendReward(self, response)

    @register_process(Request.GET_INVENTORY)
    @check_userid
    @check_field
    def get_inventory(self, request, response):
        ServiceInventory.GetInventory(self, request, response)

    @register_process(Request.EXTEND_INVEN)
    @check_userid
    @check_field
    def extend_inven(self, request, response):
        ServiceInventory.ExtendInven(self, request, response)

    @register_process(Request.HERO_EXP)
    @check_userid
    @check_field
    def hero_exp(self, request, response):
        ServiceHero.HeroExp(self, request, response)

    @register_process(Request.HERO_PROMOTION)
    @check_userid
    @check_field
    def hero_promotion(self, request, response):
        ServiceHero.HeroPromotion(self, request, response)

    @register_process(Request.HERO_LOCK)
    @check_userid
    @check_field
    def hero_lock(self, request, response):
        ServiceHero.HeroLock(self, request, response)

    @register_process(Request.HERO_RETURN)
    @check_userid
    @check_field
    def hero_return(self, request, response):
        ServiceHero.HeroReturn(self, request, response)

    @register_process(Request.GET_HERO_PASSIVE_SKILL)
    @check_userid
    @check_field
    def get_hero_passive_skill(self, request, response):
        ServiceHero.GetHeroPassiveSkill(self, request, response)

    @register_process(Request.CONFIRM_HERO_PASSIVE_SKILL)
    @check_userid
    @check_field
    def confirm_hero_passive_skill(self, request, response):
        ServiceHero.ConfirmHeroPassiveSkill(self, request, response)

    @register_process(Request.EXTRACT_HERO_EXP)
    @check_userid
    @check_field
    def extract_hero_exp(self, request, response):
        ServiceHero.ExtractHeroExp(self, request, response)


    @register_process(Request.GET_HERO_POTENTIAL_STAT)
    @check_userid
    @check_field
    def get_hero_potential_stat(self, request, response):
        ServiceHero.GetHeroPotentialStat(self, request, response)

    @register_process(Request.EXCHANGE_HERO_POTENTIAL_STAT)
    @check_userid
    @check_field
    def exchange_hero_potential_stat(self, request, response):
        ServiceHero.ExchangeHeroPotentialStat(self, request, response)

    @register_process(Request.CONFIRM_HERO_POTENTIAL_STAT)
    @check_userid
    @check_field
    def confirm_hero_potential_stat(self, request, response):
        ServiceHero.ConfirmHeroPotentialStat(self, request, response)


    @register_process(Request.SAVE_REGION)
    @check_userid
    @check_field
    def save_region(self, request, response):
        ServiceRegion.SaveRegion(self, request, response)

    @register_process(Request.START_REGION)
    @check_userid
    @check_field
    def start_region(self, request, response):
        ServiceRegion.StartRegion(self, request, response)

    @register_process(Request.REWARD_REGION)
    @check_userid
    def reward_region(self, request, response):
        ServiceRegion.RewardRegion(self, request, response)

    @register_process(Request.REGION_MISSION_REWARD)
    @check_userid
    @check_field
    def region_mission_reward(self, request, response):
        ServiceRegion.RegionMissionReward(self, request, response)

    @register_process(Request.REGION_MISSION_CLEAR_INFO)
    @check_userid
    def region_mission_clear_info(self, request, response):
        ServiceRegion.RegionMissionClearInfo(self, response)

    @register_process(Request.REGION_REWARD_CHECK)
    @check_userid
    def region_reward_check(self, request, response):
        ServiceRegion.RegionRewardCheck(self, response)

    @register_process(Request.RESOURCEAREA_LIST)
    @check_userid
    def resourcearea_list(self, request, response):
        ServiceResource.ResourceAreaList(self, response)

    @register_process(Request.RESOURCE_DISPATCH)
    @check_userid
    @check_field
    def resource_dispatch(self, request, response):
        ServiceResource.ResourceDispatch(self, request, response)

    @register_process(Request.RESOURCE_RETURN)
    @check_userid
    @check_field
    def resource_return(self, request, response):
        ServiceResource.ResourceReturn(self, request, response)

    @register_process(Request.RESOURCE_REWARD)
    @check_userid
    @check_field
    def resource_reward(self, request, response):
         ServiceResource.ResourceReward(self, request, response)

    @register_process(Request.SUMMON_GACHA)
    @check_userid
    @check_field
    def summon_gacha(self, request, response):
        ServiceGacha.SummonGacha(self, request, response)

    @register_process(Request.SUMMON_GACHA_LIST)
    @check_userid
    def summon_gacha_list(self, request, response):
        ServiceGacha.SummonGachaList(self, response)

    @register_process(Request.EQUIP_LOCK)
    @check_userid
    @check_field
    def equip_lock(self, request, response):
        ServiceEquip.EquipLock(self, request, response)

    @register_process(Request.EQUIP_EXP)
    @check_userid
    @check_field
    def equip_exp(self, request, response):
        ServiceEquip.EquipExp(self, request, response)

    @register_process(Request.EQUIP_ENCHANT)
    @check_userid
    @check_field
    def equip_enchant(self, request, response):
        ServiceEquip.EquipEnchant(self, request, response)

    @register_process(Request.TERRITORY_BUILD)
    @check_userid
    @check_field
    def territory_build(self, request, response):
        ServiceTerritory.TerritoryBuild(self, request, response)

    @register_process(Request.TERRITORY_REWARD)
    @check_userid
    @check_field
    def territory_reward(self, request, response):
        ServiceTerritory.TerritoryReward(self, request, response)

    @register_process(Request.TERRITORY_BUILDING_LIST)
    @check_userid
    def territory_building_list(self, request, response):
        ServiceTerritory.TerritoryBuildList(self, response)

    @register_process(Request.TRADE_ITEM_LIST)
    @check_userid
    @check_field
    def trade_item_list(self, request, response):
        ServiceTrade.TradeItemList(self, request, response)

    @register_process(Request.TRADE_ITEM_BUY)
    @check_userid
    @check_field
    def trade_item_buy(self, request, response):
        ServiceTrade.TradeItemBuy(self, request, response)

    @register_process(Request.MAKE_ITEM)
    @check_userid
    @check_field
    def make_item(self, request, response):
        ServiceMake.MakeItem(self, request, response)

    @register_process(Request.MAKE_ITEM_REWARD)
    @check_userid
    @check_field
    def make_item_reward(self, request, response):
        ServiceMake.MakeItemReward(self, request, response)

    @register_process(Request.MAKE_ITEM_CANCEL)
    @check_userid
    @check_field
    def make_item_cancel(self, request, response):
        ServiceMake.MakeItemCancel(self, request, response)

    @register_process(Request.MAKE_ITEM_LIST)
    @check_userid
    def make_item_list(self, request, response):
        ServiceMake.MakeItemList(self, request, response)

    @register_process(Request.MAKE_QUICK_COMPLET)
    @check_userid
    @check_field
    def make_quick_complet(self, request, response):
        ServiceMake.MakeQuickComplet(self, request, response)

    @register_process(Request.GUILD_CREATE)
    @check_userid
    @check_field
    def guild_create(self, request, response):
        ServiceGuild.GuildCreate(self, request, response)

    @register_process(Request.GUILD_JOIN)
    @check_userid
    @check_field
    def guild_join(self, request, response):
        ServiceGuild.GuildJoin(self, request, response)

    @register_process(Request.GUILD_WITHDRAW)
    @check_userid
    def guild_withdraw(self, request, response):
       ServiceGuild.GuildWithDraw(self, request, response)

    @register_process(Request.GUILD_MEMBER_KICK)
    @check_userid
    @check_field
    def guild_member_kick(self, request, response):
        ServiceGuild.GuildMemberKick(self, request, response)

    @register_process(Request.GUILD_MEMBER_ACCEPT)
    @check_userid
    @check_field
    def guild_member_accept(self, request, response):
        ServiceGuild.GuildMemberAccept(self, request, response)

    @register_process(Request.GUILD_MEMBER_REFUSAL)
    @check_userid
    @check_field
    def guild_member_refusal(self, request, response):
        ServiceGuild.GuildMemberRefusal(self, request, response)

    @register_process(Request.GUILD_MEMBER_CHANGE_GRADE)
    @check_userid
    @check_field
    def guild_member_change_grade(self, request, response):
        ServiceGuild.GuildMemberChangeGrade(self, request, response)

    @register_process(Request.GUILD_JOIN_CONDITION)
    @check_userid
    @check_field
    def guild_join_condition(self, request, response):
        ServiceGuild.GuildJoinCondition(self, request, response)

    @register_process(Request.GUILD_MSG_MODIFY)
    @check_userid
    @check_field
    def guild_msg_modify(self, request, response):
        ServiceGuild.GuildMSGModify(self, request, response)

    @register_process(Request.GUILD_INFO_MODIFY)
    @check_userid
    @check_field
    def guild_info_modify(self, request, response):
        ServiceGuild.GuildInfoModify(self, request, response)

    @register_process(Request.GET_GUILD_INFO)
    @check_userid
    @check_field
    def get_guild_info(self, request, response):
        ServiceGuild.GetGuildInfo(self, request, response)

    @register_process(Request.GUILD_MEMBER_LIST)
    @check_userid
    @check_field
    def guild_member_list(self, request, response):
        ServiceGuild.GuildMemberList(self, request, response)

    @register_process(Request.GUILD_RECOMMEND_LIST)
    @check_userid
    def guild_recommend_list(self, request, response):
        ServiceGuild.GuildRecommendList(self, response)

    @register_process(Request.GUILD_SEARCH)
    @check_userid
    def guild_search(self, request, response):
        ServiceGuild.GuildSearch(self, request, response)

    @register_process(Request.GUILD_RAID_INFO)
    @check_userid
    def guild_raid_info(self, request, response):
        ServiceGuildRaid.GuildRaidInfo(self, response)

    @register_process(Request.GUILD_RAID_START)
    @check_userid
    def guild_raid_start(self, request, response):
        ServiceGuildRaid.GuildRaidStart(self, response)

    @register_process(Request.GUILD_RAID_END)
    @check_userid
    @check_field
    def guild_raid_end(self, request, response):
        ServiceGuildRaid.GuildRaidEnd(self, request, response)

    @register_process(Request.GUILD_RAID_DAMAGE_LIST)
    @check_userid
    def guild_raid_damage_list(self, request, response):
        ServiceGuildRaid.GuildRaidDamageList(self, response)

    @register_process(Request.GUILD_RAID_REWARD)
    @check_userid
    def guild_raid_reward(self, request, response):
        ServiceGuildRaid.GuildRaidReward(self, response)

    @register_process(Request.GUILD_CONTEST_INFO)
    @check_userid
    def guild_contest_info(self, request, response):
        ServiceGuildContest.GuildContestInfo(self, response)

    @register_process(Request.GUILD_CONTEST_START)
    @check_userid
    def guild_contest_start(self, request, response):
        ServiceGuildContest.GuildContestStart(self, response)

    @register_process(Request.GUILD_CONTEST_END)
    @check_userid
    def guild_contest_end(self, request, response):
        ServiceGuildContest.GuildContestEnd(self, request, response)

    @register_process(Request.GUILD_CONTEST_REWARD)
    @check_userid
    def guild_contest_reward(self, request, response):
        ServiceGuildContest.GuildContestReward(self, response)

    @register_process(Request.GET_FARMING_TOWER)
    @check_userid
    def get_farming_tower(self, request, response):
        ServiceFarmingTower.GetFarmingTower(self, response)

    @register_process(Request.START_FARMING_TOWER)
    @check_userid
    @check_field
    def start_farming_tower(self, request, response):
        ServiceFarmingTower.StartFarmingTower(self, request, response)

    @register_process(Request.CLEAR_FARMING_TOWER)
    @check_userid
    @check_field
    def clear_farming_tower(self, request, response):
        ServiceFarmingTower.ClearFarmingTower(self, request, response)

    @register_process(Request.GET_ENDLESS_TOWER)
    @check_userid
    def get_endless_tower(self, request, response):
        ServiceEndlessTower.GetEndlessTower(self, response)

    @register_process(Request.START_ENDLESS_TOWER)
    @check_userid
    @check_field
    def start_endless_tower(self, request, response):
       ServiceEndlessTower.StartEndlessTower(self, request, response)

    @register_process(Request.CLEAR_ENDLESS_TOWER)
    @check_userid
    @check_field
    def clear_endless_tower(self, request, response):
        ServiceEndlessTower.ClearEndlessTower(self, request, response)

    @register_process(Request.START_EVENT_DUNGEON)
    @check_userid
    @check_field
    def start_event_dungeon(self, request, response):
        ServiceEventDungeon.StartEventDungeon(self, request, response)

    @register_process(Request.END_EVENT_DUNGEON)
    @check_userid
    @check_field
    def end_event_dungeon(self, request, response):
        ServiceEventDungeon.EndEventDungeon(self, request, response)

    @register_process(Request.GET_EVENT_DUNGEON)
    @check_userid
    def get_event_dungeon(self, request, response):
        ServiceEventDungeon.GetEventDungeon(self, request, response)

    @register_process(Request.EVENT_DUNGEON_REWARD)
    @check_userid
    @check_field
    def event_dungeon_reward(self, request, response):
        ServiceEventDungeon.EventDungeonReward(self, request, response)

    @register_process(Request.DARKNEST_INFO)
    @check_userid
    def darknest_info(self, request, response):
        ServiceDarknest.DarknestInfo(self, response)

    @register_process(Request.DARKNEST_START)
    @check_userid
    @check_exp
    def darknest_start(self, request, response):
        ServiceDarknest.DarknestStart(self, response)

    @register_process(Request.DARKNEST_END)
    @check_userid
    @check_field
    @check_exp
    def darknest_end(self, request, response):
        ServiceDarknest.DarknestEnd(self, response)

    @register_process(Request.DARKNEST_NEXT_LEVEL)
    @check_userid
    @check_field
    def darknest_next_level(self, request, response):
        ServiceDarknest.DarknestNextLevel(self, request, response)

    @register_process(Request.GET_POST_LIST)
    @check_userid
    def get_post_list(self, request, response):
        ServicePost.GetPostList(self, response)

    @register_process(Request.RECEIVE_POST)
    @check_userid
    @check_field
    def receive_post(self, request, response):
        ServicePost.ReceivePost(self, request, response)

    @register_process(Request.REWARD_POST)
    @check_userid
    @check_field
    def reward_post(self, request, response):
        ServicePost.RewardPost(self, request, response)

    @register_process(Request.CLEAN_UP_POST)
    @check_userid
    def clean_up_post(self, request, response):
        ServicePost.CleanUpPost(self, request, response)

    @register_process(Request.DELETE_POST)
    @check_userid
    @check_field
    def delete_post(self, request, response):
        ServicePost.DeletePost(self, request, response)

    @register_process(Request.EVENT_LIST)
    @check_userid
    def event_list(self, request, response):
        ServiceEvent.EventList(self, response)

    @register_process(Request.EVENT_REWARD)
    @check_userid
    @check_field
    def event_reward(self, request, response):
        ServiceEvent.EventReward(self, request, response)

    @register_process(Request.RETURN_POINT_BUY_ITEM)
    @check_userid
    @check_field
    def return_point_buy_item(self, request, response):
        ServiceShop.ReturnPointBuyItem(self, request, response)

    @register_process(Request.ARENA_COIN_BUY_ITEM)
    @check_userid
    @check_field
    def arena_coin_buy_item(self, request, response):
        ServiceShop.ArenaCoinBuyItem(self, request, response)

    @register_process(Request.COLLECTION_INFO)
    @check_userid
    @check_field
    def collection_info(self, request, response):
        ServiceCollection.CollectionInfo(self, request, response)

    @register_process(Request.COLLECTION_REWARD)
    @check_userid
    @check_field
    def collection_reward(self, request, response):
        ServiceCollection.CollectionReward(self, request, response)

    @register_process(Request.CHECK_ENTER_ARENA) # 메인화면에서 아레나 버튼 누를시 레벨체크
    @check_userid
    def check_enter_arena(self, request, response):
        ServiceArena.CheckEnterArena(self, response)

    @register_process(Request.UPDATE_TEAM_INFO)
    @check_userid
    @check_field
    def update_team_info(self, request, response): # 현재는 아레나 방어팀 셋팅 전용으로 쓰이고 있음. (아레나 일반전, 토너먼트, 리그에서 공용으로 쓰일 가능성 있음)
        ServiceArena.UpdateTeamInfo(self, request, response)

    @register_process(Request.GET_ARENA_INFO)
    @check_userid
    @check_field
    def get_arena_info(self, request, response):
        ServiceArena.GetArenaInfo(self, request, response)

    @register_process(Request.GET_ARENA_MATCH_LIST)
    @check_userid
    @check_field
    def get_arena_match_list(self, request, response): # 아레나 상대방 다시찾기 할때 불림
        ServiceArena.GetArenaMatchList(self, request, response)

    @register_process(Request.START_ARENA_BATTLE)
    @check_userid
    @check_field
    def start_arena_battle(self, request, response):
        ServiceArena.StartArenaBattle(self, request, response)

    @register_process(Request.END_ARENA_BATTLE)
    @check_userid
    @check_field
    def end_arena_battle(self, request, response):
        ServiceArena.EndArenaBattle(self, request, response)

    @register_process(Request.ARENA_RANKING_LIST)
    @check_userid
    @check_field
    def arena_ranking_list(self, request, response):
        ServiceArena.ArenaRankingList(self, request, response)

    @register_process(Request.ARENA_RECORD_LIST)
    @check_userid
    @check_field
    def arena_record_list(self, request, response):
        ServiceArena.ArenaRecordList(self, request, response)

    @register_process(Request.ARENA_REWARD)
    @check_userid
    @check_field
    def arena_reward(self, request, response):
        ServiceArena.ArenaReward(self, request, response)

    @register_process(Request.ARENA_HALL_OF_FAME)
    @check_userid
    @check_field
    def arena_hall_of_fame(self, request, response):
        ServiceArenaNormal.ArenaHallofFame(self, request, response) # 아레나 일반전 명예의 전당

    #TODO: 아레나 리펙토링 메서드
    @register_process(Request.GET_DECK_ARENA_NORMAL)
    @check_userid
    def get_deck_arena_normal(self, request, response):
        ServiceArenaNormal.Get_Deck(self, response)

    @register_process(Request.UPDATE_DECK_ARENA_NORMAL)
    @check_userid
    @check_field
    def update_deck_arena_normal(self, request, response):
        ServiceArenaNormal.Update_Deck(self, request, response)

    @register_process(Request.GET_MATCH_ARENA_NORMAL)
    @check_userid
    @check_field
    def get_match_arena_normal(self, request, response):
        ServiceArenaNormal.Get_Match(self, request, response)

    @register_process(Request.SEARCH_MATCH_ARENA_NORMAL)
    @check_userid
    def search_match_arena_normal(self, request, response):
        ServiceArenaNormal.Search_Match(self, response)

    @register_process(Request.REFRESH_MATCH_ARENA_NORMAL)
    @check_userid
    def refresh_match_arena_normal(self, request, response):
        ServiceArenaNormal.Refresh_Match(self, response)

    @register_process(Request.SKIP_MATCH_ARENA_NORMAL)
    @check_userid
    def skip_match_arena_normal(self, request, response):
        ServiceArenaNormal.Skip_Match(self, response)

    @register_process(Request.START_BATTLE_ARENA_NORMAL)
    @check_userid
    @check_field
    def start_battle_arena_normal(self, request, response):
        ServiceArenaNormal.Start_Battle(self, request, response)

    @register_process(Request.END_BATTLE_ARENA_NORMAL)
    @check_userid
    @check_field
    def end_battle_arena_normal(self, request, response):
        ServiceArenaNormal.End_Battle(self, request, response)

    @register_process(Request.GET_RANKING_ARENA_NORMAL)
    @check_userid
    def get_ranking_arena_normal(self, request, response):
        ServiceArenaNormal.Get_Ranking(self, response)

    @register_process(Request.GET_RECORD_ARENA_NORMAL)
    @check_userid
    def get_record_arena_normal(self, request, response):
        ServiceArenaNormal.Get_Record(self, response)

    @register_process(Request.GET_REWARD_ARENA_NORMAL)
    @check_userid
    def get_reward_arena_normal(self, request, response):
        ServiceArenaNormal.Get_Reward(self, response)

    @register_process(Request.GET_HOF_ARENA_NORMAL)
    @check_userid
    @check_field
    def get_hof_arena_normal(self, request, response):
        ServiceArenaNormal.Get_HOF(self, request, response)

    @register_process(Request.GET_ARENA_TOURNAMENT)
    @check_userid
    def get_arena_tournament(self, request, response):
        ServiceArenaTournament.Get_Info(self, response)
    
    @register_process(Request.RESEARCH_LIST)
    @check_userid
    def research_list(self, request, response):
        ServiceResearch.ResearchList(self, response)

    @register_process(Request.RESEARCH_START)
    @check_userid
    @check_field
    def research_start(self, request, response):
        ServiceResearch.ResearchStart(self, request, response)

    @register_process(Request.RESEARCH_QUICK_COMPLETE)
    @check_userid
    @check_field
    def research_quick_complete(self, request, response):
        ServiceResearch.ResearchQuickComplete(self, request, response)

    @register_process(Request.RESEARCH_END)
    @check_userid
    @check_field
    def research_end(self, request, response):
        ServiceResearch.ResearchEnd(self, request, response)