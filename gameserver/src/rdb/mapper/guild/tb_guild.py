# -*- coding: utf-8 -*-
from sqlalchemy import delete, desc, insert, select, update

from src.rdb.sqlsession import Mapper


class GuildDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_guild'
        self.tguild = self.tables[table_name]

    def add_guild(self, name, master_uid, bg, emblem, time):
        query = insert(self.tguild).values(
            guild_name = name,
            guild_master = master_uid,
            guild_bg = bg,
            guild_emblem = emblem,
            guild_create = time
        )
        return query

    def delete_guild(self, guild_uid):
        query = delete(self.tguild).where(
            self.tguild.c.guild_uid == guild_uid
        )
        return query

    def change_master(self, guild_uid, master_uid):
        query = update(self.tguild).values(
            guild_master = master_uid
        ).where(
            self.tguild.c.guild_uid == guild_uid
        )
        return query

    def get_guild_recommend_list(self, limit_count):
        query = select([self.tguild]).order_by(
            desc(self.tguild.c.guild_uid)
        ).limit(
            limit_count
        )
        return query

    def get_guild_search_list(self, limit_count, search_key):
        search_key = "%{}%".format(search_key)
        query = select([self.tguild]).order_by(
            desc(self.tguild.c.guild_uid)
        ).limit(
            limit_count
        ).filter(
            self.tguild.c.guild_name.like(search_key)
        )
        return query

    def modify_guild(self, guild_uid, guild_bg, guild_emblem):
        query = update(self.tguild).values(
            guild_bg=guild_bg,
            guild_emblem=guild_emblem
        ).where(
            self.tguild.c.guild_uid == guild_uid
        )
        return query

    def select_guild(self, guild_uid):
        query = select([self.tguild]).where(
            self.tguild.c.guild_uid == guild_uid
        )
        return query

    def select_guild_all(self):
        query = select([self.tguild])
        return query
