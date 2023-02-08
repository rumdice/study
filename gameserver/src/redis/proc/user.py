# -*- coding: utf-8 -*-
from src.common.gamecommon import GAMECOMMON
from src.protocol.webapp_pb import Define
from src.redis.proc.base import ProcBase


class UserProc(ProcBase):
    def __init__(self, factory):
        ProcBase.__init__(self, factory)

    # Setting User information.
    def set_user_profile(self, user_id, nickname, last_login, team_info, level, exp, territory_dict, start_hero):
        self.redis().hmset(user_id, {
            GAMECOMMON.R_USER_NICK: nickname,
            GAMECOMMON.R_USER_LAST_LOGIN: last_login,
            GAMECOMMON.R_USER_TEAM_INFO: team_info,
            GAMECOMMON.R_USER_LEVEL: level,
            GAMECOMMON.R_USER_EXP: exp,
            GAMECOMMON.R_USER_REFRESH_RESOURCE: '[0,0,0]',
            GAMECOMMON.R_USER_RESOURCE_SLOT: '[1, 2, 3, 4]',
            GAMECOMMON.R_USER_TERRITORY_INFO: territory_dict,
            GAMECOMMON.R_USER_GUILD_UID: 0,
            GAMECOMMON.R_USER_GUILD_GRADE: Define.GUILD_GRADE_NONE,
            GAMECOMMON.R_USER_PVP_POINT: 0,
            GAMECOMMON.R_USER_AVATAR_ID: 0,
            GAMECOMMON.R_USER_GUILD_POINT: 0,
            GAMECOMMON.R_USER_CHECK_UPDATE: '[0,0,0,0,0]',
            GAMECOMMON.R_USER_HAD_HERO_SET: start_hero,
            GAMECOMMON.R_USER_COLLECTED_SINGLE_SET: '{}',
            GAMECOMMON.R_USER_COLLECTED_GROUP_SET: '{}',
            GAMECOMMON.R_USER_LEVEL_SET: '{1}',
        })

    def get_user_profile(self, user_id):
        return self.redis().hgetall(user_id)

    def get_user_data(self, user_id, key):
        return self.redis().hget(user_id, key)

    def remove_user_profile(self, user_id):
        self.redis().delete(user_id)

    def set_user_info(self, user_id, key, value):
        self.redis().hset(user_id, key, value)

    def set_user_info_dict(self, user_id, data):
        self.redis().hset(user_id, mapping=data)

    def clear(self):
        self.factory.redis().flushdb()
