# -*- coding: utf-8 -*-

from src.redis.proc.arena import *
from src.redis.proc.arena_tournament import *
from src.redis.proc.event import *
from src.redis.proc.guild import *
from src.redis.proc.user import *
from src.redis.redis_connection import *
from src.redis.session import *


def create_session(parser, prefix='redis-'):
    config = parser.items('session')
    configure = RedisConfig(config, prefix)
    return Session(RedisConnectionFactory(configure))


def create_session_clone(parser, prefix='clone-redis-'):
    config = parser.items('session')
    configure = RedisConfig(config, prefix)
    return Session(RedisConnectionFactory(configure))


def create_cache(parser, prefix='redis-'):
    config = parser.items('cache_manager')
    configure = RedisConfig(config, prefix)
    return UserProc(RedisConnectionFactory(configure))


def create_cache_clone(parser, prefix='clone-redis-'):
    config = parser.items('cache_manager')
    configure = RedisConfig(config, prefix)
    return UserProc(RedisConnectionFactory(configure))


def create_guild(parser, prefix='redis-'):
    config = parser.items('guild_manager')
    configure = RedisConfig(config, prefix)
    return GuildProc(RedisConnectionFactory(configure))


def create_guild_clone(parser, prefix='clone-redis-'):
    config = parser.items('guild_manager')
    configure = RedisConfig(config, prefix)
    return GuildProc(RedisConnectionFactory(configure))


def create_arena(parser, prefix='redis-'):
    config = parser.items('arena_manager')
    configure = RedisConfig(config, prefix)
    return ArenaProc(RedisConnectionFactory(configure))


def create_arena_clone(parser, prefix='clone-redis-'):
    config = parser.items('arena_manager')
    configure = RedisConfig(config, prefix)
    return ArenaProc(RedisConnectionFactory(configure))

def create_arena_tournament(parser, prefix='redis-'):
    config = parser.items('arena_tournament_manager')
    configure = RedisConfig(config, prefix)
    return ArenaTournamentProc(RedisConnectionFactory(configure))


def create_arena_tournament_clone(parser, prefix='clone-redis-'):
    config = parser.items('arena_tournament_manager')
    configure = RedisConfig(config, prefix)
    return ArenaTournamentProc(RedisConnectionFactory(configure))


def create_event_repository(parser, prefix='redis-'):
    config = parser.items('event_manager')
    configure = RedisConfig(config, prefix)
    return EventProc(RedisConnectionFactory(configure))


def create_event_clone_repository(parser, prefix='clone-redis-'):
    config = parser.items('event_manager')
    configure = RedisConfig(config, prefix)
    return EventProc(RedisConnectionFactory(configure))