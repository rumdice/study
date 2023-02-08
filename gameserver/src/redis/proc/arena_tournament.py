# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.redis.proc.base import ProcBase


class ArenaTournamentProc(ProcBase):
    def __init__(self, factory):
        ProcBase.__init__(self, factory)

    def set_tournament_data(self, key, data):
        self.redis().hmset(key, data)

    def set_tournament_info(self, group, match_dict):
        self.redis().hmset(group, {
            GAMECOMMON.R_TOURNAMENT_MATCH_LIST: match_dict,
        })

    def get_tournament_data(self, key):
        return self.redis().hgetall(key)

    def flush_db(self):
        self.factory.redis().flushdb()

