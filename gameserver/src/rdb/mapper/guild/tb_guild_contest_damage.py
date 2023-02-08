# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, select

from src.rdb.sqlsession import Mapper


class GuildContestDamageDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_guild_contest_damage'
        self.tguildcontestdamage = self.tables[table_name]

    def get_guild_member_damage(self, member_uid, guild_uid):
        query = select([self.tguildcontestdamage]).where(
            and_(
            self.tguildcontestdamage.c.auid == member_uid,
            self.tguildcontestdamage.c.guild_uid == guild_uid
            )
        )
        return query

    def get_guild_damage_list(self, guild_uid):
        query = select([self.tguildcontestdamage]).where(
            self.tguildcontestdamage.c.guild_uid == guild_uid
        )
        return query

    def get_guild_total_damage(self, guild_uid):
        query = select([self.tguildcontestdamage.c.total_damage]).where(
            self.tguildcontestdamage.c.guild_uid == guild_uid
        )
        return query

    def contest_damage_clear(self):
        query = delete(self.tguildcontestdamage).where(
            self.tguildcontestdamage.c.guild_uid != 0
        )
        return query
