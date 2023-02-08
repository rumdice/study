# -*- coding: utf-8 -*-
from src.rdb.mapper.account.tb_account import *
from src.rdb.mapper.admintool.arena_tournament_info import *
from src.rdb.mapper.admintool.event_dungeon import *
from src.rdb.mapper.admintool.guild_contest_info import *
from src.rdb.sqlsession import *


def create_account_factory(parser, prefix="db_account"):
    config = parser.items("database")
    session_config = SqlSessionConfigureWithConfig(config, prefix)
    session_config.add_mapper(
        AccountDAO, 
        ArenaNormalHallOfFameDAO
    )
    return SqlSessionFactory(session_config)


def create_admintool_factory(parser, prefix='db_admintool'):
    config = parser.items("database")
    session_config = SqlSessionConfigureWithConfig(config, prefix)
    session_config.add_mapper(
        ArenaTournamentInfoDAO, 
        EventDungeonDAO, 
        GuildContestInfoDAO
    )
    return SqlSessionFactory(session_config)
