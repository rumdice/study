# -*- coding: utf-8 -*-
from src.common.logger import register_logger


@register_logger('repository')
class RepositoryBase(object):
    def __init__(self, account_factory, game_factory, guild_factory, admintool_factory, table):
        self.account_factory = account_factory
        self.game_factory = game_factory
        self.guild_factory = guild_factory
        self.admintool_factory = admintool_factory
        self.table = table
