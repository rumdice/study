# -*- coding: utf-8 -*-
from src.rdb.mapper.guild.tb_guild import *
from src.rdb.mapper.guild.tb_guild_contest_damage import *
from src.rdb.mapper.guild.tb_guild_member import *
from src.rdb.mapper.guild.tb_guild_raid_damage import *
from src.rdb.mapper.guild.tb_guildinfo import *
from src.rdb.mapper.guild.tb_raid_result import *
from src.rdb.sqlsession import *


def create_guild_factory(parser, prefix="db_guild"):
    config = parser.items("database")
    session_config = SqlSessionConfigureWithConfig(config, prefix)
    session_config.add_mapper(
        GuildDAO,
        GuildInfoDAO, 
        GuildMemberDAO, 
        GuildRaidDamageDAO, 
        RaidResultDAO, 
        GuildContestDamageDAO,
    )
    return SqlSessionFactory(session_config)
