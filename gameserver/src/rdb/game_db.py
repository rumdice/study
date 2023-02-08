# -*- coding: utf-8 -*-
import re

from sqlalchemy import types
from sqlalchemy.dialects.mysql import LONGTEXT

from src.rdb.mapper.game.tb_arena_normal import *
from src.rdb.mapper.game.tb_arena_tournament import *
from src.rdb.mapper.game.tb_attendance import *
from src.rdb.mapper.game.tb_darknest import *
from src.rdb.mapper.game.tb_deck import *
from src.rdb.mapper.game.tb_endless_tower import *
from src.rdb.mapper.game.tb_event_dungeon import *
from src.rdb.mapper.game.tb_farming_tower import *
from src.rdb.mapper.game.tb_gacha import *
from src.rdb.mapper.game.tb_inventory import *
from src.rdb.mapper.game.tb_make_item import *
from src.rdb.mapper.game.tb_post import *
from src.rdb.mapper.game.tb_profile import *
from src.rdb.mapper.game.tb_region_info import *
from src.rdb.mapper.game.tb_region_mission import *
from src.rdb.mapper.game.tb_research import *
from src.rdb.mapper.game.tb_resource import *
from src.rdb.mapper.game.tb_territory import *
from src.rdb.mapper.game.tb_territory_build import *
from src.rdb.mapper.game.tb_tradeitem import *
from src.rdb.sqlsession import *

REGEX_UNPACK = re.compile('(?<!\\|)\\|(?!\\|)')


def bar_escape(item):
    return str(item).replace('|', '||')


def bar_encode(items):
    if not isinstance(items, (list, tuple)):
        return items

    if items is None:
        return '||'

    return '|%s|' % '|'.join(bar_escape(item) for item in items if str(item).strip())


def bar_decode_integer(value):
    if value is None:
        return []

    if not hasattr(value, 'split') and hasattr(value, 'read'):
        value = value.read()
    return [int(x) for x in value.split('|') if x.strip()]


def bar_decode_string(value):
    if value is None:
        return []

    return [x.replace('||', '|') for x in
            REGEX_UNPACK.split(value[1:-1]) if x.strip()]


class IntegerListType(types.TypeDecorator):
    impl = LONGTEXT

    def process_result_value(self, value, dialect):
        return bar_decode_integer(value)

    def process_bind_param(self, value, dialect):
        return bar_encode(value)


def create_game_factory(parser, prefix='db_game'):
    config = parser.items("database")
    session_config = SqlSessionConfigureWithConfig(config, prefix)
    session_config.add_mapper(
        ProfileDAO, 
        InvenHeroDAO, 
        InvenEquipDAO, 
        InvenEtcDAO, 
        TerritoryDAO, 
        RegionInfoDAO,
        ResourceCollectDAO, 
        ResourceDispatchDAO, 
        GachaDAO, 
        TerritoryBuildDAO, 
        RegionMissionDAO,
        TradeItemDAO, 
        MakeItemDAO, 
        FarmingTowerDAO, 
        EndlessTowerDAO, 
        ArenaNormalDAO, 
        ArenaTournamentDAO,
        EventDungeonDAO, 
        PostDAO, 
        AttendanceDAO, 
        DarknestDAO,
        DeckDAO,
        ResearchDAO
    )
    return SqlSessionFactory(session_config)