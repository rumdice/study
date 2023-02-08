# -*- coding: utf-8 -*-
from sqlalchemy import and_, delete, insert, select, update

from src.rdb.sqlsession import Mapper


class RaidResultDAO(Mapper):
    def __init__(self, metadata):
        Mapper.__init__(self, metadata)
        table_name = self.metadata.schema + '.tb_raid_result'
        self.traidresult = self.tables[table_name]

    def add_raid_result(self, guild_uid):
        query = insert(self.traidresult).values(
            guild_uid = guild_uid,
            damage_record = '[]'
        )
        return query

    def del_raid_result(self, guild_uid):
        query = delete(self.traidresult).where(
            self.traidresult.c.guild_uid == guild_uid
        )
        return query

    def find_raid_result(self, guild_uid):
        query = select([self.traidresult]).where(
            self.traidresult.c.guild_uid == guild_uid
        )
        return query

    def update_raid_result(self, guild_uid, id, element, cur_hp, level, damage):
        query = update(self.traidresult).values(
            raid_monster = id,
            element = element,
            monster_hp = cur_hp,
            monster_level = level,
            damage_record = damage
        ).where(
            self.traidresult.c.guild_uid == guild_uid
        )
        return query

