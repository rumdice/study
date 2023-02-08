# -*- coding: utf-8 -*-

from src.common.gamecommon import GAMECOMMON
from src.common.util import *
from src.protocol.webapp_pb import *


class ServiceAccount(object):
    def CheckVerison(self, request, response):
        if request.check_version.current_version != Request.PROTOCOL_VERSION:
            response.result = Response.VERSION_CHECK_FAIL
            return

        server_config = self.context.server_config

        response.server_config.default_language = server_config["default_lang"]
        response.server_config.guild_chatting_server = server_config["guild_chatting_server"]
        response.result = Response.SUCCESS
        return

    def CheckUpdate(self, response):
        post_count = 0
        is_raid_reward = False

        r_update_data = self.cache_clone.get_user_data(self.userid, GAMECOMMON.R_USER_CHECK_UPDATE)
        if r_update_data:
            update_list = convert_string_to_array(r_update_data)
            post_count = self.w_db['post'].post_count(self.userid)
            is_raid_reward = bool(update_list[GAMECOMMON.UPDATE_GUILD_RAID])

        response.check_update.post_count = post_count
        response.check_update.raid_reward = is_raid_reward
        response.result = Response.SUCCESS
        return

    def PushAlramAgree(self, request, response):
        req_agree = request.push_alram_agree.agree

        account_db = self.w_db['account'].find_user_id(self.userid)
        if not account_db:
            response.result = Response.USER_INVALID
            return

        if account_db.push_alram_agree != req_agree:
            self.w_db['account'].update_alram_agree(self.userid, req_agree)

        response.result = Response.SUCCESS
        return


