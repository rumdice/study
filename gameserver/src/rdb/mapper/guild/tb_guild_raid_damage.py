# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, select

from src.rdb.sqlsession import Mapper


class GuildRaidDamageDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_guild_raid_damage'
        self.tguildraiddamage = self.tables[table_name]

    def get_guild_member_damage(self, member_uid, guild_uid):
        query = select([self.tguildraiddamage]).where(
            and_(
            self.tguildraiddamage.c.auid == member_uid,
            self.tguildraiddamage.c.guild_uid == guild_uid
            )
        )
        return query

    def get_guild_damage_list(self, guild_uid):
        query = select([self.tguildraiddamage]).where(
            self.tguildraiddamage.c.guild_uid == guild_uid
        )
        return query

    def get_guild_total_damage(self, guild_uid):
        query = select([self.tguildraiddamage.c.total_damage]).where(
            self.tguildraiddamage.c.guild_uid == guild_uid
        )
        return query

    def raid_damage_clear(self):
        query = delete(self.tguildraiddamage).where(
            self.tguildraiddamage.c.guild_uid != 0
        )
        return query