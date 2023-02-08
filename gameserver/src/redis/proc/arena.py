# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.redis.proc.base import ProcBase


class ArenaProc(ProcBase):
    def __init__(self, factory):
        ProcBase.__init__(self, factory)

    def set_hall_of_fame_data(self, key, data):
        self.redis().hmset(key, data)

    def get_hall_of_fame_data(self, key):
        return self.redis().hgetall(key)

    def set_arena_normal_rank(self, userid, rank):
        self.redis().zadd(GAMECOMMON.ARENA_NORMAL, {userid : rank})
        return

    def get_arena_normal_rank(self, userid):
        rank = self.factory.redis().zscore(GAMECOMMON.ARENA_NORMAL, userid)
        return 0 if rank is None else int(rank)

    def get_arena_normal_total(self):
        _count = self.factory.redis().zcard(GAMECOMMON.ARENA_NORMAL)
        return int(_count)

    def get_arena_normal_userid(self, rank):
        return self.factory.redis().zrange(GAMECOMMON.ARENA_NORMAL, rank -1, rank -1, withscores=False)

    def arena_normal_rank_range(self, high, low):
        return self.factory.redis().zrange(GAMECOMMON.ARENA_NORMAL, high -1, low -1, withscores=True)

    def set_arena_season_count(self, count):
        self.redis().hmset('ARENA_SEASON_INFO', {
            'SEASON_COUNT': count
        })

    def flush_db(self):
        self.factory.redis().flushdb()

