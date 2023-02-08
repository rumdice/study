# -*- coding: utf-8 -*-
import os

from src.rdb.account_db import *
from src.rdb.game_db import *
from src.rdb.guild_db import *
from src.rdb.repo.account.account import *
from src.rdb.repo.admintool.arena_tournament_info import *
from src.rdb.repo.admintool.event_dungeon import *
from src.rdb.repo.admintool.guild_contest_info import *
from src.rdb.repo.game.arena_normal import *
from src.rdb.repo.game.arena_tournament import *
from src.rdb.repo.game.attendance import *
from src.rdb.repo.game.darknest import *
from src.rdb.repo.game.deck import *
from src.rdb.repo.game.endless_tower import *
from src.rdb.repo.game.event_dungeon import *
from src.rdb.repo.game.farming_tower import *
from src.rdb.repo.game.gacha import *
from src.rdb.repo.game.inven import *
from src.rdb.repo.game.makeitem import *
from src.rdb.repo.game.post import *
from src.rdb.repo.game.profile import *
from src.rdb.repo.game.region_mission import *
from src.rdb.repo.game.regioninfo import *
from src.rdb.repo.game.research import *
from src.rdb.repo.game.resource import *
from src.rdb.repo.game.territory import *
from src.rdb.repo.game.territory_build import *
from src.rdb.repo.game.tradeitem import *
from src.rdb.repo.guild.guild import *
from src.rdb.repo.guild.guildcontestdamage import *
from src.rdb.repo.guild.guildinfo import *
from src.rdb.repo.guild.guildmember import *
from src.rdb.repo.guild.guildraiddamage import *
from src.rdb.repo.guild.raid_result import *
from src.redis.redis_storage import *


class GameServerContext(object):
    def __init__(self, inifile, *args, **kwargs):
        from src.common.config_parser import GameServerConfigParser

        basedir = os.path.dirname(inifile)
        parser = GameServerConfigParser(basedir=basedir)
        parser.read(inifile)

        # self.pay_url = parser.get("pay_url", "call_pay_url")
        self.server_config = {
            "default_lang": parser.get("server_config", "default_lang"),
            "guild_chatting_server": parser.get("server_config", "guild_chatting_server")
        }

        _creator = (lambda obj: obj(parser) if obj is not None else None)
        self.table = _creator(kwargs.pop('table', None))

        # redis db1 - ini 파일 참조 (defualt.local / service.local)
        # 접속한 클라에 대한 세션 정보 - 접속 유지시간 (TTL)
        self.session = create_session(parser)             # get
        self.session_clone = create_session_clone(parser) # set

        # redis db2
        # 유저 정보에 대한 캐싱 데이터 (rdb에도 있지만 간략화 해서 중복 저장해둠)
        # 성능상의 이슈로 진행한 듯 함.
        self.cache = create_cache(parser)
        self.cache_clone = create_cache_clone(parser)

        # redis db4
        # 길드 정보 - 마찬가지로 RDB와 중복해서 쓰고 있음.
        self.guild = create_guild(parser)
        self.guild_clone = create_guild_clone(parser)

        # TODO: 서버 서비스 코드에서 현재 쓰이지 않음. 과거 오래전 주석처리된 real_event.py에서 일부 쓰임
        # self.event_redis = create_event_repository(parser)
        # self.event_clone_redis = create_event_clone_repository(parser)

        # redis db5 - arena normal
        # 아레나 일반전 랭킹 점수표
        self.arena = create_arena(parser)
        self.arena_clone = create_arena_clone(parser)

        # redis db6
        self.arena_tournament = create_arena_tournament(parser) 
        self.arena_tournament_clone = create_arena_tournament_clone(parser)

        after_init = kwargs.pop("after_init", None)
        if after_init is not None:
            after_init(self, parser)


class RepositoryFactory(object):
    def __init__(self, parser, table, write_db=False):
        if write_db:
            self.account_factory = create_account_factory(parser)
            self.game_factory = create_game_factory(parser)
            self.guild_factory = create_guild_factory(parser)
            self.admintool_factory = create_admintool_factory(parser)
        else:
            self.account_factory = None
            self.game_factory = None
            self.guild_factory = None
            self.admintool_factory = None

        self.table = table
        self.repositories = self._get_repositories()

    def __getitem__(self, item):
        repo = self.repositories[item]
        if not repo:
            return None
        return repo(
            self.account_factory,
            self.game_factory,
            self.guild_factory,
            self.admintool_factory,
            self.table
        )

    def _get_repositories(self):
        return dict(
            account = Account,
            halloffame = HallofFame,
            profile = Profile,
            heroinven = HeroInven,
            equipinven = EquipInven,
            etcinven = EtcInven,
            territory = Territory,
            regioninfo = RegionInfo,
            resourcecollect = ResourceCollect,
            resourcedispatch = ResourceDispatch,
            gacha = Gacha,
            territorybuild = TerritoryBuild,
            tradeitem = TradeItem,
            makeitem = MakeItem,
            guild = Guild,
            guildinfo = GuildInfo,
            guildmember = GuildMember,
            guildraiddamage = GuildRaidDamage,
            guildraidresult = RaidResult,
            guildcontestdamage = GuildContestDamage,
            farmingtower = FarmingTower,
            endlesstower = EndlessTower,
            arenanormal = ArenaNormal,
            arenatournament = ArenaTournament,
            eventdungeon = EventDungeon,
            regionmission = RegionMission,
            post = Post,
            attendance = Attendance,
            darknest = Darknest,
            deck = Deck,
            tourmentinfoadmin = ArenaTournamentInfo,
            eventdungeonadmin = EventDungeonAdmin,
            guildcontestinfo = GuildContestInfo,
            research = Research,
        )

def init_callback(ctx, parser):
    table = ctx.table
    ctx.w_db = RepositoryFactory(parser, table, True)

conf_dir = os.path.dirname(os.path.abspath(__file__)) + "/conf/"
service_ini = conf_dir + "service_local.ini"
if __name__ == '__main__':
    context = GameServerContext(
        inifile=service_ini,
        after_init=init_callback
    )
