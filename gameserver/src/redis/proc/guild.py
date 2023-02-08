# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.redis.proc.base import ProcBase


class GuildProc(ProcBase):
    def __init__(self, factory):
        ProcBase.__init__(self, factory)

    # Setting User information.
    # @NOTE guild battle
    def insert_guild_info(self, guild_uid, guild_name, master_uid, guild_bg, guild_emblem, join_option, join_level, msg):
        self.factory.redis().hset(
            guild_uid,
            mapping = {
                GAMECOMMON.GUILD_NAME: guild_name,
                GAMECOMMON.GUILD_MASTER_UID: master_uid,
                GAMECOMMON.GUILD_BG: guild_bg,
                GAMECOMMON.GUILD_EMBLEM: guild_emblem,
                GAMECOMMON.GUILD_JOIN_TYPE: join_option,
                GAMECOMMON.GUILD_JOIN_LEVEL: join_level,
                GAMECOMMON.GUILD_MEMBER_COUNT: 1,
                GAMECOMMON.GUILD_POINT: 0,
                GAMECOMMON.GUILD_MESSAGE: msg
            }
        )
        self.factory.redis().set(guild_name, guild_uid)

    def get_guild_info(self, guild_uid):
        return self.factory.redis().hgetall(guild_uid)

    def get_guild_info_name(self, guild_name):
        guild_uid = self.factory.redis().get(guild_name)
        if None == guild_uid:
            return 0
        return int(guild_uid)

    def get_guild_rank(self, guild_uid):
        _ranking = self.factory.redis().zrevrank(GAMECOMMON.GUILD_RANK, guild_uid)
        return 0 if _ranking is None else _ranking + 1

    def update_guild_info(self, guild_uid, key, value):
        self.factory.redis().hset(guild_uid, key, value)

    def update_guild_info_dict(self, guild_uid, data):
        self.factory.redis().hmset(guild_uid, data)

    def get_ranking_list(self, high, low, withscores=True):
        return self.factory.redis().zrevrange(GAMECOMMON.GUILD_RANK, high-1, low-1, withscores)

    def update_guild_point(self, guild_uid, value):
        self.factory.redis().zadd(GAMECOMMON.GUILD_RANK, value, guild_uid)

    def get_random_list(self, limit_count):
        count = 0
        keys = []
        while True:
            if limit_count == count:
                return keys

            temp = self.factory.redis().randomkey()
            if not temp:
                count += 1
                continue

            if temp.isdigit():
                if int(temp) in keys:
                    count += 1
                    continue
                keys.append(int(temp))
            count += 1
        return keys

    def del_guild_info(self, guild_uid):
        del_redis = self.get_guild_info(guild_uid)
        guild_name = ""
        if del_redis:
            guild_name = del_redis.get(GAMECOMMON.GUILD_NAME, "")

        self.factory.redis().delete(guild_name)
        self.factory.redis().delete(guild_uid)
        self.factory.redis().zrem(GAMECOMMON.GUILD_RANK, guild_uid)

    def change_guild_name(self, guild_uid, name):
        r_guild = self.factory.redis().hgetall(guild_uid)
        self.factory.redis().delete(r_guild[GAMECOMMON.GUILD_NAME])
        self.factory.redis().set(name, guild_uid)

    def clear(self):
        self.factory.redis().flushdb()
