# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class GuildContestInfoDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self,metadata)
        table_name = self.metadata.schema + '.guild_contest_info'
        self.guildcontestinfo = self.tables[table_name]

    def get_guild_contest_info(self):
        query = select([self.guildcontestinfo]).where(self.guildcontestinfo.c.uid == 1)
        return query